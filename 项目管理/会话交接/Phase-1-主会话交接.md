# Phase 1 主会话交接

## 1. 交接声明

用户已决定为 Phase 1 新建独立主会话。新会话完成本文件规定的启动门禁并明确接受职责后，将在 Phase 1 期间成为 `cloud-ops-roadmap` 的唯一项目领导者、任务签发者和最终验收者。

Phase 0 主会话负责完成本次交接提交。交接生效后，Phase 0 主会话不再参与 Phase 1 日常治理、任务签发或验收裁决，避免两个主会话同时修改计划、任务状态和项目结论。用户始终可以暂停、替换或重新授权主会话。

## 2. 当前状态与固定对象

- P0-05：`accepted`。
- P0-06：`accepted`。
- Phase 0：`accepted`。
- Phase 1：只解锁导航、路线、完整章节树、技术索引、知识依赖和任务规划；正式学习正文仍未授权批量生产。
- Phase 0 最终验收提交：`a3c04d28461861bdd166d9f2208201dae3c3011f`。
- 交接设计提交：`cf35dcc61884eb2bd3b52485c081b42d49423660`。
- 交接实施计划提交：`8037ae3c51730c911dcdab949c4e9e754e4047b7`。
- 实施计划批准提交：`9d4a6408fb8921d3c1db2fe99a4ad495e8fb7d8b`。
- 官方远程：`https://github.com/beiyue1988/cloud-ops-roadmap.git`。

本文件不能预测包含自身的交接提交哈希。新主会话必须使用 Git 查询本文件最近一次提交，并把实际返回值作为交接提交记录。

权威状态入口：

- [Phase 0 最终验收报告](../验收记录/Phase-0-最终验收报告.md)
- [任务看板](../任务看板.md)
- [交接设计说明](../执行计划/2026-07-13-Phase-1主会话交接-设计说明.md)
- [交接实施计划](../执行计划/2026-07-13-Phase-1主会话交接-实施计划.md)

## 3. 必读文件与读取顺序

新主会话必须完整读取以下文件，不得只依赖本交接摘要：

1. [AGENTS.md](../../AGENTS.md)：角色、权限、任务包、执行与验收边界；
2. 本文件：Phase 1 接任状态和启动门禁；
3. [CODEX-PRD.md](../../CODEX-PRD.md)：产品范围、完整阶段、信息架构、质量门禁与治理；
4. [Phase 0 最终验收报告](../验收记录/Phase-0-最终验收报告.md)：已接受基线与 Phase 1 解锁边界；
5. [项目记忆索引](../../项目记忆/MEMORY.md)，以及其路由的 [decisions.md](../../项目记忆/decisions.md)、[patterns.md](../../项目记忆/patterns.md)、[open-questions.md](../../项目记忆/open-questions.md) 和 [resources.md](../../项目记忆/resources.md)；
6. [任务看板](../任务看板.md)：任务状态唯一权威来源；
7. [软件版本基线](../../版本记录/软件版本基线.md)与[来源优先级](../../参考资料/来源优先级.md)；
8. [ADR 索引](../决策记录/README.md)及 ADR-0001 至 ADR-0005；
9. [Kubernetes 分层版本策略](../执行计划/2026-07-13-Kubernetes分层版本策略-设计说明.md)；
10. [AI-CODEX-RULES.md](../../AI-CODEX-RULES.md)和[模板说明](../../模板/README.md)：约束 Phase 1 的任务设计及后续内容交付。

若摘要与权威文件冲突，以运行时系统/开发者指令、用户当前明确指令以及仓库内既定优先级处理；仍无法消解时停止并请用户裁决。

## 4. 启动门禁

新主会话在写入任何文件前必须运行并阅读以下结果：

```powershell
$ErrorActionPreference = 'Stop'
$phase0 = 'a3c04d28461861bdd166d9f2208201dae3c3011f'

git -c core.quotepath=false status --short
git branch --show-current
git rev-parse HEAD
git remote get-url origin
$handoffCommit = git log -1 --format=%H -- '项目管理/会话交接/Phase-1-主会话交接.md'
$handoffCommit
git cat-file -e "$handoffCommit^{commit}"
if ($LASTEXITCODE -ne 0) { exit 1 }
git merge-base --is-ancestor $phase0 HEAD
if ($LASTEXITCODE -ne 0) { exit 1 }
git merge-base --is-ancestor $handoffCommit HEAD
if ($LASTEXITCODE -ne 0) { exit 1 }
python --version
python -B -m unittest discover -s '脚本资源/项目校验/tests' -p 'test_*.py' -v
if ($LASTEXITCODE -ne 0) { exit 1 }
python -B '脚本资源/项目校验/validate_repository.py' .
if ($LASTEXITCODE -ne 0) { exit 1 }

$roots = @('学习路线','技术索引','知识库','实验手册','项目实战','故障案例','面试体系','运维思维训练','企业规范')
$formal = @()
foreach ($root in $roots) {
  if (Test-Path -LiteralPath $root) {
    $formal += Get-ChildItem -LiteralPath $root -Recurse -File -Filter '*.md' |
      Where-Object { $_.Name -ne 'README.md' }
  }
}
Write-Output "formal_non_readme_md=$($formal.Count)"
if ($formal.Count -ne 0) { exit 1 }

git ls-remote --heads origin
```

启动通过条件：

- 工作目录为 `C:\Workspace\Projects\cloud-ops-roadmap`；
- 分支为 `main`，工作区干净；
- origin 与本文件记录一致；
- Phase 0 最终验收提交和查询到的交接提交均为当前 HEAD 祖先；
- Python 与现行校验器基线一致；
- 单元测试 44/44 通过；
- 仓库校验器退出 0、知识章节 0、错误 0；
- 九类正式内容目录的非 `README.md` Markdown 为 0；
- 远程只读检查退出 0。

受限沙箱中的远程检查失败时，只能以完全相同的 `git ls-remote --heads origin` 合规提升一次。禁止关闭安全控制、写入凭据、push 或修改远程。仍失败时如实报告外部阻塞，不伪造结果。

出现未知修改、分支/远程不符、固定提交缺失、测试失败、校验错误、正式正文越界或敏感信息时，不得开始 Phase 1 设计。

## 5. 动态版本门禁

新主会话启动时必须重新打开以下一手入口：

- <https://kubernetes.io/releases/1.36/>
- <https://kubernetes.io/releases/patch-releases/>
- <https://containerd.io/releases/>
- <https://docs.tigera.io/calico/latest/getting-started/kubernetes/requirements>

处理规则：

1. 如果 Kubernetes 页面只有未来计划 patch，不修改版本基线；
2. 如果新的 1.36 patch 已正式发布，登记独立版本维护任务，在任何“当前 patch”正文、实验或任务包产生前更新并验证版本入口；
3. 与具体 patch 无关的 Phase 1 信息架构设计可以继续；
4. 如果 minor、containerd LTS 线、Calico minor 或主实验组合需要变化，必须通过替代 ADR；
5. 官方兼容交集失效时停止相关结论，不自行更换组件。

当前交接不声称 Kubernetes、containerd 或 Calico 已完成环境验证。

## 6. Phase 1 授权范围

当前只授权设计与规划：

- 总学习导航；
- 运维职业成长路线；
- 三个月就业路线；
- 完整阶段与章节树；
- 技术索引；
- 知识前置依赖；
- 贯穿项目演进线与章节映射；
- 对应任务拆分、依赖、优先级、文件所有权、审查门和验收标准；
- 与以上成果直接相关的设计说明、实施计划、任务包、审查与治理记录。

Phase 1 设计若提出样章验证，仍须经过：新主会话设计 → 用户批准 → 书面规格 → 实施计划 → 完整任务包 → 独立执行会话 → 内容审查 → 主会话验收。

## 7. 当前禁止范围

- 不批量编写正式学习正文；
- 不直接编写实验、项目、故障案例、面试题、脚本、配置或图表；
- 不绕过样章与审查门；
- 不擅自修改 Phase 0 已接受结论、项目定位、双许可证、ADR 或全局版本策略；
- 不把来源核验表述为环境验证或生产经验；
- 不选择具体 GPU/模型组合，除非到达批准的阶段决策门；
- 不 push、不创建 Pull Request、标签、Release，不发布网站、不修改 GitHub 设置；
- 不采购或创建阿里云资源；
- 不与另一个主会话并行修改同一治理文件或作出相互竞争的最终裁决。

## 8. 已接受基线与未决门禁

### 治理和产品决定

- [ADR-0001](../决策记录/ADR-0001-主会话与执行会话分离.md)：主会话治理和验收，具体任务由独立新会话执行；
- [ADR-0002](../决策记录/ADR-0002-双许可证策略.md)：原创内容与图表 CC BY-SA 4.0，原创代码与配置 Apache License 2.0；
- [ADR-0003](../决策记录/ADR-0003-VitePress文档站.md)：文档站采用 VitePress，具体依赖仍是阶段门；
- [ADR-0004](../决策记录/ADR-0004-Kubernetes-1.36教学基线.md)：Kubernetes 1.36 minor 和已批准配套组合是主实验基线；
- [ADR-0005](../决策记录/ADR-0005-RuoYi-Vue-v3.9.2教学基线.md)：贯穿项目固定 RuoYi-Vue v3.9.2、commit `0e2d75c`，默认不提交完整上游源码。

### Kubernetes 四层教学角色

1. 核心概念：尽量版本中立；
2. 主实验环境：Kubernetes 1.36.x；
3. 企业兼容参考：Kubernetes 1.35.x；
4. 历史升级参考：Kubernetes 1.31.14。

1.31.6 只允许出现在明确旧案例中，不得成为项目推荐安装版本。主实验环境唯一，不表示企业只能使用 1.36，也不表示所有概念属于 1.36。

### 唯一非阻塞阶段决策门

AI Infra 实验进入 `ready` 前，必须核定阿里云 GPU ECS 实例族、GPU 型号、显存、地域库存、执行日价格、目标模型规模以及 NVIDIA/CUDA/PyTorch/vLLM 兼容交集。预算不构成项目级阻塞，但实验必须提供资源释放步骤；不得在记忆或仓库保存云 AccessKey。

该门不阻塞 Phase 1 信息架构设计。

## 9. 新主会话的唯一首要目标

> 在不创建正式学习正文的前提下，审计 PRD 的 Phase 1 范围和现有目录职责，提出 Phase 1“导航与完整大纲”的设计方案，取得用户批准后形成书面设计与实施计划。

建议顺序：

1. 汇报启动门禁、交接提交、继承边界和动态版本结果；
2. 审计 PRD、目录 README、模板与现有路线约束；
3. 逐项确认导航、章节编号、颗粒度、知识依赖和三个月路线裁剪规则；
4. 提出两至三种信息架构方案及权衡，给出推荐；
5. 分节向用户展示设计并取得批准；
6. 写入 Phase 1 设计说明并完成规格自检；
7. 用户复核书面规格后制定实施计划；
8. 实施计划获批后才创建边界清晰的执行任务包。

## 10. 治理、审查与验收责任

新主会话继承以下责任：

- 维护 Phase 1 的目标、范围、设计、优先级和质量门禁；
- 只编辑治理类文件，不直接生产具体教学交付物；
- 为每个执行会话提供完整启动指令、精确白名单、验证和停止条件；
- 让高风险、跨模块或阶段性成果接受独立审查；
- 独立复验执行与审查证据，只有主会话可以更新 `accepted`、`rework` 或 `blocked`；
- 不允许两个会话同时修改同一文件；
- 维护项目记忆，但只保存稳定、可复用且无敏感信息的事实；
- Phase 1 结束时组织阶段审查、最终验收和下一阶段交接。

## 11. 停止条件

遇到以下情况必须停止扩大范围并请求用户裁决：

- 权威文件之间存在无法按优先级消解的冲突；
- 需要改变 Phase 0 已接受的项目定位、许可证、主版本、贯穿项目或角色边界；
- 需要让两个主会话同时拥有 Phase 1 最终裁决权；
- Phase 1 设计依赖尚未核定的动态版本或 GPU/模型组合才能成立；
- 工作区未知修改、固定对象缺失、测试失败、校验失败、正文越界或发现敏感信息；
- 需要 push、PR、发布、采购、云资源或 GitHub 设置变更但用户没有明确授权；
- 用户要求立即批量生产正文，而 Phase 1 设计、样章、任务包或审查门尚未建立。

## 12. 接任生效与 Phase 1 结束

接任在以下条件全部满足后生效：

1. 本交接文件已经提交；
2. 用户把第 13 节完整指令发送到新会话；
3. 新会话完成启动门禁；
4. 新会话在首轮回复中明确接受 Phase 1 唯一主会话职责；
5. 用户没有提出交接修订或暂停。

Phase 1 结束时，新主会话必须组织独立阶段审查，作出最终裁决，更新看板、验收记录和项目记忆，明确下一阶段真正解锁的范围，并在用户选择分阶段主会话时创建新的交接记录。新主会话在下一位主会话明确接任前保持领导责任，避免治理空窗。

## 13. 可直接复制的新会话启动指令

将以下完整内容复制到新的 Codex 会话：

```text
你现在接任 C:\Workspace\Projects\cloud-ops-roadmap 的 Phase 1 主会话。

角色与权限：
- 你在 Phase 1 期间是本项目唯一的项目领导者、架构制定者、任务签发者、质量负责人和最终验收者。
- 原 Phase 0 主会话完成交接后不再参与 Phase 1 日常治理。
- 你不承担具体学习正文、实验、项目脚本、配置或图表生产；具体任务必须交给新的独立执行会话。
- 高风险、跨模块或阶段性成果应由独立审查会话检查，最终裁决仍由你完成。

工作目录：
C:\Workspace\Projects\cloud-ops-roadmap

任何写操作前，按顺序完整阅读：
1. AGENTS.md
2. 项目管理/会话交接/Phase-1-主会话交接.md
3. CODEX-PRD.md
4. 项目管理/验收记录/Phase-0-最终验收报告.md
5. 项目记忆/MEMORY.md，以及它路由的 decisions.md、patterns.md、open-questions.md、resources.md
6. 项目管理/任务看板.md
7. 版本记录/软件版本基线.md
8. 参考资料/来源优先级.md
9. 项目管理/决策记录/README.md 和 ADR-0001 至 ADR-0005
10. 项目管理/执行计划/2026-07-13-Kubernetes分层版本策略-设计说明.md
11. AI-CODEX-RULES.md
12. 模板/README.md

随后执行交接文件第 4 节的全部启动门禁，至少确认：
- 当前分支、HEAD、工作区和 origin；
- Phase 0 最终验收提交 a3c04d28461861bdd166d9f2208201dae3c3011f 在当前历史中；
- 使用 git log 查询 Phase-1-主会话交接.md 的交接提交，并确认它在当前历史中；
- Python 版本；
- 44/44 仓库校验器单元测试；
- 仓库校验器退出 0、知识章节 0、错误 0；
- 九类正式内容目录中非 README.md 学习 Markdown 为 0；
- 只读远程检查 git ls-remote --heads origin 退出 0。

受限沙箱导致远程检查失败时，只能以完全相同的只读命令合规提升一次；禁止 push、写凭据、关闭安全控制或修改远程。

重新核验以下官方入口：
- https://kubernetes.io/releases/1.36/
- https://kubernetes.io/releases/patch-releases/
- https://containerd.io/releases/
- https://docs.tigera.io/calico/latest/getting-started/kubernetes/requirements

若新的 Kubernetes 1.36 patch 已正式发布，登记独立版本维护任务；不得在交接流程中直接修改全局基线。与 patch 无关的 Phase 1 信息架构设计可以继续，但任何“当前 patch”正文、实验或任务包必须先等待版本入口更新。minor 或主组合变化必须走替代 ADR。

你当前唯一首要目标：
在不创建正式学习正文的前提下，审计 PRD 的 Phase 1 范围和现有目录职责，提出 Phase 1“导航与完整大纲”的设计方案，取得用户批准后形成书面设计与实施计划。

当前允许范围：
- 总学习导航；
- 职业成长路线；
- 三个月就业路线；
- 完整阶段与章节树；
- 技术索引；
- 知识前置依赖；
- 贯穿项目演进线与章节映射；
- 相关设计、计划、任务拆分、审查和治理记录。

当前禁止：
- 批量生产正式学习正文；
- 直接编写实验、项目、故障案例、面试题、脚本、配置或图表；
- 修改已接受 ADR、许可证或全局版本策略；
- 选择尚未到门禁的 GPU/模型组合；
- push、创建 PR、标签、Release、发布网站、修改 GitHub 设置或创建云资源；
- 与其他主会话并行作出 Phase 1 最终裁决。

必须保留的基线：
- VitePress 文档站方向，具体依赖版本仍为阶段门；
- 内容 CC BY-SA 4.0、代码 Apache License 2.0；
- RuoYi-Vue v3.9.2 / commit 0e2d75c；
- Kubernetes 概念尽量版本中立，1.36.x 为唯一主实验，1.35.x 为企业兼容参考，1.31.14 为历史升级参考；
- GPU 使用云上租用资源，优先阿里云 GPU ECS；具体实例/GPU/显存/地域/价格/模型组合仍是 AI Infra 实验前的非阻塞决策门。

停止条件：
- 权威规格冲突无法消解；
- 工作区未知修改、固定提交缺失、测试或校验失败、正式正文越界；
- 需要改变 Phase 0 已接受的全局决定；
- 需要外部写操作但未获用户明确授权；
- Phase 1 设计必须依赖尚未核定的 GPU/模型或动态版本才能成立。

你的首轮回复只包含：
1. 明确接受 Phase 1 唯一主会话职责；
2. 启动门禁的实际结果和交接提交完整哈希；
3. 从权威文件读取到的 Phase 1 授权与禁止边界；
4. 发现的冲突、动态版本变化或阻塞；
5. 对 Phase 1 设计工作的下一步建议。

首轮不得创建正文、任务包、更新任务状态或推送远程。若门禁失败，停止并提供证据，不要猜测或绕过。
```
