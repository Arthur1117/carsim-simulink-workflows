---
name: carsim-2021-simulink
description: Build, reproduce, run, and hand off CarSim 2021 / MATLAB R2025b co-simulations on Windows. Prefer Simulink-first staged development and verified native-solver coupling; attempt native CPAR delivery at closeout and provide detailed operating documentation. Supports dataset inspection, reviewed research integration and native archive delivery; includes an existing ABS automation preset.
---

# CarSim 2021 / Simulink workflow

Use the optional `carsim2021` MCP for supported data and experiment operations, and the official MATLAB MCP or installed application for MATLAB/Simulink work. This skill supports CarSim research integration beyond ABS, including the verified lane-keeping workflow. The local application and command fallback are in [local-workflow.md](references/local-workflow.md).

## Capability boundaries

This skill supports projects with different vehicles, controllers and scenarios. When using MCP, discover the tools and check `carsim_info`:

| Layer | Supported use and boundary |
|---|---|
| General CarSim MCP tools | Environment inspection, managed database initialization, dataset search/read and source auditing are not restricted to ABS dataset names. Respect each tool's managed-path and state constraints. |
| Existing automated experiment runner | `prepare_closed_loop`, `execute_closed_loop`, `run_closed_loop_workflow` and their experiment status/validation/rollback operate on the currently registered `abs_split_mu` preset. Its time, channel and override limits apply to that runner. |
| Reviewed research integration | CarSim MCP discovery/data tools, official MATLAB MCP, official native solver and scoped local/native operations have together supported FOISMC lane keeping, official-block comparison and CPAR delivery. Reuse that route for suitable new tasks with a verified task-specific contract; not every step is exposed as a CarSim MCP endpoint. |

A successful non-ABS task demonstrates an extensible integration workflow, not arbitrary-model compatibility or newly installed server endpoints. Do not require a server-code change merely to use an already reviewed native research route.

## Agree the delivery folder before building

For a new build/reproduction, establish the final deliverable folder with the user before creating substantial models and package dependencies. An explicit path in the request or an already agreed location counts as confirmation; reuse it without asking again. If missing, ask early with a concrete suggested full path and wait for that choice before committing the package layout; continue independent read-only discovery meanwhile. Do not silently choose Desktop or defer this choice to closeout.

Create and maintain staged user-facing deliverables under that agreed root where supported. Keep tool-required managed database/experiment paths in place; the folder agreement does not add an arbitrary output-path capability or authorize moving a registered service. See [staged-workflow.md](references/staged-workflow.md) for this distinction. A fixed agreed delivery folder is an organizational choice, not permission to hardcode that path: derive project paths from the package root and configure machine-specific installations separately.

## Route the task

For a new controller, research model, vehicle or scenario, read [staged-workflow.md](references/staged-workflow.md). Separate MATLAB/Simulink work, CarSim work and their interface, retain useful verified deliverables at each stage, and attempt a minimal real connection before growing the system. Existing MATLAB modeling/specification skills own their respective work; do not duplicate their procedures here. Simple reads and repeats of the verified ABS profile do not require a new multi-stage plan.

The tested order is **Simulink first, then CarSim native integration, then final packaging**. Perform essential read-only discovery early, build and retain the controller/interface stage, and then prepare CarSim data and real coupling. For new research work prefer the proven Simulink-to-official-solver route; a foreground Browser UI is not intrinsically required, but a usable solver license provider is. Check the actual cold-start dependency rather than assuming that no Browser process is needed: this installation required Browser to finish License Settings when no other provider was ready. Verify the official MEX/DLL, actual inputs, channel contract and fresh native outputs.

Preserve a working existing setup. A generic S-Function calling official `vs_sf` is an acceptable default. The official `Solver_SF` library block adds a parameter UI and library link and can be used when requested or helpful for learning/delivery. Do not replace a working block solely for its appearance. Operate Browser when explicitly requested or needed for native data/archive operations.

Read only the additional references relevant to the task:

- Research integration outside the bound ABS endpoint: [native-cosimulation.md](references/native-cosimulation.md).
- Final delivery or a CPAR request: [cpar-delivery.md](references/cpar-delivery.md). Attempt CPAR export after the main simulation workflow succeeds.
- Completed model/reproduction handoff: [delivery-documentation.md](references/delivery-documentation.md). Lead with click-by-click file/menu/button instructions for a fresh run and its result plots; put command/code alternatives after that usable route. Include detailed model explanations, modification points and final file locations.
- Complete study packaging, relocation or sharing: [portable-delivery.md](references/portable-delivery.md). Cover all promised cases/strategies and plots, ship their project dependencies, separate project paths from installation settings, and distinguish local, relocated and recipient-machine validation.
- Completed vehicle-study closeout or video/playback problems: [animation-playback.md](references/animation-playback.md). Check native recorded-result data, scene/resources, the actual Browser/player association and a representative playback; include the click route in the guide. Live streaming and movie export are separate capabilities.

These references describe the tested research route alongside the existing runner preset. Attribute each operation to its actual tool/native interface; documentation updates do not install new MCP endpoints. Recheck available tools if the service changes. A narrow read or accepted smoke-test repeat does not automatically require a full research package or lengthy report.

The user prefers visible modeling and simulation. Use a visible MATLAB session and show relevant models/plots when supported. Opening CarSim Browser, replaying animation and live solver-to-Visualizer animation are different operations; report which is actually available. The v1 runner currently closes its own model and rejects a preloaded model with the same name: opening it before `run_closed_loop_workflow` is not a working visibility switch. See the staged reference before arranging visible runs; do not claim that this instruction alone added GUI support.

## Registered ABS run sequence

1. Through official MATLAB MCP, verify release R2025b and win64, then evaluate `shareMATLABSession;`. This shares the currently running visible session without changing startup files. It is necessary after MATLAB restarts; the CarSim service deliberately connects in existing-session mode.
2. Call `carsim_info`. The supported execution route is Simulink with `solvers/Matlab84+`; CLI availability is independently false and does not invalidate this route.
3. Call `run_closed_loop_workflow(label, overrides, stop_time)` for the complete local ABS workflow. It initializes one full hash-verified database clone if needed, reuses it afterward, creates a fresh experiment, applies scoped overrides through upstream code, manages only its own license process, calls official MATLAB MCP, and validates results.
4. Report the experiment ID, validation outcome, requested-versus-echoed parameter values, signal validity, native warnings and output folder. `integrationPassed` does not mean `physicsValidated`. The installed ABS example currently emits table extrapolation warnings; keep them visible.

If preparing without execution is useful, use `prepare_closed_loop`, then `execute_closed_loop`. Each prepared experiment can execute once; never overwrite or rerun a completed or failed experiment. A failure retains its files and structured error; correct the cause and prepare a fresh experiment. For `MATLAB_SESSION_NOT_SHARED`, refresh sharing through official MATLAB MCP. For license errors, inspect the recorded error and use the installed legitimate license provider; never modify license files.

## Existing runner preset and parameter semantics

The existing automated experiment runner's registered profile is `abs_split_mu` / `Ext. ABS: Split Mu`. Stop time is 2–10 s; its interface is fixed at 4 wheel-cylinder pressure imports and 6 speed/master-pressure exports, with a 0.0005 s maximum step. These are endpoint limits, not limits for all CarSim research models. Do not silently route another vehicle, controller or research model into this profile.

Registered native-unit overrides:

| Keyword | Meaning | Unit |
|---|---|---|
| M_SU | Unladen sprung mass | kg |
| H_CG_SU | CG height of unladen sprung mass | mm |
| IZZ_SU | Yaw inertia of unladen sprung mass | kg-m2 |

Total vehicle mass is not M_SU. If the user's requested physical quantity is ambiguous, resolve it before changing anything. Convert explicit user units to the registered native units and report the conversion. Unsupported parameters must be discovered and deliberately registered from local dataset/echo evidence; never guess a keyword, table family, channel order or unit.

## Inspect, validate and roll back

- Use `search_datasets` and `read_dataset` for the cloned database. Reads and `.par` handling reuse reviewed upstream code; do not install the upstream server unrestricted against the source database.
- Use `experiment_status` for state/results and `validate_experiment` to recheck an executed experiment. Validation covers job hashes, exact channel order, finite strictly increasing aligned time grids, sample counts, fresh isolated artifacts, normal native termination and scalar echo.
- After a solver-block, interface or packaging change, compare preserved old/new time series under matched conditions and stated tolerances. Check time grids, units and effective controller configuration; do not infer equivalence from plots alone. Retain exploratory failures and separate accepted settings from paper assumptions.
- When startup/export fails, inspect logs, the selected clone and existing processes before retrying. Retry with new evidence or a relevant change; do not accumulate Browser/license-manager instances or discard unsaved user work.
- Use `rollback_parameters` only when the user requests rollback. It restores the experiment's parameter copy, retains historical results, and invalidates its current acceptance. It does not undo a historical run or write to the original database.
- Use `audit_original_database` for a full original-source hash audit when requested or during release acceptance. It is intentionally more expensive than normal per-run checks. Report Browser log/cache changes separately and preserve the original database.
- The configured original database remains outside every writable MCP path. Writes, simfiles, animator files and results stay in managed clones/experiments. Reject traversal and reparse points. Do not change source attributes/ACLs, MATLAB startup files or the installed solver binaries.

For models beyond this runner preset, inspect callbacks and dependencies, use the available building-simulink-models workflow, copy the model, and prepare a reviewed task-specific configuration through the native research route. Register a new server profile only if extending the automated runner is part of the task; existing native research integration does not depend on that extension. The service does not automate arbitrary GUI operations or promise arbitrary-model compatibility.

## Closeout

For a completed build/reproduction, preserve the runnable MATLAB/Simulink package first, then attempt native CPAR export and appropriate import/open verification. Deliver a detailed manual operating guide alongside the explanation. Start with the exact files to open, buttons/menus to click, prerequisite initialization, visible success checks and how to display/save the requested figures. Distinguish MATLAB editor Run, Simulink Run and CarSim Send to Simulink/Run Now. Explain fresh simulation versus plotting saved data, then provide model/parameter explanations, optional code commands, modification points, final paths and observed troubleshooting. Prefer the software’s normal menus and readable initialization code; do not add shortcuts or extra launch wrappers merely to conceal setup. Use the agreed final location throughout and verify a representative run there before calling the package runnable. If relocation is requested, regenerate paths and recheck the moved package; historical simfiles may contain obsolete absolute paths.

Before calling the final study complete, apply the coverage and dependency checks in [portable-delivery.md](references/portable-delivery.md): a working main-controller demo plus historical comparison images does not deliver rerunnable comparison experiments. For a sharing-ready claim, also perform the relevant relocation check; successful execution at the original destination alone does not establish portability.

For a completed vehicle co-simulation handoff, include recorded-result playback readiness and a representative playback check unless the user excludes it. Follow [animation-playback.md](references/animation-playback.md) to connect the actual native result to the delivered Browser/player entry, preserve numerical settings, and document watching/refreshing the video separately from running the simulation. Numerical success, playable animation, live streaming and exported video have separate acceptance statuses.

If optional CPAR work is blocked, deliver the verified core and report the packaging status precisely. If a working CPAR is a user requirement, it remains outstanding until verified or explicitly waived. Structural checks, native execution, CPAR import/open, final-location execution, physics validation and faithful paper reproduction are separate evidence levels.
