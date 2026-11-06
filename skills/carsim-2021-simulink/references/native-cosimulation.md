# Native research co-simulation

Read for a research controller, vehicle or interface beyond the existing ABS runner preset. This verified route combines general CarSim MCP discovery/data tools, official MATLAB MCP and scoped native/local operations; it supports non-ABS work without requiring new server endpoints. It supplements [staged-workflow.md](staged-workflow.md).

## Select a real execution route

The tested local combination is CarSim 2021.0, MATLAB R2025b win64, installed `Programs/solvers/Matlab84+/vs_sf.mexw64`, and `Programs/solvers/carsim_64.dll`. Discover current paths and resolve the actual function/library in MATLAB; do not assume another machine's simfile, an example's `solvers/Matlab` directory or a CLI executable is usable. Local integration evidence is not a vendor support statement for R2025b.

Simulink can call the official solver while Browser is closed. This is real co-simulation when native provenance and live bidirectional feedback are verified. Inspect `FunctionName`, resolved MEX/DLL, actual input files and native results. A generic block name/icon is not evidence either way. Replay of exported CSV is not native closed-loop execution.

Installed `Solver_SF/CarSim S-Function` uses `vs_sf` with a mask and library link. Preserve the user's working form. If replacing it with the library block, inspect available mask values/callbacks rather than inventing parameters. In the local 2021 block, `StopMode_ind` accepts `External` / `Vehicle Model`, not `Off` / `On`; its parameter callback and initialization text differed. Preserve effective stop behavior and validate by running. Do not rewrite installed library code to hide the discrepancy.

## Keep the profile explicit

For a research route, review and record its own contract and preparation/validation code before running. Use supported CarSim MCP discovery/data tools and official MATLAB MCP, adding scoped native/local operations where needed. Preserve the working ABS runner preset rather than relabeling it or bypassing its model/hash checks. A reviewed native research configuration can execute independently of that runner; add a server profile only when runner generalization is explicitly in scope.

Retain a machine-readable job/configuration record containing:

- Actual source dataset identity/location and source/input/model hashes.
- Vehicle parameters/data origin, separate from controller nominal parameters.
- Import/export names in exact order, units/dimensions, external-control and driver modes.
- Solver/controller sample times, delays/holds, initialization and stop criteria.
- Requested native overrides, application/precedence, and subsequent echoed values.
- Dependencies, official solver paths, independent output directory and validation status.

The FOISMC steering/wind contract from 2026-10-21 is evidence, not the default interface for other tasks. Discover each new contract from actual data/docs.

## Input preparation and execution

Prepare controller/interface artifacts first, then native PAR/SIM inputs and the integrated model. Use native datasets/expanded parameters from the managed clone. Check a purported self-contained expanded input for remaining `PARSFILE` references and file-based tables; resolve required dependencies. Avoid blind substitutions, duplicate import/export declarations and guessed units.

Check actual override precedence in generated input and solver echo. A Procedure title can retain a base speed while later VS Commands deliberately override it; explain this in the user guide. A research runner may bind an official DLL and explicit port sizes in a run-specific SIM file only from its reviewed profile. Use SimulationInput for per-run overrides.

Each execution gets a new folder. Save source/configuration snapshots, raw outputs and logs. Preserve failures and material deviations from the source paper. Do not silently change a controller, vehicle or path to obtain a successful run.

## Acceptance and regression

Check native termination and observed stop time, finite data, dimensions/order, monotonic aligned time vectors, actual echoed parameters, and intended control/disturbance response. Account for native initialization samples and observed solver-step stop offsets. Preserve extrapolation and other native notices.

After a module/interface/packaging change, compare old/new plant outputs, actuator inputs, controller errors/reference and relevant internal terms. State tolerances by signal where needed and compare effective configuration. Added parameters/weight columns for an unused branch do not automatically imply the active controller changed: verify which fields and columns it uses, and record the raw metadata differences.

Use matched metric windows/definitions for paper comparisons. Matching two implementations supports their numerical consistency but cannot establish physical truth if both use the same inaccurate assumptions.

The 2026-10-21 FOISMC study established exact time-series equality for four accepted w=12 m cases between the initial direct S-Function route and the CPAR-imported official-library route. It did not establish universal wrapper equivalence, validate the paper's original vehicle or newly replay every other controller branch. See [local-environment.md](local-environment.md) for evidence locations.
