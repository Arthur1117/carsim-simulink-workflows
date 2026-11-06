# Configure the local tools

This skill can guide a new CarSim/Simulink project using the installed tools. Configure the optional `carsim2021` MCP using the repository's `mcp/README.md` and `mcp/config.example.json`. Use the official MATLAB MCP to access MATLAB, or operate the installed applications directly. On Windows the tested combination was CarSim 2021.0 and MATLAB R2025b/win64.

Start with `carsim_info` and `initialize_workspace` for database discovery. Database tools read a managed copy of the installation database. The optional closed-loop demonstration uses user-prepared ABS inputs under a separately checked contract. The repository's `examples/abs/README.md` describes the setup. A different project can use the staged workflow and native solver integration without enabling the ABS demo.

For the CLI, run `.venv/Scripts/python.exe cli.py info` from the MCP directory. The local configuration selects the workspace and the licensed installation. Keep experiment files in that workspace.
