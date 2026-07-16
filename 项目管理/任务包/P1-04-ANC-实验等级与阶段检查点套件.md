# P1-04-ANC 实验等级与阶段检查点套件任务包

## 新会话启动指令

```text
请执行 cloud-ops-roadmap 的 P1-04-ANC 实验等级与阶段检查点套件任务。

你是新的独立执行会话，只负责一次性交付实验手册入口、四级实验合同、21 个阶段检查点和本任务执行报告；不是项目领导者、实验正文作者、项目映射执行者、审查者或最终验收者。工作目录固定为 C:\Workspace\Projects\cloud-ops-roadmap，分支固定为 main。本项目禁用 superpowers-zh 技能组，不得自行增加头脑风暴、TDD、工作树、子代理或审查轮次。

任何写操作前完整阅读：AGENTS.md、CODEX-PRD.md、AI-CODEX-RULES.md、本任务包、2026-07-16 Phase 1 波次 4 压缩执行与实践映射合同设计说明和实施计划、原 Phase 1 导航与完整大纲设计说明和实施计划、实验模板、知识库 README、21 个阶段 README、任务看板和校验器 README。用 Git 查询本任务包最近提交，并确认启动 HEAD 精确等于主会话提供的签发提交。

固定输入为签发提交可达的波次 3 验收提交 `be9e910aef8730609bbff3b6345ad85633797b4d` 及其 21/620/817 章节树。启动门禁：main、origin、工作区干净；P1-03-RTE、P1-03-IDX、P1-03R 均 accepted；Python 3.11.15；133/133；默认错误 0；views 21/620/817 且错误 0；正式正文 0。

唯一目标：按冻结合同在一个产品提交中建立四级实验锚点定义和 CP-00 至 CP-20 阶段检查点。只允许修改或创建：
- 实验手册/README.md
- 实验手册/Level-1-基础实验/README.md
- 实验手册/Level-2-综合实验/README.md
- 实验手册/Level-3-企业实验/README.md
- 实验手册/Level-4-架构实验/README.md
- 学习路线/阶段检查点/README.md
- 项目管理/执行报告/P1-04-ANC-执行报告.md

必须严格执行冻结合同：四个 Level 分别定义 LAB-L1 至 LAB-L4 的准入、能力边界、退出、风险和证据；每个 Level README 中自身 LAB 字面量精确出现一次且不得出现其他等级；不得列实验文件或步骤。检查点使用精确五列表头，精确 21 行，CP-00 至 CP-20 与阶段 00 至 20 一一对应；所需章节使用该阶段最后一章；实践锚点是该阶段九列表实际出现的 LAB 等级去重集合，没有则写 `—`；能力结果是单行可观察结果。不得创建或引用 PRJ 锚点。

禁止修改知识库、项目实战、其他学习路线、技术索引、看板、任务包、计划、PRD、ADR、版本基线、校验器、模板或其他文件。禁止创建实验正文、命令、配置、代码、图表、故障演练、项目实现、云资源或动态版本/GPU/模型选择；禁止远程写。

执行时由你创建或修改的上述白名单文件属于本任务交付，不得误判为未知外部修改；任何白名单外修改必须立即停止。

提交顺序：
1. `docs: establish experiment anchors and checkpoints`，只包含六个产品文件；
2. `docs: report P1-04-ANC anchors`，只包含执行报告。

必须运行 133/133、默认、views、partial、正式正文计数、链接和 Git 检查。另以独立只读解析证明：LAB 定义 4/4；各 Level 锚点字面量精确；检查点 21/21 且连续；阶段和末章对应 21/21；检查点 LAB 集合与阶段表一致；未知引用和失效链接 0。由于项目产品尚未创建，本任务不要求 complete 退出 0，也不得为追求 complete 越界创建项目文件。

停止条件：固定输入漂移；实际统计不符；需要修改白名单外文件；无法闭合 4 个 LAB 或 21 个 CP；133/默认/views/partial、链接或正文边界失败；需要具体动态版本、GPU、模型或外部写。

完成回复必须包含 submitted/rework/blocked、两个完整提交、精确文件范围、4/4 和 21/21 统计、门禁、异常、风险、未决和远程操作。不得更新看板、宣布 accepted、启动 PRJ 或自行安排审查。
```

## 1. 任务信息

- **任务编号：** `P1-04-ANC`
- **任务名称：** 实验等级与阶段检查点套件
- **覆盖原任务：** `P1-04A`、`P1-04B`
- **状态：** `assigned`
- **最终验收者：** Phase 1 主会话，经 P1-04R 集成审查后统一裁决

## 2. 主要成果

一次性建立四级实验合同和 21 个阶段检查点，只提供未来实践的导航锚点，不创建任何实验正文。

## 3. 验收摘要

- 六个产品文件一个提交，报告一个提交；
- LAB 定义 4/4，CP 定义 21/21；
- `partial` 错误 0，尚缺项目产品导致的 `complete` 缺口不属于本任务失败；
- 正式正文 0，无 `PRJ-*`，无章节树修改。

## 4. 验证

```powershell
$py = 'C:\Users\beiyue\AppData\Local\Temp\cloud-ops-roadmap-uv-0.11.28\python\cpython-3.11.15-windows-x86_64-none\python.exe'
& $py -B -m unittest discover -s '脚本资源/项目校验/tests' -p 'test_*.py' -v
& $py -B '脚本资源/项目校验/validate_repository.py' .
& $py -B '脚本资源/项目校验/validate_repository.py' . --outline-gate views
& $py -B '脚本资源/项目校验/validate_repository.py' . --outline-gate partial
git diff --check
git status --short
```

另做 LAB、CP、末章对应、阶段锚点集合、链接、正文边界和提交范围的只读检查。
