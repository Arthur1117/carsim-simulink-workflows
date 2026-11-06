# Staged CarSim–Simulink work on this computer

Read for a new joint simulation task, profile integration, or a request for staged/visible work. Keep an already verified small task short; use engineering judgment for the decomposition rather than prescribing a fixed number of steps.

## Establish a usable boundary early

Before substantial model building, confirm the final delivery folder using the rule in [SKILL.md](../SKILL.md), then perform essential read-only inspection of the existing setup, available signals and license/solver dependencies. An already specified or previously agreed folder needs no new question. Record that root in the existing task plan/configuration, with the deliverable and acceptance measures. When sharing or relocation is requested or already indicated, include it in the acceptance scope and use the path design in [portable-delivery.md](portable-delivery.md) from the start; no extra directory question is needed when the existing choice is clear. If the folder is still unanswered, continue independent discovery while leaving the package location undecided. This discovery does not require opening Browser or mutating CarSim data before Simulink construction. Distinguish controller behavior from vehicle-model accuracy.

Describe the MATLAB/Simulink work, CarSim work and connection work in a compact plan. The connection contract needs signal meaning/order, units, dimensions, sign/coordinate convention, sample times, actuator mode and initial conditions. If the user's existing model can satisfy the task, extend its copy rather than automatically substituting a new example.

Do not defer all CarSim discovery until after building a large controller. Use the smallest useful real CarSim connection early to expose interface, initialization and licensing issues. The deployed v1 automated experiment runner accepts its registered ABS preset; this does not restrict general MCP dataset tools or the verified native research route. For another research task, review its own configuration and contract and use that route; changing an ABS runner label does not change its model. Registering a new server profile is necessary only when extending that runner itself.

## Preferred staged outcomes

Follow the user's validated order: Simulink controller/interface first, CarSim native coupling second, full experiments third, archive/documentation last. These are useful outcomes, not compulsory approval meetings; continue within the existing authorization.

| Stage | Work and retained deliverables |
|---|---|
| Simulink | Saved controller/reference/interface model, initialization and parameters, dependencies, interface description, actual structural/algorithm checks. A labeled fixture or surrogate can help validate this stage independently. |
| Native coupling | Isolated native data/profile, PAR/SIM inputs, integrated SLX, minimal real feedback run, native echo/logs and channel/unit checks. Read [native-cosimulation.md](native-cosimulation.md). |
| Experiments | Requested cases with immutable inputs/configuration, raw time series and metrics, warnings/failures, comparisons and explicit source-paper deviations. |
| Handoff | Preserve the working package; attempt native CPAR export/import, verify a representative run and recorded playback at the final destination, and provide detailed operating documentation. Read [cpar-delivery.md](cpar-delivery.md), [animation-playback.md](animation-playback.md) and [delivery-documentation.md](delivery-documentation.md). |

Do not rebuild a completed controller or vehicle merely to package a CPAR. Do not postpone every useful deliverable until Browser/packaging succeeds. For a required artifact, report the outstanding requirement instead of declaring the whole task complete prematurely.

## Preserve useful intermediate work

Use the existing MATLAB specification and building skills when relevant. Build and check the controller/interface first when this permits independent verification. A simple surrogate plant or recorded data can help exercise signals, timing, saturation and error handling, but neither proves the closed-loop behavior of the real vehicle plant. Offline CarSim CSV is useful for replay/analysis; it does not replace bidirectional feedback during co-simulation.

Keep the surrogate/replay route explicitly distinguishable from the real CarSim route. Preserve the same interface when possible so the actual vehicle plant can be connected with minimal rework. Add complexity only after the preceding interface or behavior has been checked; extend one relevant module at a time when this makes failures easier to locate.

For a model-building task, retain the useful stage deliverables: saved .slx, required initialization/parameter files, interface information, executed checks and results. A drawn model, an update/compile pass, a surrogate simulation and an actual CarSim closed-loop run are different evidence levels. State the level reached. Do not create blank paperwork or claim an unexecuted model is runnable.

When replacing a block, regenerating parameters or changing packaging, compare the preserved baseline with new signals under matched conditions. Check shape, time grids, ordering, units and effective settings before calculating differences. State appropriate absolute/relative tolerances; exact zero difference is possible in deterministic local runs but is not a universal requirement. Newly added fields for an unused control branch should be explained rather than silently treated as a changed active controller.

If CarSim integration fails, preserve those deliverables and record the specific blocker, evidence, remaining file/GUI actions and how completion will be verified. Continue independent authorized work; retry only after a relevant change or new diagnostic evidence. Do not fabricate success, silently change the user's target or stop at a plan when other useful authorized implementation remains.

## Visible work

Prefer `open_system` for model work through the existing building skill so the user can observe edits in MATLAB. Use Scope/plots for signals when the model and execution route support them. Simulation pacing can help when a run finishes too quickly to observe; check R2025b/local help before configuring it and preserve the experiment's numerical settings.

The current `cs21_execute.m` v1 implementation runs through SimulationInput, rejects an already loaded `cs21_abs_smoke`, and closes its experiment model at cleanup. It has no tested visible-run/keep-open option. Do not pre-open that same model and then invoke the unchanged runner. A visible-run extension must handle model ownership, same-name conflicts and session restoration, and must be tested before it becomes the default. A saved model/results preview after a run is a separate viewing action and must not be described as watching execution.

CarSim Browser is the database/configuration GUI; merely opening it does not show Python parameter-file edits or a live solver run. Launching it can also update its selected database's logs/cache. Open a clone only through a locally verified database-selection method, identify the selected database, and leave the user's existing Browser/work untouched. Do not guess launch flags or fall back to the original database.

VS Visualizer supports output-file replay and a separate live-communication mode. Native recorded playback and Browser Video association were demonstrated in the local FOISMC delivery; this did not validate live animation or add a playback MCP endpoint. At vehicle-study closeout, use [animation-playback.md](animation-playback.md) to check the actual motion files, scene/resources and Browser/player association, observe representative playback and document the user's clicks. Keep live animation separately unverified until exercised. Show actual native windows on the user's desktop when available; never imply Codex is embedding or observing a native window if the current tools cannot do so.

## File management

Keep the agreed delivery root stable across controller construction, native integration, results and documentation. Resolve reusable project resources from the entry-point/package root and store portable experiment indexes as package/batch-relative paths. Generate required absolute SIM/output paths for each new run. Keep external installation paths in one documented local configuration or resolver rather than scattering them through runners and plotting scripts. Do not unnecessarily build a final package elsewhere and then move it at closeout. Retain stage deliverables within this root where the tools support it.

Reuse the managed database clone and runtime. Use independent experiment IDs; keep successful results, failure evidence and rollback backups. Do not create a new full database copy per module or per run.

A separate clone for isolated CPAR import verification is justified when needed; reuse it across the cases being verified. Startup/export failures require inspection of logs, database selection and owned processes before another attempt. Repeated blind launches can create duplicate-write and license conflicts.

The existing v1 runner still executes in its managed experiment directory; archive its verified artifacts into the agreed delivery root, subject to filesystem permissions. Do not claim v1 has an arbitrary runtime-output-directory parameter. A destination choice does not authorize overwriting user files or moving the registered service. In the native research route, use the agreed root for reusable models/code and task-owned runs where supported, while keeping isolated native databases where needed.

Verify a representative end-to-end run from the actual final package path, with runtime paths regenerated there. Choosing the root early prevents avoidable relocation; it does not eliminate this final-path acceptance check. If the user later requests a move, update active references and repeat the affected path-dependent checks, preserving historical run inputs as provenance. Absolute paths in an old simfile do not become portable just because files were copied.

## Completion report

Summarize completed MATLAB work, completed CarSim work and the actual integration evidence. Link the useful deliverables and report remaining actions precisely if the requested joint workflow is incomplete. Keep interface/integration acceptance separate from physics/controller validation; these require task-specific evidence. Identify whether the complete requested case/controller/figure coverage was delivered and whether relocation or another-computer use was actually tested. Consult [portable-delivery.md](portable-delivery.md) before describing the study as complete or shareable.

For a completed research/build delivery, this concise status accompanies the detailed guide in [delivery-documentation.md](delivery-documentation.md). Include manual user operations and modification points, source/assumption explanations, important file locations, actual test scope and limitations. Do not replace the guide with a list of tool calls or file names.
