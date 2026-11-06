# 用本机安装准备 Split-Mu ABS 示例

该示例展示 MCP 的闭环执行与校验。你可以先完成 [数据工具安装](../../mcp/README.md)，再准备这些输入。

1. 在自己的授权安装中找到 `Ext. ABS: Split Mu` 工况。通过 CarSim 展开其参数（`Run_all.par`），检查工况与数据来源。选择带完整展开内容、无外部绝对路径或未展开 `PARSFILE` 引用的输入，置于你选择的项目数据库内。
2. 检查导入顺序为 `IMP_PBK_L1, IMP_PBK_R1, IMP_PBK_L2, IMP_PBK_R2`，导出顺序为 `Vx_L1, Vx_R1, Vx_L2, Vx_R2, Vx_SM, Pbk_Con`。把文件相对于源库根目录的路径写入 `abs_base`，用 PowerShell `Get-FileHash -Algorithm SHA256` 获取该文件的 SHA-256，转成小写写入 `abs_base_sha256`。哈希用于固定已审查的输入。若已经建立工作副本，要用新的工作目录重新初始化来纳入新的源文件。
3. 从本机数据库找到 `Extensions/Simulink/abs_SLX_CS9.slx`，另存到自己的工作位置，文件名为 `cs21_abs_smoke.slx`。确认 CarSim 模块链接到安装目录中的 `Solver_SF/CarSim S-Function`，SIM 文件填 `simfile.sim`，Run 设置为 `Run`，停止方式为 `External`，关闭实时运行选项。保留原控制器与制动执行器。
4. 在 CarSim 模块输入和输出线上各分接一个 **To Workspace** 块，变量名分别为 `cs21_imports` 和 `cs21_exports`，保存格式为 `Timeseries`，采样继承且保留全部样本。输入是执行器送给车辆的四通道信号。输出在分解成各通道之前取车辆模块的六通道信号。保存模型，将路径和 SHA-256 分别写入 `abs_model` 和 `model_sha256`。
5. 让 CarSim 使用正常的授权配置。打开 MATLAB，按官方 MCP 文档共享当前会话（`shareMATLABSession`）。配置指向注册了官方 MATLAB MCP 的 Codex 配置文件，并填好对应服务名，默认 `matlab`。关闭同名模型后，先按 [MCP 说明](../../mcp/README.md) 做一次两秒运行，再尝试修改簧载质量并检查原生 echo。

原环境的 2 秒示例记录了 4,001 个样本，并验证了 `M_SU` 从 1110 kg 改为 1150 kg 后的原生回读。日志中有车辆表格外推提示，物理标定需要另外验证。公开版本从使用者自己的安装获得模型与数据，不随仓库分发厂商案例文件。
