# Native CPAR closeout

Read for a completed CarSim model/reproduction handoff or an explicit archive request. Preserve the successful Simulink/native workflow, then attempt the archive. Export is a delivery stage, not a prerequisite for every simulation. If optional packaging is blocked, retain the verified core and explain the status; a required working CPAR remains outstanding until verified or waived.

## Archive the actual experiment

An edited expanded `Run_all.par` does not automatically update Browser datasets. Before export, register isolated dataset copies/links that reproduce the accepted vehicle, scenario, native overrides, ordered I/O and model dependencies. Do not export an unchanged stock example and imply it represents the custom controller/scenario. Confirm source identities and actual generated settings rather than relying on Procedure titles.

Use a native export capability if the connected plugin supports it. Otherwise the installed 2021 Browser COM interface is a verified fallback. Consult the installed VehicleSim COM/Browser manuals for the current version. Do not rename a PAR/ZIP or manually change a container and call it a native-exported CPAR.

Collect the SLX and required MATLAB code, data, dictionaries, tables and other dependencies. Native export includes linked supporting files inside the database; indirectly referenced `.m` files are not automatically guaranteed. Stage such files in the clone and use documented `*CPAR_INCLUDE` entries where appropriate, or bundle them explicitly with the archive. Check what actually arrived in the CPAR. Avoid absolute links to transient work folders. Treat the archive as one part of the full study: four scenario archives, for example, can share a MATLAB controller-selection layer, but importing an archive does not itself select all algorithms or deliver comparison-run initialization. See [portable-delivery.md](portable-delivery.md) for the package dependency and path rules.

## Local 2021 COM mechanics

These are observed compatibility details for this installation, not universal instructions for newer versions:

- COM is registered as 32-bit `CarSim.Application`. Use a matching 32-bit client; the tested Windows script host is `C:/Windows/SysWOW64/cscript.exe`. A 64-bit client can report class-not-registered despite a working Browser.
- The tested startup form is `CarSim.exe -p "<managed-clone>" /Automation`, with `-p` first, **launched with the CarSim installation directory as working directory**. Using the database root as working directory caused LoadPanel -94 while resolving the relative `sgui_lib/all_panels.uir` UI resource; this did not indicate missing CPAR data. Inspect running instances before starting one. Allow initialization and inspect logs rather than continually creating COM objects/Browser processes.
- Read `GetDatabaseFolder` through its ByRef VARIANT output and verify the resolved folder is the intended writable clone before any mutation. Several getters, including `GetCurrentParsfileName`, also use output arguments rather than returning the string as a function result.
- `Gotolibrary(library,title,category)` selects the intended native dataset. `ExportParsfile(fullPath,0)` exports expanded PAR; mode `1` exports native CPAR. `ImportParsfile(fullPath,0)` skips existing datasets; mode `1` overwrites matching datasets. Do not guess another mode's meaning.
- Get/put field methods are control-specific and may silently do nothing for an invalid keyword. Read back the value and inspect the serialized native data. In the case study, attempts to set `#AltPath` did not persist; the unused alternate-directory option was disabled instead of being declared configured.
- Overwrite import can still show **Import - Locked File**. Inspect the real dialog and destination. In an isolated test clone, **Unlock and Import** with the checkbox applying the choice to remaining locked datasets was successful. This is not permission to unlock or overwrite original/user databases.

Keep the export file and trace under unique paths. Keep an automation client alive only as long as needed for its operations; release task-owned helpers cleanly when finished. An automation-created Browser can exit when its final client releases it. Do not force-close other sessions to obtain a COM instance.

## Verify the archive in levels

1. **Container/dependencies:** Record bytes and SHA256; inspect format markers, archive CRC and required assets; compare model/code hashes with the tested package. The read-only [inspect_cpar.py](../scripts/inspect_cpar.py) supports this local ZIP-based 2021 format. Its success does not establish native import or runnable behavior.
2. **Native import/open:** Import the exported file in a separate writable test database/clone. Open the intended Run Control and model/vehicle links. Preserve native logs and selected identities. Say whether this tested import into an existing database or creation of an empty database; they are different operations.
3. **Regenerated inputs:** Use the native Browser to generate the solver inputs. Verify I/O ordering/units, actual override precedence, timing, vehicle/table data and effective settings against the tested experiment. Full byte equality of PAR files is not required when only titles, timestamps, UUIDs or UI metadata differ.
4. **Run:** Execute the imported model/parameters through the claimed MATLAB/native entry point. Check fresh normal termination and outputs; compare with the retained baseline. Use case coverage appropriate to the deliverable. If changing the block form, preserve an unchanged baseline and test the replacement under matched conditions.
5. **Final location and relocation:** Generate runtime paths at the requested destination and run a representative case. Hash-check copied models, inputs and dependencies. If claiming portability, test a separate renamed/relocated copy as described in [portable-delivery.md](portable-delivery.md), including native import/regeneration there when archive portability is claimed. Resolve project model links and included assets against the imported database/package, keep the installed Browser working directory distinct, and disclose any remaining machine-specific reference. Do not modify historical input files just to hide old absolute paths.

Record which levels passed, failed or were not performed. Opening a SLX, CRC success, native dataset import and a complete co-simulation are separate claims. Do not imply Browser **Run Now**, live animation or empty-database creation worked unless those specific actions were tested. Keep screenshots and reports consistent with the final archive revision; recheck after material changes.

## Common local failures and bounded recovery

- In this case native export crashed through the CVI runtime on a long-path clone; export succeeded from a short ASCII path. Treat short paths as a tested workaround, not proof that every crash is caused by path length. Preserve the log/failure and change one relevant condition before retrying.
- Browser's real visible CVI panels can have an off-screen auxiliary carrier near `(25000,25000)`. The computer-use tool selected that carrier and reported `window crop is outside captured monitor`, although the real dialog was visible. Do not conclude the GUI is absent. Prefer native APIs; if GUI work is needed, inspect actual visible windows and use permitted tooling/fallbacks under the computer-use guidance. Never retain case-specific window handles, PIDs or click coordinates as reusable targets.
- A database-open warning is not a reason to create another writer. Reuse the known session, select a separate test clone, or cancel the duplicate attempt.
- **No Data** may be the currently selected empty Run Control rather than an archive error. Verify the database root and whether the intended datasets were actually imported, then select the recorded category/title. In the normal GUI, **Open Existing Database** opens a prepared database; **Import Parsfile** imports one CPAR into the current database. Import preview, changed categories and skipped duplicates need explicit explanation in the user guide when relevant.
- Inspect license/startup logs and existing process ownership before launching another helper. Do not change license files or silently terminate processes. Preserve applicable permission requirements and any unsaved user work.

Keep source runtime files/results available if archive or UI work fails. Describe the precise blocker and next verification step; do not repeat unchanged failed launches indefinitely or rebuild the study to work around a packaging problem.
