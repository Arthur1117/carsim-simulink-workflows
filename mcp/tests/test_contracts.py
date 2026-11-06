from pathlib import Path
import json
import os
import shutil
import sys
import tempfile
import unittest
import subprocess

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(APP))
from core import APP, Engine, WorkflowError, IMPORTS, EXPORTS, inside, sha256, write_json

class Contracts(unittest.TestCase):
    def setUp(self):
        scratch = APP/'.state'/'test-scratch'
        scratch.mkdir(parents=True,exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.temp = Path(self.temporary.name).resolve()
        assert self.temp.is_relative_to(scratch.resolve())
        self.source = self.temp/'source'
        base = self.source/'Results'/'reviewed-abs'/'Run_all.par'
        base.parent.mkdir(parents=True)
        channels = [f'IMPORT {name}' for name in IMPORTS] + [f'EXPORT {name}' for name in EXPORTS]
        base.write_text('\n'.join(['PARSFILE', 'M_SU 1110', 'H_CG_SU 540', *channels, 'END', '']), encoding='latin-1')
        self.base_rel = base.relative_to(self.source)
        self.base_hash = sha256(base)
        model = self.temp/'reviewed-model.slx'
        model.write_bytes(b'Fixture for prepare/rollback only; not a runnable Simulink model.')
        raw = self.source/'Runs'/'fixture.par'
        raw.parent.mkdir()
        raw.write_text('PARSFILE\n#FullDataName Test`Fixture`Unit\nM_SU 1110\nEND\n',encoding='latin-1')
        cfg = {'workspace':'managed', 'original_database':'source', 'carsim_program':'program',
               'abs_base':self.base_rel.as_posix(), 'abs_base_sha256':self.base_hash,
               'abs_model':model.name, 'model_sha256':sha256(model)}
        self.config = self.temp/'config.json'
        write_json(self.config,cfg)
        self.engine = Engine(self.config)
        self.engine.initialize()

    def tearDown(self):
        assert self.temp.is_relative_to((APP/'.state'/'test-scratch').resolve())
        self.temporary.cleanup()

    def test_real_copy_integrity_and_reuse(self):
        first = self.engine.initialize()
        self.assertTrue(first['reused'])
        self.assertEqual(sha256(self.engine.database/self.base_rel),self.base_hash)

    def test_database_tools_work_without_abs_profile(self):
        self.engine.config['abs_base'] = ''
        self.engine.config['abs_model'] = ''
        self.assertTrue(self.engine.initialize()['reused'])
        self.engine.dataset('Runs/fixture.par')
        with self.assertRaisesRegex(WorkflowError, 'ABS_BASE_PATH'):
            self.engine.prepare('requires-reviewed-profile')

    def test_source_and_traversal_are_rejected(self):
        for target in [self.source/'Runs'/'fixture.par', self.engine.root/'..'/'source'/'Runs'/'fixture.par']:
            with self.assertRaises(WorkflowError):
                self.engine.source_safe(target)
        with self.assertRaises(WorkflowError):
            self.engine.dataset('../../source/Runs/fixture.par')

    def test_sibling_prefix_is_not_containment(self):
        with self.assertRaises(WorkflowError):
            inside(self.temp/'managed-evil'/'test.par',self.engine.root)

    def test_native_parameter_roundtrip_and_rollback(self):
        before = sha256(self.source/self.base_rel)
        prepared = self.engine.prepare('paramtest',{'M_SU':1150,'H_CG_SU':550})
        folder,job = self.engine.job(prepared['experimentId'])
        self.assertEqual(job['parameterBefore'],{'M_SU':1110.0,'H_CG_SU':540.0})
        self.assertIn('M_SU 1150', (folder/'Run_all.par').read_text(encoding='latin-1'))
        self.assertEqual(before,sha256(self.source/self.base_rel))
        self.assertEqual(sha256(folder/'Run_all.par.bak'),self.base_hash)
        restored=self.engine.rollback(prepared['experimentId'])
        self.assertEqual(restored['restoredBaseSHA256'],self.base_hash)
        self.assertIsNone(self.engine.status(prepared['experimentId'])['validation'])
        with self.assertRaises(WorkflowError):
            self.engine.validate(prepared['experimentId'])

    def test_unknown_nonfinite_boolean_and_range_rejected(self):
        for overrides in [{'TSTOP':2},{'M_SU':float('nan')},{'M_SU':float('inf')},
                          {'M_SU':True},{'M_SU':-1},{'M_SU':'1110\nEND'}]:
            with self.assertRaises(WorkflowError):
                self.engine.prepare('bad',overrides)

    def test_copy_tampering_is_detected(self):
        prepared=self.engine.prepare('tamper')
        folder,job=self.engine.job(prepared['experimentId'])
        with (folder/'simfile.sim').open('a') as stream:
            stream.write('\nDATADIR C:/outside/database\n')
        with self.assertRaisesRegex(WorkflowError,'JOB_FILE_CHANGED'):
            self.engine.job(prepared['experimentId'])

    def test_source_base_tampering_is_detected(self):
        base = self.engine.database/self.base_rel
        base.write_bytes(base.read_bytes()+b'\n')
        with self.assertRaises(Exception):
            self.engine.prepare('basechanged')

    def test_active_workflow_is_exclusive(self):
        with self.engine.exclusive():
            with self.assertRaisesRegex(WorkflowError,'WORKFLOW_BUSY'):
                with self.engine.exclusive():
                    pass

    def test_junction_escape_is_rejected(self):
        link=self.engine.root/'outside'
        subprocess.run(['cmd.exe','/d','/c','mklink','/J',str(link),str(self.source)],
                       capture_output=True,check=True)
        try:
            with self.assertRaisesRegex(WorkflowError,'REPARSE_POINT'):
                self.engine.source_safe(link/'Runs'/'fixture.par')
        finally:
            assert link.parent.resolve()==self.engine.root
            os.rmdir(link)


if __name__ == '__main__':
    unittest.main(verbosity=2)
