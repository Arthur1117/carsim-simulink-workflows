import argparse
from pathlib import Path
import hashlib
import json
import struct

def describe(path):
    result = {'path': str(path), 'exists': path.is_file()}
    if not path.is_file():
        return result
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    result.update(size=path.stat().st_size, sha256=h.hexdigest())
    with path.open('rb') as stream:
        if stream.read(2) == b'MZ':
            stream.seek(0x3c)
            offset = struct.unpack('<I',stream.read(4))[0]
            stream.seek(offset)
            if stream.read(4) == b'PE\0\0':
                result['peMachine'] = hex(struct.unpack('<H',stream.read(2))[0])
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Inspect the local CarSim and MATLAB installations')
    parser.add_argument('--carsim-program', required=True, type=Path)
    parser.add_argument('--database', required=True, type=Path)
    parser.add_argument('--matlab-root', required=True, type=Path)
    args = parser.parse_args()
    PROG, DB, MATLAB = args.carsim_program, args.database, args.matlab_root
    checks = [PROG/'CarSim.exe', PROG/'CarSim_64.exe',
              PROG/'Programs'/'cslm.exe',
              PROG/'Programs'/'VS_SolverWrapper_CLI_64.exe',
              PROG/'Programs'/'solvers'/'carsim_64.dll',
              PROG/'Programs'/'solvers'/'Matlab84+'/'vs_sf.mexw64',
              PROG/'Programs'/'solvers'/'Matlab84+'/'Solver_SF.slx',
              PROG/'Programs'/'solvers'/'Matlab'/'vs_sf.mexw64',
              MATLAB/'bin'/'matlab.exe', DB/'simfile.sim']
    print(json.dumps({'readOnly':True,'files':[describe(p) for p in checks]},indent=2))
