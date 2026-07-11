# P0-02A AI 内容写作与验证规则基线任务包

## 任务信息

- **任务编号：** P0-02A
- **所属阶段：** Phase 0
- **状态：** ready
- **执行方式：** 独立新会话，禁止与其他写任务并行
- **前置任务：** P0-02 `accepted`，AI 规则设计与实施计划已批准
- **制定者：** 主会话
- **设计说明：** [AI-CODEX-RULES.md 设计说明](../执行计划/2026-07-11-AI-CODEX-RULES-设计说明.md)
- **实施计划：** [AI-CODEX-RULES 规则基线实施计划](../执行计划/2026-07-11-AI-CODEX-RULES-实施计划.md)
- **前置验收：** [P0-02 验收报告](../验收记录/P0-02-验收报告.md)

## 新会话启动指令

把下面整段原样发送给新的 Codex 会话：

```text
请执行 cloud-ops-roadmap 的 P0-02A“AI 内容写作与验证规则基线”任务。

你的身份是独立执行会话，不是项目领导者、规则批准者或验收者。工作目录固定为 C:\Workspace\Projects\cloud-ops-roadmap。你只负责 P0-02A，不得执行 P0-02B、P0-03 或任何后续任务，不得把任务委派给其他会话，也不得与其他写任务并行。开始前必须使用 executing-plans 技能，严格按已批准实施计划执行；提交前使用 verification-before-completion 技能取得新鲜验证证据。本任务是用户已批准、由主会话签发的全局治理任务，明确在当前 main 分支和固定工作目录串行执行；不得另建分支或 Git worktree。若技能的一般建议与本任务的分支、工作目录或禁止委派要求冲突，以根 AGENTS.md、本任务包和用户对实施计划的批准为准。

采取任何写操作前，必须完整阅读以下文件：
1. 根目录 AGENTS.md；
2. 根目录 CODEX-PRD.md；
3. 根目录 README.md；
4. 项目管理/任务包/P0-02A-AI内容写作与验证规则基线.md 全文；
5. 项目管理/执行计划/2026-07-11-AI-CODEX-RULES-设计说明.md 全文；
6. 项目管理/执行计划/2026-07-11-AI-CODEX-RULES-实施计划.md 全文；
7. 项目管理/验收记录/P0-02-验收报告.md；
8. 项目记忆/patterns.md；
9. 项目管理/任务看板.md。

唯一目标：创建根 AI-CODEX-RULES.md，并以最小改动把它接入 AGENTS.md、CODEX-PRD.md、README.md 和 项目记忆/patterns.md。该文件只规定跨内容任务“如何研究、写作、可视化、保证安全和提供验证证据”，不得成为第二份 PRD、模板库、版本基线或编码规范。

唯一写入白名单只有以下 6 个文件：
1. AI-CODEX-RULES.md（创建）；
2. AGENTS.md（修改）；
3. CODEX-PRD.md（修改）；
4. README.md（修改）；
5. 项目记忆/patterns.md（修改）；
6. 项目管理/执行报告/P0-02A-执行报告.md（最后创建）。

禁止修改任务看板、任务包、设计说明、实施计划、验收记录、许可证、版本记录、内容目录 README 或其他文件。禁止创建模板、章节、实验、项目脚本、配置、图表、校验脚本或临时仓库文件。所有文件修改必须使用 apply_patch。不得读取或复制桌面上的 GPT 候选文件；候选条款的取舍已经固化在批准设计、实施计划和本任务包中。

启动时实际运行 git status --short --branch、git branch --show-current、git remote get-url origin、Test-Path AI-CODEX-RULES.md，并检查任务看板中 P0-02A 为 ready。预期工作区干净、分支 main、远程为 https://github.com/beiyue1988/cloud-ops-roadmap.git、规则文件不存在。还要确认 AGENTS.md、CODEX-PRD.md、README.md、项目记忆/patterns.md 尚未引用 AI-CODEX-RULES.md。任一条件不符立即停止，不得覆盖、合并既有实现或自行修订任务包。

AI-CODEX-RULES.md 必须为 220–300 行，按任务包规定的 14 个主题组织。必须覆盖零基础教学、自适应知识结构、背景历史取舍、理论与实践关系、Mermaid/Draw.io 分工、来源与时效核验、实验安全与成本、故障与面试证据、验证等级、禁止模式和停止条件。70% 实践、30% 理论只能解释为全项目方向，不能作为每个文件的机械字数配额。安装、实验、图、面试、背景和故障模块都按知识类型与学习价值选择，不得规定所有章节必须具备。

规则正文不得重新定义 21 个阶段、五个项目、Phase 结构、Front Matter schema、目录树、版本表、状态集合、会话权限或详细编程规范。不得写入固定 Kubernetes、Rocky Linux、Python 等版本；版本只能路由到 PRD、ADR 或未来的版本基线。当前尚不存在的 版本记录/软件版本基线.md 只能用代码路径表示，不能创建失效 Markdown 链接。

必须阻止这些候选污染进入正式规则：Kubernetes 初始教学基线：1.35.x、cloud-ops-roadmap-Codex-PRD.md、技术文档/、发现版本冲突时先修正基线、项目 0：、### Phase 6：AI Infra 与 AIOps。不得表达 AI 规则高于 AGENTS/PRD/ADR/版本基线，也不得授权执行会话修改全局基线。

AGENTS.md 只增加内容类任务的必读门禁和冲突停止规则，不削弱现有主会话/执行会话职责分离。CODEX-PRD.md 只在根结构和治理说明中登记 AI 规则的职责，不复制正文，不改变阶段、项目、Front Matter、版本或状态定义。README.md 只增加有效导航链接。项目记忆/patterns.md 只记录规格、规则、模板、任务包的分层模式。

完成正文和治理路由后，实际运行任务包规定的行数、14 主题、必需词、禁止词、治理关键语句、写入白名单、相对链接、敏感信息、占位符、第二份 PRD 人工检查和 git diff --check。不得以“应该通过”代替运行结果。若验证失败，只能在白名单内修复；若需要修改清单外文件、上层规格或版本基线，立即停止并报告。

验证通过后，把除执行报告外的 5 个文件以 docs: add AI content writing rules baseline 单独提交，并记录完整提交哈希。随后创建 项目管理/执行报告/P0-02A-执行报告.md，只提交该报告，提交信息必须是 docs: add P0-02A execution report。报告正文记录规则提交哈希，不记录报告提交自身哈希；报告提交哈希在最终回复给出。不得 push、创建 Pull Request、发布网站或修改 GitHub 设置。

结束前确认 git status --short 为空。最终回复必须给出执行报告路径、规则提交完整哈希、报告提交完整哈希、规则行数、自动验证通过项数/总项数、候选条款处理结果、异常、风险、未决问题、远程操作确认和建议状态 submitted。你无权宣布 accepted，也不得修改任务看板。

遇到以下任一情况必须停止：规格冲突；启动状态不符；规则或路由已存在；需要白名单外写入；需要改变全局规则或版本；候选材料与批准设计冲突；验证无法在白名单内修复；发现敏感信息；同一阻塞连续出现三次。
```

## 目标与学习者价值

建立统一、简洁、可执行的 AI 内容写作与验证规则，使后续不同执行会话产出的章节、实验、项目、故障、面试和图表能够保持：

- 对完全零基础学习者友好；
- 背景、原理、实践和验证之间有明确关系；
- 不机械套用同一章节结构；
- 不虚构命令、配置、版本、输出或测试结果；
- 能区分文档核验、静态检查、环境验证和生产验证；
- 符合安全、成本、来源与项目治理要求。

## 范围

- 创建根 `AI-CODEX-RULES.md`；
- 将其职责以最小化方式接入 `AGENTS.md`、`CODEX-PRD.md`、`README.md`；
- 在 `项目记忆/patterns.md` 记录可复用的规则分层；
- 运行自动检查和人工检查；
- 形成规则提交和独立执行报告提交。

## 非范围

- 不编写学习正文、实验、项目、故障、面试、图表或脚本；
- 不创建 P0-03 模板；
- 不创建 P0-04 校验工具；
- 不创建 P0-05 版本基线；
- 不修改项目阶段、贯穿项目、Front Matter、版本结论或状态规则；
- 不复制桌面候选文件；
- 不修改任务看板、任务包、计划、验收记录或许可证；
- 不执行任何远程写操作。

## 唯一写入白名单

```text
AI-CODEX-RULES.md
AGENTS.md
CODEX-PRD.md
README.md
项目记忆/patterns.md
项目管理/执行报告/P0-02A-执行报告.md
```

除 Git 元数据外，不允许创建或修改清单外文件。

## 必读规范与基线

1. `AGENTS.md`；
2. `CODEX-PRD.md`；
3. 本任务包；
4. `项目管理/执行计划/2026-07-11-AI-CODEX-RULES-设计说明.md`；
5. `项目管理/执行计划/2026-07-11-AI-CODEX-RULES-实施计划.md`；
6. `项目管理/验收记录/P0-02-验收报告.md`；
7. `项目记忆/patterns.md`；
8. `项目管理/任务看板.md`。

本任务不需要检索外部技术资料。不得引入新的动态版本事实；所有具体版本仍以现有 PRD、ADR 和后续 P0-05 版本基线为准。

## 规则正文结构

`AI-CODEX-RULES.md` 必须在 220–300 行内按顺序覆盖：

1. 文件目的与适用范围；
2. 规则边界、权威分层与冲突停止；
3. 执行前检查与必读输入；
4. 零基础写作原则；
5. 知识类型识别与自适应结构；
6. 背景、历史和技术演进的取舍；
7. 理论、实践和项目之间的关系；
8. 可视化选择与 Mermaid/Draw.io 分工；
9. 技术真实性、来源与时效性核验；
10. 实验、安全、成本、清理与敏感信息；
11. 企业场景、故障案例与面试内容；
12. 验证证据等级与完成声明；
13. 禁止模式与停止条件；
14. 自动检查、人工审查和提交前清单。

可以使用二级、三级标题细分，但不得把内容扩展成第二份 PRD、模板全集或工具编码规范。

## 必须表达的规则

### 教学与结构

- 70% 实践、30% 理论是全项目方向，不是逐文件字数指标；
- 面向完全小白解释首次出现的术语、命令、参数、占位符、前置和验证；
- 基础理论、软件服务、平台、工具、语言、云服务、方法论、硬件主题采用自适应结构；
- 背景和历史只保留能解释“为什么出现、解决什么、为何演进”的内容；
- 安装、实验、企业案例、故障、面试、最佳实践和扩展阅读均为按需模块。

### 可视化

- 图用于表达复杂关系、层级、流程、状态、拓扑和比较，不作装饰；
- Mermaid 用于简单流程、时序、关系和状态；
- Draw.io 用于正式架构、网络拓扑、云架构和多边界系统图；
- 正式材料不得用 ASCII 画框替代图；
- 不强制每个章节固定图数。

### 真实性、来源与验证

- 命令、参数、配置、版本、输出、来源和验证结果不得虚构；
- 动态或易变事实必须依据官方/一手资料核验并记录适用版本或核验日期；
- 区分来源核验、静态检查、环境验证、综合实验和生产证据；
- 只对实际运行过的内容声明“已验证”；
- 无法验证时明确限制、风险和下一步，不用推测冒充结果。

### 安全与成本

- 实验必须说明前置、验证、清理和风险，但不要求每个知识点独立实验；
- 破坏性、权限、安全、网络和数据操作必须包含警示与恢复路径；
- 云资源与 GPU 实验必须说明成本边界和释放方式；
- 不保存密码、Token、Cookie、私钥、云 AccessKey 或真实个人信息。

### 企业、故障与面试

- 企业案例必须说明适用条件和取舍，不能把示例宣称为唯一最佳实践；
- 故障案例区分现象、假设、证据、根因、恢复和预防；
- 面试内容来自知识正文、实验、项目和故障证据，不形成孤立背题库。

## 候选条款处理

执行报告必须逐项记录以下处理，不得只写“已吸收”：

| 候选主题 | 处理 | 归属 |
|---|---|---|
| 70/30、零基础、自适应、背景历史 | 吸收 | AI 规则 |
| Mermaid/Draw.io 的选择原则 | 吸收 | AI 规则 |
| Draw.io 配色、字体和导出细节 | 迁移 | P0-03 图表模板或企业规范 |
| 来源、动态核验、过时标记 | 吸收 | AI 规则 |
| 安全、清理、云/GPU 成本、敏感信息 | 吸收 | AI 规则 |
| Front Matter 完整字段 | 迁移 | PRD 与 P0-03 模板 |
| 章节、实验、项目的详细固定结构 | 迁移并去机械化 | P0-03 模板 |
| Shell/Python/YAML 详细规范 | 迁移 | 后续脚本模板或企业规范 |
| 目录、阶段、项目、版本、Phase | 舍弃重复 | PRD/ADR/版本基线 |
| Kubernetes 1.35.x、旧 PRD 名、`技术文档/` | 纠正并拦截 | 不进入正式规则 |
| AI 规则高于 PRD、执行会话修基线、项目 0、错误 Phase | 舍弃 | 维持现有治理 |

## 治理文件修改要求

### `AGENTS.md`

只增加内容正文、内容模板、实验、项目、故障、面试、图表和内容审查任务的 AI 规则必读门禁，以及冲突停止升级规则。不得修改主会话/执行会话职责、状态责任、文件所有权或远程写限制。

### `CODEX-PRD.md`

只在根结构与治理/内容规范附近登记 AI 规则的职责：PRD 决定“做什么”，AI 规则决定跨内容任务“怎么研究、写作和验证”。不得复制规则正文或改变阶段、项目、Front Matter、版本和状态集合。

### `README.md`

只增加指向根 AI 规则的有效相对链接和一句适用说明，不把 README 扩展为规则副本。

### `项目记忆/patterns.md`

新增“规格与写作规则分层”模式，记录 AGENTS、PRD/ADR/版本基线、AI 规则、模板、任务包的职责及冲突停止原则。

## 必须运行的验证

执行会话必须实际运行并在执行报告中记录退出码和关键输出。

### 启动检查

```powershell
git status --short --branch
git branch --show-current
git remote get-url origin
Test-Path -LiteralPath 'AI-CODEX-RULES.md'
Select-String -LiteralPath '项目管理\任务看板.md' -Pattern '^\| P0-02A .*`ready`'

if (Test-Path -LiteralPath 'AI-CODEX-RULES.md') { exit 1 }
$routing = Select-String -Path 'AGENTS.md','CODEX-PRD.md','README.md','项目记忆\patterns.md' -Pattern 'AI-CODEX-RULES.md'
if ($routing) { $routing; exit 1 }
```

### 行数、主题与污染检查

```powershell
$lineCount = (Get-Content -LiteralPath 'AI-CODEX-RULES.md' -Encoding UTF8).Count
$lineCount
if ($lineCount -lt 220 -or $lineCount -gt 300) { exit 1 }

$required = @(
  '适用范围','规则边界','零基础','自适应','背景','历史','Mermaid','Draw.io',
  '来源','时效','不得虚构','停止条件','安全','成本','敏感信息','证据','人工审查'
)
foreach ($term in $required) {
  if (-not (Select-String -LiteralPath 'AI-CODEX-RULES.md' -SimpleMatch -Pattern $term)) {
    Write-Error "缺少必需主题：$term"
    exit 1
  }
}

$forbidden = @(
  'Kubernetes 初始教学基线：1.35.x',
  'cloud-ops-roadmap-Codex-PRD.md',
  '技术文档/',
  '发现版本冲突时先修正基线',
  '项目 0：',
  '### Phase 6：AI Infra 与 AIOps'
)
foreach ($term in $forbidden) {
  if (Select-String -LiteralPath 'AI-CODEX-RULES.md' -SimpleMatch -Pattern $term) {
    Write-Error "发现候选污染：$term"
    exit 1
  }
}

Select-String -LiteralPath 'AI-CODEX-RULES.md' -Pattern 'AGENTS\.md','CODEX-PRD\.md','版本记录/软件版本基线\.md'
```

### 治理保护检查

```powershell
Select-String -LiteralPath 'AGENTS.md' -Pattern '主会话不直接编写','执行会话不得直接更新','不得自行 push','AI-CODEX-RULES.md'
Select-String -LiteralPath 'CODEX-PRD.md' -Pattern '知识库','1.36','AI-CODEX-RULES.md'
Select-String -LiteralPath 'README.md','项目记忆\patterns.md' -Pattern 'AI-CODEX-RULES.md'
```

### 白名单检查

创建执行报告前，实际变更集合必须与以下五个路径完全相等：

```powershell
$expected = @(
  'AI-CODEX-RULES.md',
  'AGENTS.md',
  'CODEX-PRD.md',
  'README.md',
  '项目记忆/patterns.md'
) | Sort-Object
$actual = @(
  git -c core.quotepath=false status --short |
    ForEach-Object { $_.Substring(3).Replace('\','/') }
) | Sort-Object
$missing = @($expected | Where-Object { $_ -notin $actual })
$extra = @($actual | Where-Object { $_ -notin $expected })
$missing
$extra
if ($missing.Count -ne 0 -or $extra.Count -ne 0) { exit 1 }
```

### 敏感信息与占位符检查

```powershell
$secretHits = rg -n --hidden -g '!\.git/**' '(AKIA[0-9A-Z]{16}|BEGIN (RSA |OPENSSH )?PRIVATE KEY|access[_-]?key\s*[:=]\s*[^<\s]+|secret[_-]?key\s*[:=]\s*[^<\s]+)' AI-CODEX-RULES.md AGENTS.md CODEX-PRD.md README.md 项目记忆/patterns.md
if ($LASTEXITCODE -eq 0) { $secretHits; exit 1 }
if ($LASTEXITCODE -ne 1) { exit $LASTEXITCODE }

$placeholders = rg -n 'TODO|TBD|待补充|稍后完善|这里填写' AI-CODEX-RULES.md AGENTS.md CODEX-PRD.md README.md 项目记忆/patterns.md
if ($LASTEXITCODE -eq 0) { $placeholders; exit 1 }
if ($LASTEXITCODE -ne 1) { exit $LASTEXITCODE }
```

### 相对链接检查

必须检查本任务修改的五个 Markdown 文件。忽略 `http://`、`https://`、`mailto:` 和 `#` 锚点后，所有相对目标必须存在，失效数必须为 0。可以使用只读 PowerShell 内联命令，不得把临时脚本保存到仓库。`版本记录/软件版本基线.md` 尚不存在时不得写成 Markdown 链接。

### 第二份 PRD 人工检查

逐项确认并记录：

1. 没有完整阶段表、项目表、目录树、版本表或 Front Matter schema；
2. 没有重新定义状态集合、提交工作流或会话权限；
3. 没有详细 Shell/Python/YAML 编码规范；
4. 没有固定章节、实验、项目或面试题结构；
5. 没有弱化 AGENTS 的职责分离；
6. 没有改变 PRD 的阶段、项目、Front Matter 和版本结论。

### Git 检查

```powershell
git diff --check
git diff --stat
git -c core.quotepath=false status --short
```

## 提交要求

本任务必须形成两个独立提交：

1. 规则与治理路由：`docs: add AI content writing rules baseline`；
2. 执行报告：`docs: add P0-02A execution report`。

第一个提交只能包含白名单前五个文件。第二个提交只能包含执行报告。禁止 amend 已批准历史，禁止 rebase，禁止 push。

## 执行报告要求

`项目管理/执行报告/P0-02A-执行报告.md` 必须包含：

1. 任务编号、执行日期、建议结论；
2. 六个允许文件的实际处理情况；
3. 规则文件行数与 14 个主题覆盖表；
4. 候选条款“吸收、迁移、纠正、舍弃”逐项清单；
5. 必需词、禁止词、治理保护、白名单、链接、敏感信息、占位符和 `git diff --check` 结果；
6. 第二份 PRD 人工检查结果；
7. 规则提交完整哈希；报告提交自身哈希不写入正文；
8. 实际命令、退出码和关键输出；
9. 异常、风险、权限请求和未决问题；
10. 明确确认未 push、未创建 PR、未发布网站、未修改 GitHub 设置；
11. 建议状态 `submitted`，不得写 `accepted`。

## 验收标准

1. `AI-CODEX-RULES.md` 存在且为 220–300 行；
2. 14 个主题完整，规则面向零基础且允许自适应结构；
3. 背景历史、可视化、来源、验证、安全、成本、故障和面试规则明确；
4. 六个候选污染字符串命中为 0；
5. 文件没有成为第二份 PRD、模板库、版本表或编码规范；
6. 四个治理入口的改动最小且职责正确；
7. AGENTS 的角色、状态和远程限制未被削弱；
8. PRD 的阶段、项目、Front Matter、版本和状态未改变；
9. 白名单缺失/越界为 0，相对链接失效为 0；
10. 敏感信息和占位符命中为 0；
11. `git diff --check` 通过；
12. 两个规定提交存在，最终工作区干净且未执行远程写操作。

## 停止条件

出现任一情况立即停止并报告主会话：

- 启动状态与预期不符；
- `AI-CODEX-RULES.md` 或治理路由已存在；
- 规格、计划、PRD、AGENTS 之间存在无法按优先级解决的冲突；
- 需要修改白名单外文件；
- 需要改变阶段、项目、Front Matter、版本或全局治理；
- 需要引入未经批准的新版本或新工具；
- 验证无法在白名单内修复；
- 发现真实敏感信息；
- 同一外部阻塞连续出现三次。

## 完成后的回复

向主会话回复：

```text
P0-02A 已提交审查。
执行报告：项目管理/执行报告/P0-02A-执行报告.md
规则提交：填写 docs: add AI content writing rules baseline 的完整哈希
报告提交：填写 docs: add P0-02A execution report 的完整哈希
规则行数：填写实际行数
自动验证：填写实际通过项数/总项数，并给出白名单缺失/越界、失效链接、敏感信息、占位符和候选污染命中数
候选条款：填写吸收/迁移/纠正/舍弃的实际核对结果
异常：填写“无”或具体异常
风险：填写“无”或具体风险
未决问题：填写“无”或需要主会话裁决的问题
远程操作：确认未 push、未创建 PR、未发布网站、未修改 GitHub 设置
建议状态：submitted
```

执行会话只能建议 `submitted`，不能宣布 `accepted`，也不能启动 P0-02B。
