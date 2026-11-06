# Complete and portable CarSim study delivery

Read for a completed multi-case/controller study, a request for a complete package, relocation, or sharing with another person. This extends the existing Simulink-first workflow; it does not require rebuilding a verified controller/vehicle or expanding a narrow diagnostic into a full product.

## Plan the package before substantial construction

Use the final folder agreed at task start under [SKILL.md](../SKILL.md). An explicit existing location already counts as confirmation. Work there for reusable project artifacts where supported, retaining tool-required managed databases/experiments in their supported locations. Agreeing a folder avoids repeated staging moves; it does not make that absolute path part of the algorithm.

When the user intends to share the deliverable, design for that use immediately. Record the intended software/version/platform prerequisites and remaining local settings in the existing configuration/guide. Do not move the registered MCP service, assume Desktop as a universal destination, or create a new full database clone for every case.

## Deliver the complete requested experiment

Use an existing result index or a compact table to map **reported result/figure → case and controller → fresh-run entry → plotting entry → required data/configuration → saved output and acceptance evidence**. Match the user's actual scope; a particular twelve-run study is an example, not a universal experiment count.

For every algorithm/scenario promised in the comparison, deliver its implementation, effective parameters, initialization, runnable model/native inputs and the practical way to select/run it. A plot generated from historical data is useful evidence, but does not replace the ability to rerun the underlying experiments. Label missing author implementations as reconstructed baselines, and retain tuning/fidelity limitations.

For a complete comparison, provide one clear supported route to run all required combinations and automatically plot that new batch; provide individual-strategy/case operation when it materially helps the user. Reuse shared execution/plot functions rather than copy algorithm logic into separate wrappers. Keep a replot-only route for completed data. A batch's plots/index should point to that batch's own successful runs, with sufficient status to reject incomplete coverage or to label it explicitly. Never fill missing curves with unrelated older results merely to finish a graph.

Keep project-side dependencies under the deliverable root: code/helpers, models/libraries the project owns, input data/tables/dictionaries, controller presets, native input templates, plotting indexes, required raw results, playback entries and their motion/scene dependencies, numerical/reference checks, archives, documentation and verification records as applicable. Follow references and indirect file loads; a copied plotting function without its run index/CSVs is not complete. A justified external prerequisite must be declared; an unexplained scratch/research directory is a delivery gap.

When delivering animation, follow [animation-playback.md](animation-playback.md): associate each promised recording with its case/controller and source run, retain both native motion files and the required scene/resources, and distinguish an installation prerequisite from an omitted project asset. Regenerate active player/Browser result links for the current location rather than rewriting historical evidence. Include representative recorded playback in relocation checks when animation portability is claimed; a playable recording at the old path is insufficient. CPAR alone does not include every completed result or guarantee that the recipient's Video button can find it.

## Separate three kinds of paths

| Path class | Required treatment |
|---|---|
| Project assets and result indexes | Derive the root from the entry script/function location, not the user's name, Desktop, the agent workspace, a fixed drive letter or an incidental current folder. In MATLAB use `mfilename('fullpath')`, `fileparts` and `fullfile` as appropriate. Store cross-file indexes and project links relative to their package/batch/database base, with that base unambiguous. |
| External installations and local runtime settings | Keep the supported CarSim installation, solver/MEX/library selection and other machine-dependent settings in one documented local configuration/resolver. A detected or known local installation can be a default, not a universal mandatory path. Permit an explicit override or normal file/folder selection when needed, validate it and give an actionable missing-dependency message. Use MATLAB's own installation root where appropriate. |
| Per-run native absolute paths and historical provenance | Generate native PAR/SIM/DLL/resource/output paths for the current run and current machine. A native tool may require absolute paths; that is compatible with a relocatable package when regenerated. Preserve historical SIM/echo/log/job files and their original paths as immutable evidence; do not mass-rewrite them or present them as reusable startup inputs. |

Apply the same distinction to model callbacks, library links, included files, configuration MAT/JSON, plotting indexes, saved-data readers and documentation. Review active dependencies for obsolete absolute paths; a string search alone cannot distinguish harmless provenance from a live file reference. Do not claim portability just because the top-level script uses relative paths while a helper still hardcodes the old project root.

Keep Browser's startup working directory at the installed CarSim location when required by this local CVI version. Select the database separately. MATLAB may need a run directory for `simfile.sim`; derive it explicitly and restore the caller's directory when appropriate. Do not confuse these working directories with the agreed deliverable folder.

The recipient supplies compatible installed MATLAB/Simulink/CarSim and a usable legitimate license provider. Do not claim the package includes vendor installations/licenses or depends on the author's logged-in MATLAB workspace, agent-only helper process, undeclared global variables or Codex/MCP server. A standalone handoff should initialize its own state through its documented entry point. If MCP is actually required, declare and deliver its required setup within the authorized scope rather than calling it standalone.

## Validate the claim at the right level

1. **Coverage and dependencies:** Verify all promised cases/controllers/figures have their files and usable routes. Check the active code/model/data dependencies and current configuration. Record hashes where useful without replacing historical provenance. Default settings should resolve the current machine; report remaining local prerequisites.
2. **Final folder execution:** Run the actual delivered entry point from the agreed root through fresh native completion and plotting. Validate case/controller labels, timing, units, effective parameters and normal outputs. Match the validation to the claimed coverage, including non-main-controller branches. Do not use historical replot success to certify fresh-run execution.
3. **Relocation:** For a portable/shareable claim, use a separate copy under a different parent and package name. Never move, rename or disable the user's original as a test. Exclude or isolate original project paths in the test session without resetting MATLAB's entire path or breaking MCP. Confirm loaded model/helper/data paths resolve to the copy; replot saved data there and execute a representative new native case with regenerated paths. Check outputs are written under the copy and compare matched results with stated tolerances. Include native archive import/regeneration at the new location if claiming that capability. Exercise spaces/non-ASCII paths when those are part of intended supported usage; otherwise state the tested range and known short-path limitations.
4. **Recipient-machine use:** Same-computer relocation does not test a different MATLAB/CarSim version, architecture, installation drive or license environment. If no recipient environment is available, describe the package as relocation-tested on the stated machine and provide installation/configuration instructions; do not claim another-machine validation occurred.

Keep tests proportional: packaging checks and fresh runs should resolve actual coverage/path uncertainties, not blindly repeat every experiment after a prose edit. If a portability check fails, preserve the working original package, diagnose the active reference, fix the reusable path/configuration and repeat the affected check. Do not alter controller gains or vehicle physics to disguise a packaging failure.

## Make the shared package understandable

Use [delivery-documentation.md](delivery-documentation.md): mouse-operated steps first, then model/parameter/source explanations and optional commands. Provide package-relative navigation plus the current absolute root for convenience; explain how a recipient selects their own installation once. Document full-study execution, individual algorithms, replot-only operation, output files, curve provenance, dependencies, verification levels and known limitations.

Update the existing primary guide and quick start so they describe the actual final files. Avoid accumulating conflicting "final" manuals; preserve replaced versions as history/backups and identify the current guide if a locked document requires a temporary alternate filename. Keep original failed experiments and provenance; a sharing subset may omit caches or redundant backups only when those are not required inputs/evidence and the authorized sharing scope permits it. Do not delete the user's historical results as routine cleanup.

Before declaring completion, the runnable package, figures/data, playback entries, documentation and validation record must agree about case/controller coverage, active paths, baseline origins and which actions were actually tested. Distinguish opening existing images, replotting saved runs, fresh co-simulation, recorded playback, CPAR import, relocation, recipient-machine use and physics/paper validation. Live streaming and exported video require their own evidence if claimed.
