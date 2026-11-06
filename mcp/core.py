from __future__ import annotations

import contextlib
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import time
import uuid

APP = Path(__file__).resolve().parent
sys.path.insert(0, str(APP/'vendor'/'carsim_mcp'))
sys.path.insert(0, str(APP/'vendor'/'carsim_guide'))
import carsim_core as upstream
import database_tools
import base_registry

PARAMETERS = {
    'M_SU': {'unit':'kg', 'min':100, 'max':10000, 'meaning':'Unladen sprung mass'},
    'H_CG_SU': {'unit':'mm', 'min':1, 'max':3000, 'meaning':'Unladen sprung-mass CG height'},
    'IZZ_SU': {'unit':'kg-m2', 'min':1, 'max':100000, 'meaning':'Unladen sprung-mass yaw inertia'},
}
IMPORTS = ['IMP_PBK_L1','IMP_PBK_R1','IMP_PBK_L2','IMP_PBK_R2']
EXPORTS = ['Vx_L1','Vx_R1','Vx_L2','Vx_R2','Vx_SM','Pbk_Con']
BASE_HASH = 'd5ea96b4f34955d530c3ffe3421f1d17cf88535bf2b96e89bd5d963c9052ebdf'
RUN_ID = 'Run_9e4c7912-2109-4fbb-8f56-a91b47f2678e'


class WorkflowError(RuntimeError):
    def __init__(self, code, message):
        super().__init__(f'{code}: {message}')
        self.code = code


def sha256(path):
    return base_registry.sha256(path)


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name+'.tmp')
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    os.replace(temporary, path)


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def reject_reparse(path):
    path = Path(path).absolute()
    for component in (path, *path.parents):
        if component.exists():
            info = component.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise WorkflowError('REPARSE_POINT', str(component))


def inside(path, root):
    path, root = Path(path).absolute(), Path(root).absolute()
    reject_reparse(root)
    reject_reparse(path)
    resolved, boundary = path.resolve(), root.resolve()
    if not resolved.is_relative_to(boundary):
        raise WorkflowError('PATH_OUTSIDE_WORKSPACE', str(path))
    return resolved


class Engine:
    def __init__(self, config_path=None):
        self.config_path = Path(config_path or APP/'config.local.json').resolve()
        if not self.config_path.is_file():
            raise WorkflowError('CONFIG_MISSING', 'Copy config.example.json to config.local.json and configure your installation')
        self.config = read_json(self.config_path)
        self.root = self.local_path('workspace')
        self.original = self.local_path('original_database')
        self.prog = self.local_path('carsim_program')
        self.database = self.root/'.state'/'database'
        self.experiments = self.root/'experiments'
        if self.root == self.original or self.root.is_relative_to(self.original) or self.original.is_relative_to(self.root):
            raise WorkflowError('SOURCE_WORKSPACE_OVERLAP', str(self.root))
        reject_reparse(self.root)
        self.root.mkdir(parents=True, exist_ok=True)

    def local_path(self, key):
        value = self.config.get(key)
        if not isinstance(value, str) or not value.strip():
            raise WorkflowError('CONFIG_VALUE_MISSING', key)
        return (self.config_path.parent/Path(value).expanduser()).resolve()

    def source_safe(self, target):
        p = inside(target, self.root)
        if p == self.original or p.is_relative_to(self.original):
            raise WorkflowError('ORIGINAL_DATABASE_WRITE', str(p))
        return p

    @contextlib.contextmanager
    def exclusive(self):
        import msvcrt
        path = self.source_safe(self.root/'.state'/'workflow.lock')
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a+b') as stream:
            stream.seek(0, 2)
            if stream.tell() == 0:
                stream.write(b'0'); stream.flush()
            stream.seek(0)
            try:
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as error:
                raise WorkflowError('WORKFLOW_BUSY', 'Another managed workflow is active') from error
            try:
                yield
            finally:
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)

    def info(self):
        mex = self.prog/'Programs'/'solvers'/'Matlab84+'/'vs_sf.mexw64'
        dll = self.prog/'Programs'/'solvers'/'carsim_64.dll'
        return {'target':'CarSim 2021.0 / MATLAB R2025b / win64',
                'workspace':str(self.root), 'originalDatabase':str(self.original),
                'databaseCloneReady':(self.database/'.clone-ready.json').is_file(),
                'simulinkAvailable':mex.is_file() and dll.is_file(),
                'cliAvailable':False, 'solverMex':str(mex), 'solverDLL':str(dll),
                'supportedProfile':'abs_split_mu', 'parameters':PARAMETERS,
                'originalDatabaseWritableByTools':False}

    def initialize(self):
        with self.exclusive():
            started = time.perf_counter()
            marker = self.database/'.clone-ready.json'
            if marker.is_file():
                self.require_database()
                return {**read_json(marker), 'reused':True, 'elapsedSeconds':time.perf_counter()-started}
            if self.database.exists():
                raise WorkflowError('INCOMPLETE_CLONE', 'Incomplete copy retained; inspect it before resuming')
            if not (self.original/'Runs').is_dir():
                raise WorkflowError('DATABASE_NOT_FOUND', 'Select a CarSim database root containing Runs/')
            files = []
            for parent, dirs, names in os.walk(self.original, followlinks=False):
                for name in dirs+names:
                    reject_reparse(Path(parent)/name)
                for name in names:
                    path = Path(parent)/name
                    files.append({'path':str(path.relative_to(self.original)), 'size':path.stat().st_size,
                                  'sha256':sha256(path)})
            write_json(self.root/'.state'/'original-before.json', files)
            shutil.copytree(self.original, self.database)
            for row in files:
                if sha256(self.database/row['path']) != row['sha256']:
                    raise WorkflowError('CLONE_HASH_MISMATCH', row['path'])
            record = {'source':str(self.original), 'clone':str(self.database), 'files':len(files),
                      'bytes':sum(r['size'] for r in files), 'hashVerified':True,
                      'createdUTC':datetime.now(timezone.utc).isoformat()}
            write_json(marker, record)
            return {**record, 'reused':False, 'elapsedSeconds':time.perf_counter()-started}

    def require_database(self):
        marker = inside(self.database/'.clone-ready.json', self.root)
        if not marker.is_file():
            raise WorkflowError('WORKSPACE_NOT_READY', 'Call initialize_workspace once')
        if Path(read_json(marker)['source']).resolve() != self.original:
            raise WorkflowError('WORKSPACE_SOURCE_CHANGED', 'Select a new workspace for a different source database')

    def profile(self):
        self.require_database()
        relative = self.config.get('abs_base', f'Results/{RUN_ID}/Run_all.par')
        if not relative or Path(relative).is_absolute():
            raise WorkflowError('ABS_BASE_PATH', 'Set abs_base to a file relative to the source database')
        base = inside(self.database/relative, self.database)
        pin = self.config.get('abs_base_sha256', BASE_HASH)
        if not re.fullmatch(r'[0-9a-f]{64}', str(pin)) or not base.is_file() or sha256(base) != pin:
            raise WorkflowError('ABS_BASE_NOT_REVIEWED', 'Check the ABS base path and SHA-256 of the reviewed expanded PAR')
        return {'base_run_all':str(base), 'base_sha256':pin}

    def search(self, query, limit=20):
        self.require_database()
        if not query.strip() or not 1 <= limit <= 100:
            raise WorkflowError('INVALID_QUERY', 'Use a nonempty query and limit 1..100')
        return database_tools.find_datasets(self.database, query, limit=limit)

    def dataset(self, relative_path):
        self.require_database()
        p = inside(self.database/relative_path, self.database)
        if p.suffix.lower() != '.par' or not p.is_file():
            raise WorkflowError('INVALID_DATASET', 'Expected an existing .par inside the clone')
        return {'dataset':upstream.get_dataset(str(p), annotate=False),
                'links':database_tools.get_parsfile_links(p, self.database)}

    def validate_overrides(self, overrides):
        clean = {}
        for keyword, value in overrides.items():
            if keyword not in PARAMETERS:
                raise WorkflowError('UNREGISTERED_PARAMETER', keyword)
            rule = PARAMETERS[keyword]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise WorkflowError('INVALID_PARAMETER_VALUE', keyword)
            if not rule['min'] <= value <= rule['max']:
                raise WorkflowError('PARAMETER_OUT_OF_RANGE', f'{keyword} must be {rule["min"]}..{rule["max"]} {rule["unit"]}')
            clean[keyword] = float(value)
        return clean

    def prepare(self, label='abs', overrides=None, stop_time=2.0):
        profile = self.profile()
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,32}', label):
            raise WorkflowError('INVALID_LABEL', 'Use 1..32 ASCII letters, digits, _ or -')
        if isinstance(stop_time, bool) or not isinstance(stop_time, (int,float)) or not math.isfinite(stop_time) or not 2 <= stop_time <= 10:
            raise WorkflowError('INVALID_STOP_TIME', 'The validated ABS profile allows 2..10 seconds')
        overrides = self.validate_overrides(overrides or {})
        base = Path(profile['base_run_all'])
        text = base.read_text(encoding='latin-1')
        if re.search(r'[A-Za-z]:[\\/]|(?m:^PARSFILE[ \t]+\S)', text):
            raise WorkflowError('UNSAFE_BASE_REFERENCE', 'Base must be expanded and contain no absolute dependencies')
        if re.findall(r'^IMPORT[ \t]+(\S+)',text,re.M) != IMPORTS or re.findall(r'^EXPORT[ \t]+(\S+)',text,re.M) != EXPORTS:
            raise WorkflowError('CHANNEL_CONTRACT_CHANGED', 'ABS imports/exports do not match the bound contract')
        model = self.local_path('abs_model')
        if model.suffix.lower() != '.slx' or not model.is_file():
            raise WorkflowError('ABS_MODEL_MISSING', 'Set abs_model to a reviewed local SLX model')
        if sha256(model) != self.config.get('model_sha256'):
            raise WorkflowError('MODEL_CHANGED', 'Re-audit and deliberately rebind the model before use')
        experiment_id = datetime.now().strftime('%Y%m%d_%H%M%S')+'_'+label+'_'+uuid.uuid4().hex[:8]
        folder = self.source_safe(self.experiments/experiment_id)
        folder.mkdir(parents=True, exist_ok=False)
        copied_base = folder/'Run_all.par'
        shutil.copy2(base, copied_base)
        before = {}
        for key in overrides:
            occurrences = re.findall(r'^'+re.escape(key)+r'[ \t]+([^\r\n]+)',text,re.M)
            if len(occurrences) != 1:
                raise WorkflowError('AMBIGUOUS_PARAMETER', key)
            before[key] = float(occurrences[0].split(';')[0].split('!')[0].strip())
        if overrides:
            upstream.write_parsfile(str(copied_base), {k:format(v,'.17g') for k,v in overrides.items()})
        shutil.copy2(model, folder/'cs21_abs_smoke.slx')
        prefix = str(folder/'native').replace('\\','/')
        simfile = ['SIMFILE', f'INPUT {copied_base.as_posix()}', f'FILEBASE {prefix}',
                   f'INPUTARCHIVE {prefix}_all.par',f'ECHO {prefix}_echo.par',f'FINAL {prefix}_end.par',
                   f'LOGFILE {prefix}_log.txt',f'ERDFILE {prefix}.vs',
                   f'PROGDIR {self.prog.as_posix()}/',f'DATADIR {self.database.as_posix()}/',
                   f'RESOURCEDIR {self.prog.as_posix()}/Resources/',f'ANIFILE {folder.as_posix()}/animator.par',
                   'PRODUCT_ID CarSim','PRODUCT_VER 2021.0','VEHICLE_CODE i_i',
                   'EXT_MODEL_STEP 0.0005','PORTS_IMP 1,4','PORTS_EXP 1,6',
                   f'DLLFILE {self.prog.as_posix()}/Programs/solvers/carsim_64.dll','END']
        (folder/'simfile.sim').write_text('\n'.join(simfile)+'\n',encoding='latin-1')
        job = {'id':experiment_id,'profile':'abs_split_mu','state':'prepared','folder':str(folder),
               'database':str(self.database),'program':str(self.prog),'stopTime':float(stop_time),
               'step':0.0005,'sourceBaseSHA256':profile['base_sha256'],'baseSHA256':sha256(copied_base),
               'modelSHA256':sha256(folder/'cs21_abs_smoke.slx'), 'overrides':overrides,
               'parameterBefore':before,'imports':IMPORTS,'exports':EXPORTS,
               'simfileSHA256':sha256(folder/'simfile.sim'),
               'createdUTC':datetime.now(timezone.utc).isoformat()}
        escaped = str(folder/'job.json').replace("'", "''")
        matlab_dir = str(APP/'matlab').replace("'", "''")
        wrapper = ("function run_prepared\noldPath=path; cleanup=onCleanup(@() path(oldPath));\n"
                   f"addpath('{matlab_dir}');\ncs21_execute('{escaped}');\nend\n")
        (folder/'run_prepared.m').write_text(wrapper,encoding='utf-8')
        job['runnerSHA256'] = sha256(folder/'run_prepared.m')
        write_json(folder/'job.json',job)
        write_json(folder/'result.json',{'passed':False,'stage':'prepared','experimentId':experiment_id})
        return {'experimentId':experiment_id,'runnerPath':str(folder/'run_prepared.m'),
                'folder':str(folder),'overrides':overrides,'state':'prepared'}

    def job(self, experiment_id):
        if not re.fullmatch(r'[0-9]{8}_[0-9]{6}_[A-Za-z0-9_-]{1,32}_[0-9a-f]{8}', experiment_id):
            raise WorkflowError('INVALID_EXPERIMENT_ID', experiment_id)
        folder = self.source_safe(self.experiments/experiment_id)
        job = read_json(folder/'job.json')
        if Path(job['folder']).resolve() != folder or Path(job['database']).resolve() != self.database:
            raise WorkflowError('JOB_PATH_CHANGED', experiment_id)
        for file, key in [('Run_all.par','baseSHA256'),('cs21_abs_smoke.slx','modelSHA256'),
                          ('simfile.sim','simfileSHA256'),('run_prepared.m','runnerSHA256')]:
            if sha256(folder/file) != job[key]:
                raise WorkflowError('JOB_FILE_CHANGED', file)
        return folder, job

    def set_state(self, experiment_id, state, **extra):
        folder, job = self.job(experiment_id)
        job.update(state=state, **extra)
        write_json(folder/'job.json',job)

    def validate(self, experiment_id):
        folder, job = self.job(experiment_id)
        if job['state'] not in ('running','matlab_completed','validated'):
            raise WorkflowError('VALIDATION_STATE', 'Only an executed, non-rolled-back experiment can be accepted')
        result = read_json(folder/'result.json')
        if not result.get('passed') or result.get('experimentId') != experiment_id:
            raise WorkflowError('MATLAB_NOT_ACCEPTED', json.dumps(result,ensure_ascii=False))
        required = ['exports.csv','imports.csv','native_log.txt','native_echo.par','native_end.par','native.vs','native.vsb','simulation.mat']
        for name in required:
            p = folder/name
            if not p.is_file() or p.stat().st_size == 0:
                raise WorkflowError('MISSING_ARTIFACT', name)
        grids = []
        for file, names in [('exports.csv',EXPORTS),('imports.csv',IMPORTS)]:
            with (folder/file).open(newline='',encoding='utf-8-sig') as stream:
                reader = csv.reader(stream)
                if next(reader) != ['Time_s']+names:
                    raise WorkflowError('CSV_CHANNEL_CONTRACT',file)
                data = [[float(v) for v in row] for row in reader]
            if not data or any(len(row)!=len(names)+1 or not all(map(math.isfinite,row)) for row in data):
                raise WorkflowError('NONFINITE_OR_MALFORMED_DATA',file)
            times = [row[0] for row in data]
            if times[0]!=0 or abs(times[-1]-job['stopTime'])>1e-8 or any(b<=a for a,b in zip(times,times[1:])):
                raise WorkflowError('TIME_GRID',file)
            if len(times) != round(job['stopTime']/job['step'])+1:
                raise WorkflowError('SAMPLE_COUNT',file)
            grids.append(times)
        if grids[0] != grids[1]:
            raise WorkflowError('FEEDBACK_GRID_MISMATCH',experiment_id)
        native_log = (folder/'native_log.txt').read_text(encoding='latin-1')
        stop = re.search(r'Run stopped at t = ([0-9]+(?:\.[0-9]+)?)',native_log)
        if not stop or abs(float(stop.group(1))-job['stopTime'])>2*job['step'] or 'External control' not in native_log:
            raise WorkflowError('NATIVE_TERMINATION',experiment_id)
        parsed_echo = upstream.read_parsfile(str(folder/'native_echo.par'))['keywords']
        echo_checks = {}
        for key, expected in job['overrides'].items():
            values = parsed_echo.get(key,[])
            actual = float(values[0].split(';')[0].split('!')[0].strip()) if len(values)==1 else None
            if actual is None or not math.isclose(actual,expected,rel_tol=1e-8,abs_tol=1e-8):
                raise WorkflowError('PARAMETER_ECHO_MISMATCH',key)
            echo_checks[key] = {'requested':expected,'actual':actual,'unit':PARAMETERS[key]['unit']}
        result.update(experimentId=experiment_id, integrationPassed=True,
                      physicsValidated=False, echoChecks=echo_checks,
                      tableExtrapolationMessages=native_log.count('extrapolated'),
                      artifactHashes={name:sha256(folder/name) for name in required},
                      validationScope='Local fixed-profile closed-loop integration', state='validated')
        write_json(folder/'validation.json',result)
        self.set_state(experiment_id,'validated')
        return result

    def rollback(self, experiment_id):
        with self.exclusive():
            folder, job = self.job(experiment_id)
            if job['state'] == 'running':
                raise WorkflowError('RUN_ACTIVE','Cannot roll back an active run')
            backup = folder/'Run_all.par.bak'
            if backup.is_file():
                if sha256(backup) != job['sourceBaseSHA256']:
                    raise WorkflowError('BACKUP_CHANGED',str(backup))
                shutil.copy2(backup,folder/'Run_all.par')
            job.update(state='rolled_back',baseSHA256=sha256(folder/'Run_all.par'))
            write_json(folder/'job.json',job)
            write_json(folder/'rollback.json',{'restoredBaseSHA256':job['baseSHA256'],
                       'originalDatabaseTouched':False,'historicalResultsRetained':True})
            return read_json(folder/'rollback.json')

    def status(self, experiment_id):
        folder, job = self.job(experiment_id)
        return {'job':job,'result':read_json(folder/'result.json'),
                'validation':read_json(folder/'validation.json') if job['state']=='validated' and (folder/'validation.json').is_file() else None,
                'historicalValidationRetained':(folder/'validation.json').is_file()}

    def audit_original(self):
        before = {row['path']:row for row in read_json(self.root/'.state'/'original-before.json')}
        after = {}
        for parent, dirs, names in os.walk(self.original,followlinks=False):
            for name in dirs+names:
                reject_reparse(Path(parent)/name)
            for name in names:
                path=Path(parent)/name
                relative=str(path.relative_to(self.original))
                after[relative]={'path':relative,'size':path.stat().st_size,'sha256':sha256(path)}
        changed=sorted(key for key in before.keys() | after.keys() if before.get(key)!=after.get(key))
        transient={'Log\\log.txt','Log\\log.txt_old.txt','Configuration\\index.cache'}
        data_changed=[key for key in changed if key not in transient]
        return {'allFilesUnchanged':not changed,'sourceDataUnchanged':not data_changed,
                'beforeFiles':len(before),'afterFiles':len(after),'changedPaths':changed,
                'changedNonTransientPaths':data_changed,
                'transientPolicy':'User requested retaining Browser logs/cache; never restore them automatically'}
