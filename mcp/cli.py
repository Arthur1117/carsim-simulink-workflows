import argparse
import asyncio
import json

from core import Engine
from workflow import execute_prepared,run_closed_loop

parser=argparse.ArgumentParser(description='Local CarSim 2021 / R2025b workflow')
parser.add_argument('action',choices=['info','initialize','prepare','run','execute','validate','status','rollback','audit'])
parser.add_argument('--id')
parser.add_argument('--config')
parser.add_argument('--label',default='abs')
parser.add_argument('--mass',type=float,help='Unladen SPRUNG mass M_SU, kg; not total vehicle mass')
parser.add_argument('--cg-height',type=float,help='Unladen sprung-mass CG height H_CG_SU, mm')
parser.add_argument('--yaw-inertia',type=float,help='Unladen sprung-mass yaw inertia IZZ_SU, kg-m2')
parser.add_argument('--stop-time',type=float,default=2.0)
args=parser.parse_args()
engine=Engine(args.config)
overrides={k:v for k,v in [('M_SU',args.mass),('H_CG_SU',args.cg_height),('IZZ_SU',args.yaw_inertia)] if v is not None}
if args.action=='info': result=engine.info()
elif args.action=='initialize': result=engine.initialize()
elif args.action=='prepare': result=engine.prepare(args.label,overrides,args.stop_time)
elif args.action=='run': result=asyncio.run(run_closed_loop(engine,args.label,overrides,args.stop_time))
elif args.action=='execute': result=asyncio.run(execute_prepared(engine,args.id))
elif args.action=='validate': result=engine.validate(args.id)
elif args.action=='status': result=engine.status(args.id)
elif args.action=='rollback': result=engine.rollback(args.id)
else: result=engine.audit_original()
print(json.dumps(result,indent=2,ensure_ascii=False))
