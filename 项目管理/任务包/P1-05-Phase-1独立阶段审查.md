# P1-05 Phase 1 独立阶段审查任务包

## 新会话启动指令

```text
请执行 cloud-ops-roadmap 的 P1-05 Phase 1 独立阶段审查。

你是新的独立阶段审查会话，不得参与 Phase 1 任何产品、执行报告、返工产品、专项审查报告或主会话治理文件的编写；不是修复者、项目领导者或最终验收者。工作目录固定为 C:\Workspace\Projects\cloud-ops-roadmap，分支固定为 main。本项目禁用 superpowers-zh 技能组，不得自行增加子审查、工作树或重复工作流。

任何写操作前完整阅读：AGENTS.md、CODEX-PRD.md、AI-CODEX-RULES.md、本任务包、2026-07-13 Phase 1 导航与完整大纲设计说明和实施计划、波次 3/4 压缩设计和实施计划、Phase 0 最终验收报告、任务看板、项目记忆 MEMORY 及其路由文件、版本基线、来源优先级、ADR-0001 至 ADR-0005、校验器 README；再按任务看板和最终验收标准抽取 P1-01、波次 2、P1-03R、P1-04R 的任务包、报告和固定提交证据。确认启动 HEAD 精确等于主会话提供的签发提交、工作区干净，且 P1-01、波次 2、P1-03、P1-04 所有最终任务均为 accepted。

唯一目标：对完整 Phase 1 固定基线做一次阶段级独立审查，判断 2026-07-13 实施计划第 12 节 16 项最终验收标准是否全部具备可复验证据，并给出 `recommend-accept`、`changes-required` 或 `blocked` 建议。只允许创建 `项目管理/验收记录/Phase-1-独立审查报告.md`。

禁止修改任何产品、执行报告、专项审查、看板、计划、任务包、PRD、ADR、项目记忆、版本基线、校验器、README 入口或其他文件；发现问题只记录，不得修复。禁止创建正式学习正文、实验、项目实现、故障、面试、脚本、配置、图表或云资源；禁止 push、PR、标签、Release、网站发布和其他远程写。

机械审查必须 fresh 运行并记录：Python 3.11.15；133/133；默认错误 0；partial/catalogs/views/complete 四级门禁全部错误 0；21 阶段、620 章、817 边；三个月主线/弹性/闭包；技术索引覆盖；LAB/CP/PRJ 定义；项目/章节双向集合；链接；正式正文允许列表；敏感信息与占位符；Git 固定提交范围和工作区卫生。对历史问题只核对最终关闭证据，不重演已通过的每轮返工和单元级异常注入。

人工审查只按最终验收标准收敛为十个阶段主题：双重可用与章节颗粒度；零基础连续性和前置 DAG；十二周就业闭包；完整/职业/节奏/依赖路线；三类技术索引可发现性；Linux 日志分层与 AI Infra/AIOps 边界；四级实验和检查点；RuoYi 项目连续演进与 AI 项目独立性；Kubernetes 四层版本角色和动态决策门；无正式正文与 Phase 2 解锁边界。专项审查已经机械证明的逐行映射不重复做文案偏好审查。

必须重新核验四个官方入口：Kubernetes 1.36、Kubernetes patch releases、containerd releases、Calico requirements。新的 1.36 patch 只建议独立版本维护任务，不直接修改全局基线；minor 或主组合冲突则建议 blocked。VitePress、GPU、模型和云资源具体组合继续保持后续阶段门，不得把未决选择误判为 Phase 1 阻塞。

报告必须逐项给出 16 项最终标准的 passed/failed/blocked 与证据，列出 Critical/Important/Minor。Minor 且不影响完整门禁、双重可用、范围或 Phase 2 解锁的事项只登记后续维护；仅 Critical/Important 才建议一个合并的 `P1-05-M1`，不得拆分成多轮 R1/R2。结论为 recommend-accept 时必须明确建议 Phase 2 只解锁任务设计、样章门和基础阶段内容任务，不授权批量正文、动态组合、网站发布或云资源。

提交信息固定为 `docs: review Phase 1 navigation baseline`，提交只能包含唯一审查报告。提交后运行 git show --check、精确单文件范围和工作区干净检查。不得更新看板、宣布 Phase 1 accepted、编写最终验收报告或启动 Phase 2。

停止条件：签发 HEAD 或固定提交不符；工作区未知修改；前置任务未 accepted；任何 fresh 门禁失败且无法形成可靠审查证据；发现未关闭 changes-required/blocked；正式正文越界；权威版本出现 minor/主组合冲突；需要修改产品或外部写。

完成回复必须包含建议结论、签发与审查提交完整哈希、16 项矩阵、关键统计、十项人工主题、动态官方入口、问题分级、是否需要唯一 M1、Phase 2 建议解锁范围、风险、未决和远程操作。不得把完成建议表述为主会话最终验收。
```

## 1. 任务信息

- **任务编号：** `P1-05`
- **任务名称：** Phase 1 独立阶段审查
- **状态：** `assigned`
- **前置：** P1-01、波次 2、P1-03、P1-04 所有最终任务均 `accepted`
- **唯一交付：** `项目管理/验收记录/Phase-1-独立审查报告.md`
- **最终裁决者：** Phase 1 主会话通过 P1-06 完成最终验收

## 2. 审查原则

阶段审查只聚合验证最终 Phase 1 基线和 16 项验收标准，不重做专项审查的逐文件文案评议。机械门禁 fresh 运行一次，问题集中到一份报告，必要返工最多一个合并 M1。

## 3. 验证

```powershell
$py = 'C:\Users\beiyue\AppData\Local\Temp\cloud-ops-roadmap-uv-0.11.28\python\cpython-3.11.15-windows-x86_64-none\python.exe'
& $py -B -m unittest discover -s '脚本资源/项目校验/tests' -p 'test_*.py' -v
& $py -B '脚本资源/项目校验/validate_repository.py' .
& $py -B '脚本资源/项目校验/validate_repository.py' . --outline-gate partial
& $py -B '脚本资源/项目校验/validate_repository.py' . --outline-gate catalogs
& $py -B '脚本资源/项目校验/validate_repository.py' . --outline-gate views
& $py -B '脚本资源/项目校验/validate_repository.py' . --outline-gate complete
git diff --check
git status --short
```

另做 16 项矩阵、路线与索引集合、LAB/CP/PRJ、项目双向映射、正式正文允许列表、动态入口、敏感信息、占位符和固定提交范围的独立只读检查。
