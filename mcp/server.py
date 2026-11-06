import argparse
import asyncio

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import StrictFloat, StrictInt

from core import Engine
from workflow import execute_prepared, run_closed_loop

parser = argparse.ArgumentParser()
parser.add_argument('--config',default=None)
args = parser.parse_args()
engine = Engine(args.config)
mcp = FastMCP('carsim2021-local')
READ = ToolAnnotations(readOnlyHint=True,destructiveHint=False,openWorldHint=False)
WRITE = ToolAnnotations(readOnlyHint=False,destructiveHint=False,openWorldHint=False)


@mcp.tool(annotations=READ)
def carsim_info() -> dict:
    """Inspect this computer's 2021 paths and supported capabilities; does not start a solver."""
    return engine.info()


@mcp.tool(annotations=WRITE)
def initialize_workspace() -> dict:
    """Create and hash-verify one complete database clone, or reuse its verified bound base."""
    return engine.initialize()


@mcp.tool(annotations=READ)
def search_datasets(query: str, limit: int = 20) -> list:
    """Search dataset names in the managed clone using upstream CarSim Guide code."""
    return engine.search(query,limit)


@mcp.tool(annotations=READ)
def read_dataset(relative_path: str) -> dict:
    """Read a .par and its links inside the clone. Absolute external paths and traversal are refused."""
    return engine.dataset(relative_path)


@mcp.tool(annotations=WRITE)
def prepare_closed_loop(label: str = 'abs', overrides: dict[str,StrictFloat | StrictInt] | None = None, stop_time: StrictFloat = 2.0) -> dict:
    """Prepare a fresh ABS experiment. Overrides use registered native units: M_SU kg, H_CG_SU mm, IZZ_SU kg-m2. No simulation yet."""
    return engine.prepare(label,overrides,stop_time)


@mcp.tool(annotations=WRITE)
async def execute_closed_loop(experiment_id: str) -> dict:
    """Execute a prepared experiment through the configured official MATLAB MCP; manage only the license process we start; validate artifacts."""
    return await execute_prepared(engine,experiment_id)


@mcp.tool(annotations=WRITE)
async def run_closed_loop_workflow(label: str = 'abs', overrides: dict[str,StrictFloat | StrictInt] | None = None, stop_time: StrictFloat = 2.0) -> dict:
    """Full local workflow: initialize/reuse clone, prepare scoped parameter edits, run existing MATLAB through official MCP, validate and retain logs. Requires a shared running R2025b session."""
    return await run_closed_loop(engine,label,overrides,stop_time)


@mcp.tool(annotations=READ)
def experiment_status(experiment_id: str) -> dict:
    """Read experiment state, result and current validation without rerunning it."""
    return engine.status(experiment_id)


@mcp.tool(annotations=READ)
def audit_original_database() -> dict:
    """Hash every original database file against the pre-clone manifest. This can take a minute; it never edits or restores source files."""
    return engine.audit_original()


@mcp.tool(annotations=WRITE)
def validate_experiment(experiment_id: str) -> dict:
    """Recheck run hashes, finite time grids, port order, native termination and requested parameter echo."""
    return engine.validate(experiment_id)


@mcp.tool(annotations=WRITE)
def rollback_parameters(experiment_id: str) -> dict:
    """Restore only an experiment's parameter-copy backup; preserve every historical result; never edit the source database."""
    return engine.rollback(experiment_id)


if __name__ == '__main__':
    mcp.run()
