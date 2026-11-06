# Native animation playback at handoff

Read for a completed vehicle co-simulation delivery, a request to watch CarSim results, a grey Video button, or missing/stale playback. Keep the verified Simulink-first numerical workflow; ordinary replay does not require replacing its solver block or enabling live streaming. Scale checks to the actual task, rather than requiring animation for every read or diagnostic.

## Distinguish the deliverables

Native output such as `.vs` metadata with its `.vsb` motion data (or the version's `.erd`/`.bin` pair) can already exist even when Browser cannot play the run. These are recorded numerical results, not an encoded MP4/AVI. VS Visualizer also needs the scene/vehicle shapes, camera, resource search paths and a configuration linking them to that run. `animator.par` is a typical entry point. CPAR import alone does not supply every completed experiment's motion results.

Recorded-result playback, live solver-to-Visualizer communication and exported video are separate capabilities. Prefer recorded playback for normal closeout unless the user asks otherwise. Do not enable a different S-function, add a streaming/license dependency or export a movie merely to repair an ordinary playback link. Report exactly which capability was tested. Successful playback supports result accessibility; it does not establish physical calibration or strict paper replication.

## Associate the actual run

- Trace **case/controller and successful run -> native data pair -> scene/camera/resources -> playback entry -> Browser result selection**. Inspect actual outputs and the installed version's Visualizer/Run Control documentation. Empty or missing animation channels, resources, incomplete output and an incorrect result link require different fixes; do not assume every missing video is only a path problem.
- A native research runner often writes into isolated experiment folders while Browser's Video button searches its own database `Results/Run_<dataset ID>` folder. In the tested 2021 database, latest results use `LastRun.vs/.vsb` and the corresponding all.par. Discover the current dataset IDs, cache/output naming and destination instead of copying case-specific UUIDs. Existence of a SIM `ANIFILE` entry does not prove its target was generated or linked.
- Generate the missing playback configuration or publish documented derived result copies into the matching **delivered/test database**, with a source record. Verify the selected case/controller and preserve original logs/data. Never publish another controller's motion under an FOISMC-labelled Browser entry or mix runs to fill a missing result. Distinct algorithm playback entries can share a vehicle scene while retaining their own motion sources.
- Where useful, make successful new runs refresh their playback entry automatically, with a separate saved-data refresh route. Do not launch many players during a batch. Report playback-preparation failure separately from numerical success; preserve both statuses rather than silently showing an older video. Refreshing a file does not refresh an already open player's cached data.

## Verify playback separately from solver execution

For a completed vehicle-study handoff, include native recorded-playback readiness and a representative playback check unless the user has excluded it. If it is required and remains blocked, keep it outstanding while preserving the verified numerical deliverables.

1. **Inputs and coverage:** Check the motion pair, associated scene/configuration and resources for each promised playback entry. Record case/controller/run identity and available duration. A file-format or hash check alone is not a playback test. Representative visual inspection plus broader dependency checks must not be reported as observing every recording.
2. **Actual viewing route:** Open the final-location entry in official VS Visualizer. When delivering the Browser Video route, also verify its selected dataset/result association. Observe a rendered vehicle and advancing time/changed pose, and exercise playback/seek as applicable. Distinguish an agent-observed action, explicit user confirmation and a check not performed. Opening a blank player or merely generating `animator.par` is insufficient.
3. **Fresh-run continuity:** If a runner's postprocessing or Browser publication changed, verify a representative fresh native run updates its own playback source. Compare matched old/new numerical signals and effective settings using appropriate tolerances when the execution path changed. Keep controller, vehicle and solver configuration intact for a linkage repair. Exact equality occurred in the local case but is not a universal threshold.
4. **Usability and relocation:** Explain whether the user must reselect the case, reopen Video or use File -> Reload data after a new run. Apply [portable-delivery.md](portable-delivery.md) to regenerate active playback paths and test resources after relocation. Copied CPAR/SLX or one working absolute path does not certify a shareable animation package.

Retain enough provenance to identify the data behind the visible vehicle. Native Run Control titles can describe a shared scenario rather than the selected MATLAB algorithm. Example scenery, cones or the Browser's target-path graphic may differ from an external controller's reference trajectory; label that distinction and do not present scenery as evidence of the controller's path. Correct a misleading visual overlay when it is in scope without altering numerical inputs to make the video look better.

## Guide and completion status

Use [delivery-documentation.md](delivery-documentation.md). Give the actual database/category/case, **Video / Video + Plot**, play/pause/seek controls, and the File -> Open route with exact case/controller playback filenames where needed. Include fresh simulation followed by playback, refresh-only operation, output locations, source records and installation prerequisites. Keep optional commands after the usable click route. Separate running from watching, and a recorded animation from live video or an exported movie.

In the 2026-10-23 FOISMC case, isolated `.vs/.vsb` results already existed. Linking scene/resources and publishing corresponding Browser results repaired playback. Native motion was observed in Visualizer, the user confirmed Browser Video, and a fresh C4 run retained exact equality in four log groups. Twelve entries had input/coverage checks; this was not a claim of visually testing every case/strategy, live streaming or another computer.
