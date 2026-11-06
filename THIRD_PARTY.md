# 第三方来源与本项目新增内容

| 来源 | 固定提交 | 仓库内复用内容 |
| --- | --- | --- |
| [AngelZhaksy / CarSim MCP](https://github.com/AngelZhaksy/carsim-mcp-Carsim-matlab-mcp-server) | `bf904a0176248b93a794df2b74070b444a523597` | `mcp/vendor/carsim_mcp/carsim_core.py`，用于参数文件、原生回读和结果处理 |
| [zyfgi / carsim-guide-skill](https://github.com/zyfgi/carsim-guide-skill) | `5d80c42ed272440a3b1f63161d75d2d6a216caf7` | `mcp/vendor/carsim_guide/` 中的 `database_tools.py`、`base_registry.py`、`carsim_errors.py` 和 `version_compatibility.py` |
| [MathWorks 官方 MATLAB MCP](https://github.com/matlab/matlab-mcp-server) | 原环境实测 v0.15.0 | 外部工具，适配层调用其 MATLAB 代码与脚本执行接口 |

`vendor/` 内上游文件按固定快照原样保留，对应许可证在 [CarSim MCP](mcp/vendor/carsim_mcp/LICENSE) 和 [CarSim Guide](mcp/vendor/carsim_guide/LICENSE)。本项目新增 CarSim 2021 适配、参数约束、独立实验目录、原生回读验证、与 MATLAB MCP 的编排和实验回滚，以及面向自定义研究任务的 Skills 和交付流程。公开版将安装路径、数据库和 ABS 示例输入改为使用者配置。
