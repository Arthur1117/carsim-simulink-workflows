# CarSim × Simulink 联合仿真工作流

这套 Skills 和工具面向已有 CarSim / MATLAB / Simulink 安装的研究和教学项目。你可以用自己的车辆、控制器和工况，从最小闭环开始，逐步完成实验、验证和交付。

## 用于自己的项目

1. 下载仓库，将 `skills/carsim-2021-simulink` 整个目录复制到 Codex 的用户 Skills 目录（Windows 下通常是 `%USERPROFILE%/.codex/skills/`）。
2. 在新对话中调用 `$carsim-2021-simulink`，提供自己的车辆来源、控制目标、工况、软件版本和交付位置。可先填 [项目起步模板](docs/project-start.md)。
3. 先保留独立可检查的 Simulink 控制器和信号接口，再接入本机 CarSim 原生求解器。用小闭环核对模型、单位、通道顺序、有效参数与求解器日志，随后扩展到完整工况。
4. 按项目需求交付运行入口、结果及复核记录。CPAR、图形与回放按各自的验收方法检查。

[Skill 与参考资料](skills/carsim-2021-simulink/SKILL.md) · [FOISMC 应用案例](examples/foismc/README.md)

## 可选 MCP 工具

本仓库提供可安装的 CarSim 适配服务。[安装与工具说明](mcp/README.md)

| 组件 | 作用 |
| --- | --- |
| CarSim MCP 数据工具 | 检查本机安装、建立并核对数据库副本、搜索和读取车辆、工况及其他数据集 |
| CarSim MCP 闭环示例 | 使用已审查的 Split-Mu ABS 输入与模型演示准备、执行、核验和回滚 |
| MathWorks 官方 MATLAB MCP | 连接 MATLAB 并调用 MATLAB 代码和脚本 |

自定义项目可以走 Skill 的通用路线，按自身模型审查参数、通道和运行入口。要让某个新项目也能通过同一个 MCP 工具一键执行，需要为该项目另外实现并验证运行配置。ABS 只用于演示现成的闭环入口。

[第三方来源、固定提交及本项目新增内容](THIRD_PARTY.md) · [MIT 许可证](LICENSE)
