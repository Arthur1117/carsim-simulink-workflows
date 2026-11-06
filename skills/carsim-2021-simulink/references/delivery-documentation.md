# Detailed explanatory and operating handoff

Read when handing off a completed CarSim model, reproduction or substantial new integration. The user wants both an efficient starting point and enough explanation to inspect, operate and modify the work themselves. For small reads or a single bounded diagnostic, scale documentation to the actual task rather than generating a full manual.

## Package and entry points

Keep a short quick start and a detailed guide in the delivery folder. Match the user's language and terminology. Markdown is sufficient unless another format was requested; use the relevant document skill for Word/PDF/etc. The guide should explain the system and actual user actions, not merely recount tool calls.

Use the final folder agreed at task start; an existing explicit destination is sufficient confirmation. If none is known, ask before substantial package construction rather than choosing one at closeout. Keep the deliverable layout stable there throughout the stages where supported. Tool-required managed experiments/clones remain in their supported locations and are archived into the agreed folder; do not move a registered service or original database to make the paths match. Do not make Desktop a universal default or overwrite unrelated files.

Provide a normal manual-use route as well as any automated runner. Start with opening the installed software and the correct delivered files through their usual UI, then explain the necessary preparation. Do not create shortcuts or additional launch wrappers merely to make the user dependent on a new entry point. A small readable initialization function is useful when the model needs real workspace/configuration setup; explain what it changes and how to inspect it.

A practical package may contain models, initialization/parameters, source, run inputs, optional native archives, results, verification evidence and documentation. Choose its structure to suit the task. Keep required dependencies identifiable; separate historical run inputs from a reusable launch script. Apply [portable-delivery.md](portable-delivery.md) for complete case/controller/figure coverage, dependency closure, machine configuration and relocation checks. These are part of the executable handoff, not merely additional prose in the guide.

## Start with a complete mouse-operated route

The user's preferred handoff teaches **which file to open and which button to click**, without requiring them to type MATLAB commands. Begin the guide with a short click-by-click route from normal software startup to one fresh successful run **and the requested result figures**. Put the detailed engineering explanation next and command/code alternatives afterward as reference. Do not treat a command snippet or a list of filenames as the manual-use guide.

For each meaningful step identify the application/window, actual folder and filename, menu/button label, resulting view and visible success condition. State whether the user selects a folder, imports an archive, double-clicks a script, or opens a model. Use labels matching the tested installation; bilingual UI labels help when appropriate. Include a real annotated screenshot if it materially clarifies an ambiguous control, but never invent a screenshot or report an API operation as a witnessed click.

Make potentially confusing controls explicit:

- **MATLAB editor Run** executes the selected script; **Simulink Run** executes the loaded model and needs its initialization first. Explain that seeing code after double-clicking a script is normal and does not mean the user needs to edit it. If the script already opens and runs the model, say that no second model Run click is needed.
- State whether this delivery actually uses **CarSim Send to Simulink** or **Run Now**, or the MATLAB entry script. Opening a database/model alone does not initialize the custom controller. Distinguish the active package model from a same-name archive copy; explain how to handle preloaded models and unsaved personal edits.
- Give normal file-opening/path-prompt choices such as **Open**, **Change Folder** or the version's equivalent when applicable. A function needing input arguments is not automatically an editor-Run entry point. Prefer the existing tested script/UI route; document an unavoidable command prerequisite honestly rather than pretending the full route uses only clicks.
- After a failed run, stop the procedure at the error and retain the actual message. Do not proceed to a latest-results viewer and present an older successful result as the failed run's output.

For a requested multi-controller or multi-case study, the primary route should run the complete promised comparison and produce its figures from that new batch. Also explain individual strategies/cases when useful for learning. Keep a separate replot-only route and identify it as reading saved data. Do not document only the main-controller example while leaving the comparison experiments in an undeclared research directory.

The quick route should give the user one clear starting workflow. Explain additional workflows separately instead of interleaving alternatives at every step. Preserve normal software operations and readable initialization; do not add shortcuts or wrapper layers just to hide the setup.

## Contents the detailed guide should cover

### 1. Purpose, provenance and fidelity

Explain what was built, the control/plant architecture, signal flow and why CarSim and Simulink exchange those signals. Identify the actual vehicle, data/model origins, controller nominal parameters and reference trajectory. For paper work, map main equations or algorithm steps to implemented functions/blocks, and identify unavailable source details and reconstructed assumptions.

Explain controller timing, fractional/discrete approximations where relevant, initialization, units/sign conventions, delays, actuator constraints, disturbances and metric windows. Separate the paper's settings from changes made for this reconstruction. Do not use a smaller numerical error as proof of a more faithful or better controller when the vehicle/path/baselines differ.

### 2. Environment and exact file locations

State tested software versions/architecture, necessary products and legitimate license-provider dependency. Distinguish integration evidence from the vendor's supported-release list.

Provide a table with each important artifact's **purpose, actual final absolute path, package-relative path, and whether the user should run/edit/inspect it**. Include at least the applicable:

- Main SLX, controller source, initialization/configuration and reference/disturbance code.
- Reusable startup/runner and runtime input templates.
- CPAR files, their Run Control category/titles, model links and import instructions.
- Actual native parameters, SIM interface files, echo/logs and generated results.
- Main plots/data, acceptance/comparison report and hash manifest.
- Playback configuration/entries, corresponding native motion files and scene/resources, source records and the installed Visualizer location when animation is part of the handoff.

Use verified existing paths in the completed guide, not placeholders or remembered scratch addresses. Present package-relative paths as the reusable navigation and the current absolute root as a convenience for this user. A recipient should be able to substitute their chosen root once, rather than edit many instructions. Identify machine-specific installation paths separately and show the single supported way to configure/select them; do not imply that the current machine's CarSim drive letter is universal. Where helpful, label a historical path as provenance rather than an active dependency. Follow the host's link restrictions; use allowed clickable artifact links and plain absolute paths where a clickable link is inappropriate.

### 3. Quick automatic run

Give the exact entry point and explain how to reach it through file selection, double-click and the correct editor/window Run button. State which default case it selects, its simulation duration versus actual waiting time, where fresh outputs appear and the visible completion message or status. Explain whether it needs Browser open, a native test database, workspace initialization or a running license provider. A startup script should resolve needed library paths before opening linked models and generate current SIM/output paths instead of reusing historical absolute paths.

Explain how to select other supported cases and what evidence confirms successful completion. Do not label a script one-click runnable if it requires undocumented `job.json`, preexisting global variables or temporary directories. If such setup is intentional, describe it explicitly.

### 4. Getting the result figures

Treat figure generation as an explicit handoff step, not an implied consequence of running a model. Explain which figures open automatically and which require a separate plotting action. For the separate action, give the actual plotting file's folder/name and the exact editor Run or UI control; identify Figure windows/tabs and how to find exported images using normal file browsing.

For each requested figure or coherent figure group, identify the producing entry point, required input data/index files, cases/controllers covered, whether it runs a new simulation or reads saved results, expected figure content/units, and actual saved PNG/FIG/PDF location as applicable. Show the successful-run-to-plot order and how to associate a figure with its run folder/case/configuration. Do not claim that a single-case preview recreates the paper/report's entire batch or all controller comparisons.

If a latest-successful-run viewer is provided, explain its selection rule and that it can display historical data. A manual Simulink run may not create the runner's result index or CSVs; explain how its outputs must be saved/plotted instead of directing it blindly to that viewer.

Check that documented plotting entry points can find their actual dependencies at the final paths. A copied plot function without its selected-run index, CSVs or helper files is not a working plotting delivery. For a complete delivery, collect the required project-side plotting data and helpers under the agreed package root and fix active indexes/paths. If a separate research-directory dependency remains blocked or outside the agreed scope, identify it as an outstanding dependency and limit the completion claim; do not present its path as a substitute for delivering a self-contained study. External installed software remains a separately documented prerequisite. Distinguish opening existing images, replotting historical raw data, and rerunning the underlying experiments.

### Watching the native animation

For completed vehicle-study handoffs, include the recorded-playback route and its acceptance status unless excluded by the user. Apply [animation-playback.md](animation-playback.md) for data association and verification. Explain that native motion files need scene/camera/resource configuration and are not already an encoded MP4/AVI. CPAR import, successful simulation and playable animation are different checks.

Give a complete mouse-operated route: open the delivered database, select its actual Run Control category and case, click **Video** or **Video + Plot**, then use the official player's play/pause button and time slider. If other strategies use separate playback entries, give **VS Visualizer -> File -> Open** and each applicable case/controller filename. Map those entries to their actual run/source record; do not imply one controller's Browser dataset selects all algorithms. Explain how to identify the current run if the window title retains a shared scenario name.

Document new simulation followed by playback, any automatic result publication, and the tested way to refresh/reopen an existing player. Identify a saved-data refresh script as a postprocessing action, not a new vehicle run. Include the playback files' locations and observed fixes for missing/grey Video, stale results or missing resources. State if example scenery/cones differ from an external controller's reference trajectory. Describe live animation or movie export only when separately supported and tested; ordinary playback does not require either.

### 5. Manual operation and learning

Give step-by-step instructions for the actions actually applicable to the delivered system:

- Open MATLAB, set its current folder, distinguish scripts to run, functions to call with arguments, source to inspect and SLX models to open. Lead with the tested clickable initialization script or UI when available; provide exact command alternatives afterward. State case selection, working folder, stop time and Normal/other tested mode before the user presses Simulink Run. Identify the controller/adapters/CarSim block. Check the saved SLX stop time instead of assuming it equals the full case duration. Explain temporary in-memory configuration, unsaved edits and manual result saving when those differ from the automated runner.
- Explain how the model is actually built: identify graphical subsystems with internal block diagrams, MATLAB Function/Level-2 S-Function algorithm blocks with source files, and compiled native solver blocks. Map important block names to their actual implementation and tell the user how to inspect the diagram, parameters or source. Do not imply that a code-based algorithm has an undisclosed graphical subsystem. Inspect the solver block's `FunctionName`, actual MEX/DLL, library link and parameters; explain generic S-Function versus official library UI if relevant.
- Explain **File → Open Existing Database** for an already prepared database separately from **File → Import Parsfile (Any Export Type)** for a CPAR file. Identify the correct database root, Run Control category/title, vehicle, Procedure, VS Commands and Models link. Describe import completion, category changes and duplicate/locked items when relevant. Explain any base Procedure labels superseded by explicit native overrides.
- Locate fresh results, plot/log signals and native echo, and inspect parameters actually used.
- Describe Browser **Send to Simulink**, **Run Now**, animation replay or live animation only to the extent tested. If the provided MATLAB runner is the verified entry point, say so instead of implying Browser handles all initialization automatically.

Clearly distinguish tested instructions from version-dependent guidance that was not exercised. Native API import is not an observed GUI-menu import; executing prepared settings with `sim(in)` is not an observed click on the green Run button. Cite the installed manual for menu guidance and identify the execution route actually tested. Do not document untested GUI steps as successful operations.

For this local installation, include these points when relevant:

- Start the installed CarSim program with its installation directory as the working directory. A task-created launch with the database as working directory caused **LoadPanel -94**, looking for `sgui_lib/all_panels.uir` under the database. The installed resource existed; correcting the working directory fixed startup. Do not copy the EXE/resources into the database as a presumed repair.
- Complete the existing legitimate **License Settings** configuration and enter the main interface before relying on Browser as the solver license provider. A running process still blocked at that dialog did not satisfy the cold-start runs.
- A Run Control titled **No Data** can be the selected empty starter dataset. Check the active database, actual import completion and selected category/title before diagnosing an empty/corrupt CPAR. Do not guess which user click failed from incomplete logs.

### 6. How the user changes the experiment

Map common requested edits to real controls/files: speed, friction, initial state, controller gains, reference path, wind/disturbance, sample times, actuator limits and output signals. Explain whether each change belongs to Simulink/MATLAB, native CarSim data, or both. Describe the required regeneration, new run folder and verification after an edit.

Explain which values are controller nominal quantities versus actual plant values. Use native units and show conversions where ambiguity is likely; total mass is not unladen sprung mass. Do not imply modifying a MATLAB variable necessarily changes the native vehicle. Avoid adding unnecessary script layers solely to create extra edit locations.

### 7. Evidence and limitations

Provide the actual cases, output metrics and coverage; identify raw data/log locations. State structural/native-run/CPAR/final-location and recorded-playback acceptance separately from physics validation and strict paper replication. Identify the cases/strategies visually inspected, any broader playback-input checks, and whether a Browser click was observed or confirmed by the user. Compare against preserved old results when an interface/block/package changed, with time alignment, signal definitions and tolerances.

Report failures, warnings, extrapolation, actuator saturation and important unsupported actions. Do not silently omit unsuccessful exploratory branches. If configuration structure differs only through unused branch fields, explain this and identify the effective settings checked.

### 8. Troubleshooting and reproducibility

Include observed, actionable failures and how to diagnose them: missing MEX/library, stale SIM paths, wrong working folder, absent initialization, wrong port count/units, same-name loaded model, database already open/locked, license/startup problems, and native export issues. Keep version-specific details in scope. State how to retain old runs and reproduce a case in a new folder.

Before handoff, check that a reader can follow the written route from the final location through initialization, a representative completed run, figure display and saved output retrieval. Execute the numerical/plotting checks appropriate to the task and record the actual method used; an API check is not evidence that every GUI click was exercised. For a copied package, validate a representative case from that location and record its actual output folder. For a portable/shareable delivery, follow [portable-delivery.md](portable-delivery.md) to test a renamed or relocated isolated copy, its saved-data plotting and its fresh native run. State when only the original machine/destination was tested; do not equate this with another-machine acceptance. Hash-check deliverables where useful. Do not regenerate hashes/metadata in a way that erases historical result provenance or overstates portability to a different machine.

## Completion message

Tell the user where the final folder is, the file to open, the button/menu to click, how to display the result figures and watch the native recording, what passed and any material remaining limitation. Default to mouse-operation language rather than pasting command blocks unless the user asks for code. Link the detailed guide. Keep that final message short because the explanation and manual operations live in the delivered document; do not make the user reconstruct instructions from collapsed progress updates.
