# Tested environment and evidence

The original ABS integration was exercised on CarSim 2021.0, MATLAB R2025b and Windows x64. The tests covered source database copying, repeatability, parameter echo and native output validation. The prepared ABS model logged the four inputs and six outputs as Simulink timeseries. The comparison passed its integration checks; calibration is separate.

The original FOISMC study compared four matched cases using the official solver through a generic S-Function and the official library block. The matched logs were equal. A twelve-case run was used for the three-strategy comparison, with independently reconstructed baselines. Native import and recorded animation playback were verified separately. See the repository's FOISMC example for the scope and paper reference.

Use the recipient's own authorized installation. Verify its license provider, executable paths, model bindings, input files and channels before claiming compatibility with another environment.
