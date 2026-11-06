# CarSim 2021 MCP 适配服务

使用 Windows x64 和 Python 3.12。原项目验证过 CarSim 2021.0 和 MATLAB / Simulink R2025b。数据工具从本机的 CarSim 数据库复制出受管理的工作副本。闭环示例需要已授权的本地软件及 [MathWorks 官方 MATLAB MCP](https://github.com/matlab/matlab-mcp-server)，原项目使用 v0.15.0。

## 安装与数据工具

在 `mcp` 目录用 PowerShell 执行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
Copy-Item config.example.json config.local.json
```

编辑 `config.local.json`。填写 `original_database` 和 `carsim_program`，分别指向包含 `Runs/` 的数据库根目录和包含 `Programs/` 的安装目录。工作目录须与源库分开，并有足够空间容纳一次数据库副本。相对路径以配置文件所在位置为基准。Windows 路径建议用正斜杠。

```powershell
.\.venv\Scripts\python.exe cli.py info
.\.venv\Scripts\python.exe cli.py initialize
```

要在 Codex 使用数据工具，将下段加入自己的 MCP 配置，替换示例绝对路径，重新加载后调用 `carsim_info`、`initialize_workspace`、`search_datasets` 和 `read_dataset`。

```toml
[mcp_servers.carsim2021]
command = 'C:/projects/carsim-simulink-workflows/mcp/.venv/Scripts/python.exe'
args = ['C:/projects/carsim-simulink-workflows/mcp/server.py', '--config', 'C:/projects/carsim-simulink-workflows/mcp/config.local.json']
env_vars = ['WINDIR', 'MW_MCP_SERVER_MATLAB_SESSION_CONNECTION_DETAILS']
startup_timeout_sec = 60
tool_timeout_sec = 600
```

## 可选闭环示例

[准备自己的 ABS 示例输入和 Simulink 模型](../examples/abs/README.md)。MATLAB MCP 以 existing 模式连接已共享的 MATLAB 会话。准备完成后，调用 `run_closed_loop_workflow`，或运行：

```powershell
.\.venv\Scripts\python.exe cli.py run --label abs_check --mass 1150 --stop-time 2
```

结果位于工作目录的 `experiments/<id>/`。检查 `validation.json`、`native_echo.par`、输入输出 CSV 及求解器日志。用 `experiment_status` 和 `validate_experiment` 复核。对单次实验参数副本的恢复使用 `rollback_parameters`。需要新试验时重新准备独立运行目录。

现成运行入口约束为 4 个制动压力输入、6 个输出、0.5 ms 最大步长和 2–10 s 停止时间。支持的参数为 `M_SU`（空载簧载质量，kg）、`H_CG_SU`（其质心高度，mm）和 `IZZ_SU`（其横摆惯量，kg·m²）。使用自己审查过的数据库和模型。部署与测试所用的软件和许可证由使用者提供。

## 验证

从 `mcp` 目录执行 `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`。测试使用临时目录和合成参数文件，检查数据访问、路径边界、参数准备、哈希检查和回滚。公开适配版也通过了本机 MCP 连接、数据读取及使用已授权安装的 ABS 输入进行实验准备和回滚的检查。闭环求解结果引用原项目的实测记录。
