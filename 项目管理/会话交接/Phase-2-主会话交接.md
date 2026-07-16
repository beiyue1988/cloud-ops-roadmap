# Phase 2 主会话交接

## 1. 交接声明

Phase 1“导航与完整大纲”已经通过最终验收。用户决定为 Phase 2 创建新的主会话交接指令；新会话完成本文件规定的启动门禁并明确接受职责后，将成为 `cloud-ops-roadmap` 的唯一项目领导者、架构制定者、任务签发者、质量负责人和最终验收者。

Phase 1 主会话在新主会话明确接任前继续承担领导责任。接任生效后，Phase 1 主会话不再参与 Phase 2 日常治理、任务签发或最终裁决，避免两个主会话并行修改计划、任务状态和阶段结论。用户始终可以暂停、替换或重新授权主会话。

## 2. 固定状态与提交

- Phase 1 独立审查提交：`02d7b29afdcc907ac9203172622900b35707f75e`；
- Phase 1 最终验收提交：`4d606b1a8866314ba4d5f2d4aa03f392077762a7`；
- Phase 1 状态：`accepted`；
- Phase 2 状态：只解锁设计、样章门、模板适配和阶段 00–05 的边界化单任务；
- `origin/main` 已于 2026-07-16 推送至 Phase 1 最终验收提交 `4d606b1a8866314ba4d5f2d4aa03f392077762a7`。

本文件不能预测包含自身的交接提交哈希。新主会话必须使用 Git 查询本文件最近一次提交，并把实际完整哈希作为 Phase 2 交接提交记录。

权威入口：

- [Phase 1 最终验收报告](../验收记录/Phase-1-最终验收报告.md)
- [Phase 1 独立审查报告](../验收记录/Phase-1-独立审查报告.md)
- [Phase 1 设计说明](../执行计划/2026-07-13-Phase-1导航与完整大纲-设计说明.md)
- [Phase 1 实施计划](../执行计划/2026-07-13-Phase-1导航与完整大纲-实施计划.md)
- [任务看板](../任务看板.md)

## 3. 必读顺序

任何写操作前，新主会话必须按顺序完整阅读：

1. `AGENTS.md`；
2. 本交接文件；
3. `CODEX-PRD.md`；
4. `项目管理/验收记录/Phase-1-最终验收报告.md`；
5. `项目管理/验收记录/Phase-1-独立审查报告.md`；
6. `项目记忆/MEMORY.md`，以及它路由的 `decisions.md`、`patterns.md`、`open-questions.md`、`resources.md`；
7. `项目管理/任务看板.md`；
8. `版本记录/软件版本基线.md` 与 `版本记录/更新日志.md`；
9. `参考资料/来源优先级.md`；
10. `项目管理/决策记录/README.md` 与 ADR-0001 至 ADR-0006；
11. `AI-CODEX-RULES.md`；
12. `模板/README.md`、章节模板、实验模板、执行报告模板和验收报告模板；
13. `知识库/README.md` 与阶段 00–05 的六个阶段 README；
14. `学习路线/00-学习路线导航.md`、`01-完整成长路线.md`、`02-三个月就业路线.md`、`05-知识前置依赖.md` 与 `阶段检查点/README.md`；
15. `实验手册/README.md` 与四个 Level README；
16. `脚本资源/项目校验/README.md`。

不得只依赖本交接摘要，也不得把历史聊天记录当作权威规范。

## 4. 启动门禁

新主会话在首次写操作前必须实际执行并记录：

1. 当前分支为 `main`，工作区干净，`origin` 指向官方项目远程；
2. 当前 HEAD 包含 Phase 1 最终验收提交 `4d606b1a8866314ba4d5f2d4aa03f392077762a7`；
3. 使用 Git 查询本交接文件最近提交，并确认该交接提交在当前历史中；
4. Python 为 3.11.15；
5. 仓库校验器单元测试 133/133；
6. 默认校验退出 0、知识章节 0、错误 0；
7. `partial`、`catalogs`、`views`、`complete` 四级大纲门禁全部退出 0；
8. `complete` 仍为 21 阶段、620 章、817 条依赖、1184 个视图引用、45 个锚点、错误 0；
9. 七类正式内容目录中非 `README.md` 学习 Markdown 仍为 0；
10. `学习路线/` 只含批准的 00–06 七个导航文件，`技术索引/` 只含批准的三个索引文件；
11. 只读远程检查 `git ls-remote --heads origin` 退出 0；
12. Phase 1 最终验收提交和交接提交都可从当前 HEAD 到达。

推荐命令：

```powershell
git branch --show-current
git rev-parse HEAD
git status --short
git remote -v
git merge-base --is-ancestor 4d606b1a8866314ba4d5f2d4aa03f392077762a7 HEAD
$handoffCommit = git log -1 --format=%H -- '项目管理/会话交接/Phase-2-主会话交接.md'
git merge-base --is-ancestor $handoffCommit HEAD

$py = 'C:\Users\beiyue\AppData\Local\Temp\cloud-ops-roadmap-uv-0.11.28\python\cpython-3.11.15-windows-x86_64-none\python.exe'
& $py --version
& $py -B -m unittest discover -s '脚本资源/项目校验/tests' -p 'test_*.py'
& $py -B '脚本资源/项目校验/validate_repository.py' .
& $py -B '脚本资源/项目校验/validate_repository.py' . --outline-gate partial
& $py -B '脚本资源/项目校验/validate_repository.py' . --outline-gate catalogs
& $py -B '脚本资源/项目校验/validate_repository.py' . --outline-gate views
& $py -B '脚本资源/项目校验/validate_repository.py' . --outline-gate complete
git ls-remote --heads origin
```

若只读远程检查因受限沙箱失败，只能以完全相同的只读命令合规提升一次；禁止借机 fetch、pull、push、写凭据、关闭安全控制或修改远程。

## 5. Phase 1 继承基线

Phase 2 必须继承以下已接受事实：

- 阶段 00–20 的 README 九列表是 620 个章节 ID、目标、类型、直接前置、投入、就业标签和实践锚点的唯一权威目录源；
- 21 阶段、620 章、817 条直接前置、52 条跨阶段边构成已接受 DAG；
- 三个月主线是 293 章必须学闭包，弹性集合 74 章，两者交集 0；
- 技术类型覆盖 146/146，技术主词 96；
- CP/LAB/PRJ 定义分别为 21/4/20，项目与章节双向映射为 125=125；
- 章节 ID 在 Phase 1 验收后保持稳定，不能在正文任务中顺手重排、改名或复用；
- 路线、索引、检查点和项目视图是派生入口，不是第二份正文或章节目录源；
- 校验器只验证权威清单和派生视图，不自动生成或覆盖它们；
- P1-01 对非法组合输入可能多报一条 `OL011` 是非阻塞已知限制，合法完整基线不受影响。

任何确需变更章节 ID、标签、直接前置、阶段末章或实践映射的请求，必须停止普通内容任务，由独立大纲维护任务原子更新权威阶段表和所有受影响派生视图。

## 6. Phase 2 授权范围

Phase 2 对应 PRD 的“基础地基”，范围固定为阶段 00–05：

- 00 入门与运维认知；
- 01 计算机与服务器基础；
- 02 网络基础；
- 03 实验环境；
- 04 Linux 基础；
- 05 Linux 系统管理。

当前只允许逐门推进：

1. 审计阶段 00–05 的章节职责、前置、模板和实验锚点；
2. 设计“少量样章 → 模板校正 → 批次任务”的执行架构；
3. 制定 Phase 2 书面设计、实施计划、样章选择规则、技术验证合同和独立审查门；
4. 在用户批准设计与实施计划后，创建边界清晰的单文件内容任务包；
5. 让独立执行会话编写获授权的章节或实验，并提交产品与执行报告；
6. 让高风险实验、样章门和阶段性批次接受独立审查；
7. 主会话依据 fresh 证据接受、退回或创建一次性合并维护任务。

Phase 2 解锁不等于所有阶段 00–05 任务自动进入 `ready`，更不等于一次性授权 136 个章节或全部实验批量生产。

## 7. 样章优先门

正式批量内容任务前必须建立样章门：

1. 从阶段 00–05 选择少量、具有代表性的章节类型；
2. 样章至少覆盖概念/原理、方法论、操作型内容与相称实践证据中的代表组合；
3. 样章必须遵守章节模板、AI 内容规则、来源优先级、版本边界和安全规则；
4. 操作型样章必须提供可复验环境、命令目的、影响、验证、清理或回退；
5. 样章经独立内容审查后，主会话才能决定模板是否需要治理级调整；
6. 样章门 accepted 前不得创建阶段 00–05 的批量正文任务包。

新主会话应先提出样章选择原则和候选组合，由用户批准；不得在交接启动流程中直接生成样章。

## 8. Phase 2 动态版本与实验门

已接受的相关基线：

- Rocky Linux 9.8 x86_64 是阶段 03 主实验客体，当前仅 `source-verified`；
- VMware Workstation Pro 26H1 是阶段 03 本地虚拟化线；Windows 10 20H1+ 或 Windows 11 x86-64 为主宿主，具体下载 build 动态维护；
- Linux 客体工具使用发行版提供的 `open-vm-tools` 路径；
- 26H1、Rocky 9.8、宿主矩阵、许可与工具边界均不等于环境已经安装验证。

新主会话启动时重新核验：

- <https://rockylinux.org/news/rocky-linux-9-8-ga-release>
- <https://wiki.rockylinux.org/rocky/version/>
- <https://blogs.vmware.com/cloud-foundation/2026/05/14/announcing-vmware-workstation-and-fusion-26h1/>
- <https://knowledge.broadcom.com/external/article?legacyId=80807>
- <https://knowledge.broadcom.com/external/article/387947/installing-vmware-workstation-pro.html>

2026-07-16 交接复核发现 Rocky Linux 版本指南存在非阻塞的页面内部呈现不一致：页面顶部“当前版本”摘要仍显示 9.7，但同页 9.x 详细表已列 9.8、标记 `Supported=Yes`，官方 9.8 GA 公告也确认安装介质与镜像已发布。当前以 GA 公告和详细版本表共同支持 9.8 基线，不因摘要滞后改写基线；新主会话必须保留该来源限制，不能只引用顶部摘要声称当前 minor。

同日复核确认 VMware 26H1 公告、26H1 宿主系统文章和安装入口仍可访问，未发现需要替代 ADR 的发布线变化；这仍不构成下载、安装或宿主兼容的环境证据。

阶段 03 首个安装实验进入执行前，还必须 fresh 核定实际 build、下载可用性、处理器、宿主版本、Hyper-V/VBS/内存完整性组合、适用许可、Rocky Linux 9.8 镜像、`open-vm-tools`、快照/克隆和回退条件。不得为通过实验而关闭安全控制。改变 26H1 发布线或主产品必须走替代 ADR。

VitePress 具体依赖仍是网站任务门；GPU、模型、云实例和 AI 软件栈仍是 AI Infra 实验前的非阻塞决策门，都不阻塞 Phase 2 设计和阶段 00–05 内容。

## 9. 当前禁止范围

- 主会话直接编写学习正文、实验步骤、脚本、配置、图表、故障答案或面试答案；
- 在样章门 accepted 前批量创建阶段 00–05 正文任务；
- 创建阶段 06 及以后内容，或把 Phase 3+ 任务混入 Phase 2；
- 修改已接受的 620 章 ID、DAG、路线、索引、实践锚点或项目映射，除非另有独立维护任务；
- 修改已接受 ADR、许可证、RuoYi 固定对象、Kubernetes 分层策略或全局版本治理模型；
- 把来源核验写成环境验证，或声称 VMware/Rocky、云资源、集群、应用已经运行；
- 选择尚未到门禁的 VitePress、GPU、模型或云资源组合；
- push、Pull Request、tag、Release、网站发布、GitHub 设置修改、软件下载、安装或云资源创建，除非用户对具体外部写操作明确授权；
- 与其他主会话并行作出 Phase 2 最终裁决。

## 10. 治理、审查与验收责任

新主会话继承以下责任：

- 维护 Phase 2 目标、范围、样章策略、任务顺序、质量门和动态版本门；
- 只编辑治理文件，不直接生产具体教学交付物；
- 为每个执行会话提供完整启动指令、精确文件白名单、来源、验证、停止条件和汇报格式；
- 确保同一时刻没有两个执行会话修改同一文件；
- 对执行提交先做范围和 Git 初验，再做技术、教学、来源、安全和集成验收；
- 对高风险实验、样章门和阶段成果安排一次适度独立审查；
- 只有主会话可以更新 `accepted`、`rework` 或 `blocked`；
- 维护项目记忆，只保存稳定、可复用且无敏感信息的事实；
- Phase 2 结束时组织独立阶段审查、最终验收和下一阶段交接。

## 11. 停止条件

遇到以下情况必须停止扩大范围并提供证据：

- 工作区存在未知修改、固定提交缺失、分支或远程不符；
- 133/133、默认校验或任何大纲门禁失败；
- 正式正文或其他产品在任务包签发前越界出现；
- 权威章节清单与路线、索引、检查点或项目映射不一致；
- 需要改变 Phase 1 已接受的章节树、ADR、许可证、版本策略或角色边界；
- Rocky Linux 或 VMware 官方事实与当前基线发生无法在 patch/build 门内消解的冲突；
- 样章结果要求改变全局模板或内容规则，但尚未取得用户批准；
- 实验必须关闭安全控制、使用真实凭据或执行未授权外部写才能成立；
- 需要 push、PR、发布、下载、安装、采购、云资源或 GitHub 设置变更但用户未明确授权；
- 用户要求立即批量生成正文，而样章、模板校正、任务包或审查门尚未完成。

## 12. 接任生效与首要目标

接任在以下条件全部满足后生效：

1. 本交接文件已经提交；
2. 用户把第 13 节完整指令发送到新的 Codex 会话；
3. 新会话完成全部启动门禁；
4. 新会话在首轮回复中明确接受 Phase 2 唯一主会话职责；
5. 用户没有提出交接修订或暂停。

新主会话的唯一首要目标是：

> 在不直接创建正式学习正文或实验的前提下，审计 PRD 的 Phase 2 范围、阶段 00–05 章节职责、模板与实验门，提出“少量样章优先、审查后再分批”的 Phase 2 设计方案；取得用户批准后形成书面设计与实施计划，实施计划再次获批后才签发首批样章任务包。

## 13. 可直接复制的新会话启动指令

```text
你现在接任 C:\Workspace\Projects\cloud-ops-roadmap 的 Phase 2 主会话。

角色与权限：
- 你在 Phase 2 期间是本项目唯一的项目领导者、架构制定者、任务签发者、质量负责人和最终验收者。
- Phase 1 主会话完成交接后不再参与 Phase 2 日常治理。
- 你不承担具体学习正文、实验步骤、项目脚本、配置或图表生产；具体交付必须交给新的独立执行会话。
- 高风险实验、样章门和阶段性成果应由独立审查会话检查，最终裁决仍由你完成。

工作目录：
C:\Workspace\Projects\cloud-ops-roadmap

任何写操作前，按顺序完整阅读：
1. AGENTS.md
2. 项目管理/会话交接/Phase-2-主会话交接.md
3. CODEX-PRD.md
4. 项目管理/验收记录/Phase-1-最终验收报告.md
5. 项目管理/验收记录/Phase-1-独立审查报告.md
6. 项目记忆/MEMORY.md，以及它路由的 decisions.md、patterns.md、open-questions.md、resources.md
7. 项目管理/任务看板.md
8. 版本记录/软件版本基线.md 和 版本记录/更新日志.md
9. 参考资料/来源优先级.md
10. 项目管理/决策记录/README.md 和 ADR-0001 至 ADR-0006
11. AI-CODEX-RULES.md
12. 模板/README.md、章节模板、实验模板、执行报告模板和验收报告模板
13. 知识库/README.md 与阶段 00–05 的六个阶段 README
14. 学习路线/00-学习路线导航.md、01-完整成长路线.md、02-三个月就业路线.md、05-知识前置依赖.md、阶段检查点/README.md
15. 实验手册/README.md 与四个 Level README
16. 脚本资源/项目校验/README.md

随后执行交接文件第 4 节的全部启动门禁，至少确认：
- 当前分支、HEAD、工作区和 origin；
- Phase 1 最终验收提交 4d606b1a8866314ba4d5f2d4aa03f392077762a7 在当前历史中；
- 使用 Git 查询 Phase-2-主会话交接.md 的交接提交，并确认它在当前历史中；
- Python 3.11.15；
- 133/133 仓库校验器单元测试；
- 默认、partial、catalogs、views、complete 全部退出 0；
- complete 为 21/620/817、视图引用 1184、锚点 45、错误 0；
- 七类正式内容目录非 README Markdown 为 0；
- 学习路线和技术索引允许列表无差异；
- 只读远程检查 git ls-remote --heads origin 退出 0。

受限沙箱导致远程检查失败时，只能以完全相同的只读命令合规提升一次；禁止借机 fetch、pull、push、写凭据、关闭安全控制或修改远程。

重新核验 Phase 2 相关官方入口：
- https://rockylinux.org/news/rocky-linux-9-8-ga-release
- https://wiki.rockylinux.org/rocky/version/
- https://blogs.vmware.com/cloud-foundation/2026/05/14/announcing-vmware-workstation-and-fusion-26h1/
- https://knowledge.broadcom.com/external/article?legacyId=80807
- https://knowledge.broadcom.com/external/article/387947/installing-vmware-workstation-pro.html

若 Rocky Linux 当前 minor、VMware 日历发布线、宿主矩阵、许可或下载边界发生变化，只登记证据并判断是否需要独立版本维护或替代 ADR；不得在交接流程中直接修改全局基线。具体 VMware build、宿主安全功能与 Rocky 客体的 environment-verified 证据必须等阶段 03 安装实验门。

必须继承的基线：
- Phase 1 已 accepted，章节树固定为 21 阶段、620 章、817 边；
- 阶段 README 九列表是章节目录唯一权威源，章节 ID 不得在普通正文任务中修改；
- 三个月主线 293、弹性 74，技术类型覆盖 146/146；
- CP/LAB/PRJ 为 21/4/20，项目双向映射 125=125；
- 内容 CC BY-SA 4.0，代码与配置 Apache License 2.0；
- Rocky Linux 9.8 x86_64 与 VMware Workstation Pro 26H1 当前仅 source-verified，不代表安装成功；
- VitePress、GPU、模型和云资源具体组合仍为后续阶段门。

你当前唯一首要目标：
在不直接创建正式学习正文或实验的前提下，审计 PRD 的 Phase 2 范围、阶段 00–05 章节职责、模板与实验门，提出“少量样章优先、审查后再分批”的 Phase 2 设计方案；取得用户批准后形成书面设计与实施计划，实施计划再次获批后才签发首批样章任务包。

当前允许范围：
- Phase 2 范围审计与信息架构；
- 阶段 00–05 内容批次、样章组合、模板适配和验证合同设计；
- 实验等级、环境证据、安全、清理和回退门设计；
- 相关治理记录、书面计划、任务拆分和独立审查设计。

当前禁止：
- 主会话直接编写正文、实验、脚本、配置或图表；
- 样章门 accepted 前批量签发正文任务；
- 创建阶段 06 及以后内容；
- 修改 Phase 1 已接受章节 ID、DAG、路线、索引、锚点或项目映射；
- 修改已接受 ADR、许可证、全局版本策略或 RuoYi/Kubernetes 固定边界；
- 把 source-verified 写成 environment-verified；
- 下载或安装 VMware/Rocky、关闭安全控制、写入凭据或创建云资源；
- push、PR、标签、Release、网站发布或 GitHub 设置修改；
- 与其他主会话并行作出 Phase 2 最终裁决。

停止条件：
- 权威规格冲突无法消解；
- 工作区存在未知修改、固定提交缺失、测试或校验失败、正式内容越界；
- 需要改变 Phase 1 已接受的章节树或全局决定；
- Rocky/VMware 动态事实使设计必须依赖尚未核定的环境组合；
- 样章门尚未建立却需要批量生产；
- 需要外部写但未获用户明确授权。

你的首轮回复只包含：
1. 明确接受 Phase 2 唯一主会话职责；
2. 启动门禁的实际结果和交接提交完整哈希；
3. 从权威文件读取到的 Phase 2 授权与禁止边界；
4. Rocky/VMware 动态变化、冲突或阻塞；
5. 对 Phase 2 样章优先设计工作的下一步建议。

首轮不得创建正文、实验、任务包、更新任务状态或执行远程写。若门禁失败，停止并提供证据，不要猜测或绕过。
```
