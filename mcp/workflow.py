from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import time
import tomllib
import traceback
import uuid

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from core import Engine, WorkflowError, read_json, write_json


async def matlab_execute(engine, folder):
    settings = tomllib.loads(engine.local_path('codex_config').read_text(encoding='utf-8'))
    matlab = settings['mcp_servers'][engine.config.get('matlab_server_name','matlab')]
    args = list(matlab.get('args',[]))
    args = [arg for arg in args if not arg.startswith('--matlab-session-mode')]
    args.append('--matlab-session-mode=existing')
    env = os.environ.copy()
    env.update(matlab.get('env',{}))
    parameters = StdioServerParameters(command=matlab['command'],args=args,env=env)
    started = time.perf_counter()
    with (folder/'matlab-mcp-stderr.log').open('w',encoding='utf-8') as error_log:
        async with stdio_client(parameters,errlog=error_log) as (read,write):
            async with ClientSession(read,write) as session:
                await session.initialize()
                def inspect(response,restore=False):
                    text='\n'.join(item.text for item in response.content if getattr(item,'type','')=='text')
                    if response.isError or text.lstrip().lower().startswith('matlab error:'):
                        if 'failed to attach' in text.lower():
                            raise WorkflowError('MATLAB_SESSION_NOT_SHARED',
                                'Use the existing official MATLAB MCP to evaluate shareMATLABSession first; then prepare a fresh experiment')
                        code='SESSION_RESTORE_FAILED' if restore else ('LICENSE_UNAVAILABLE' if 'license' in text.lower() else 'MATLAB_EXECUTION_FAILED')
                        raise WorkflowError(code,text[-5000:])
                    return text
                state='cs21_mcp_state_'+uuid.uuid4().hex
                capture=f"assert(~exist('{state}','var')); {state}=struct('folder',pwd,'path',path);"
                inspect(await session.call_tool('evaluate_matlab_code',{'code':capture}))
                try:
                    response=await session.call_tool('run_matlab_file',{'script_path':str(folder/'run_prepared.m')})
                    text='\n'.join(item.text for item in response.content if getattr(item,'type','')=='text')
                    (folder/'matlab-mcp-response.txt').write_text(text,encoding='utf-8')
                    inspect(response)
                finally:
                    restore=(f'cd({state}.folder); path({state}.path); '
                             f'assert(strcmp(pwd,{state}.folder) && strcmp(path,{state}.path)); clear {state};')
                    inspect(await session.call_tool('evaluate_matlab_code',{'code':restore}),restore=True)
    return {'matlabMcpSeconds':time.perf_counter()-started,'sessionRestored':True}


async def execute_prepared(engine: Engine, experiment_id: str):
    with engine.exclusive():
        folder, job = engine.job(experiment_id)
        if job['state'] != 'prepared':
            raise WorkflowError('RUN_NOT_PREPARED','A run can execute only once; prepare a fresh experiment')
        engine.profile()
        started = time.perf_counter()
        process = None
        start_license = bool(engine.config.get('start_license_manager',True))
        engine.set_state(experiment_id,'running',startedUTC=datetime.now(timezone.utc).isoformat())
        try:
            if start_license:
                startup = subprocess.STARTUPINFO()
                startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startup.wShowWindow = 0
                executable = engine.prog/'Programs'/'cslm.exe'
                process = subprocess.Popen([str(executable)],cwd=str(executable.parent),
                                           startupinfo=startup,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                await asyncio.sleep(float(engine.config.get('license_startup_seconds',2)))
            bridge = await asyncio.wait_for(matlab_execute(engine,folder),timeout=600)
            result = engine.validate(experiment_id)
            result.update(bridge,elapsedSeconds=time.perf_counter()-started)
            write_json(folder/'validation.json',result)
            return result
        except BaseException as error:
            def leaves(exc):
                children=getattr(exc,'exceptions',None)
                return [leaf for child in children for leaf in leaves(child)] if children else [exc]
            failures=leaves(error)
            code=next((getattr(exc,'code') for exc in failures if hasattr(exc,'code')),type(error).__name__)
            message='; '.join(str(exc) for exc in failures)[:6000]
            engine.set_state(experiment_id,'failed',failureType=code,failureMessage=message)
            write_json(folder/'failure.json',{'experimentId':experiment_id,
                       'code':code,'message':message,
                       'traceback':traceback.format_exc(),
                       'previousMatlabResult':read_json(folder/'result.json')})
            if isinstance(error,asyncio.CancelledError):
                raise
            raise WorkflowError(code,f'Experiment {experiment_id}: {message}') from error
        finally:
            if process is not None:
                owned = {'pid':process.pid,'startedByWorkflow':True,'closed':False}
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill(); process.wait(timeout=5)
                    owned['closed'] = True
                else:
                    owned['alreadyExited'] = True
                write_json(folder/'license-process.json',owned)


async def run_closed_loop(engine, label='abs', overrides=None, stop_time=2.0):
    initialization = engine.initialize()
    prepared = engine.prepare(label,overrides,stop_time)
    result = await execute_prepared(engine,prepared['experimentId'])
    return {**result,'workspaceInitialization':initialization,'folder':prepared['folder']}
