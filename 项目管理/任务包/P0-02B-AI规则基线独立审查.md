# P0-02B AI 规则基线独立审查任务包

## 任务信息

- **任务编号：** P0-02B
- **所属阶段：** Phase 0
- **状态：** ready
- **执行方式：** 独立新会话，只读审查；不得由 P0-02A 执行会话承担
- **前置任务：** P0-02A `submitted`，且主会话将本任务状态更新为 `ready`
- **制定者：** 主会话
- **设计说明：** [AI-CODEX-RULES.md 设计说明](../执行计划/2026-07-11-AI-CODEX-RULES-设计说明.md)
- **实施计划：** [AI-CODEX-RULES 规则基线实施计划](../执行计划/2026-07-11-AI-CODEX-RULES-实施计划.md)

> 本任务已于 2026-07-11 由主会话解锁。P0-02A 已提交审查，提交范围初审通过，任务看板中的 P0-02B 已进入 `ready`；现在可以交给未参与 P0-02A 的新会话执行。

## 解锁记录

- **P0-02A 规则提交：** `bd23ca178eba99fa207a483af9ba9e1386c596e0`
- **P0-02A 报告提交：** `0c2b3761f0fb6737d963599874a4f7c971983537`
- **主会话范围初审：** 规则提交 5 个文件、报告提交 1 个文件，均与白名单完全一致；规则 226 行、14 个主题、候选污染 0、失效链接 0、敏感信息 0、占位符 0；工作区干净。
- **初审边界：** 只确认范围和机械门禁，不代表规则基线已接受；P0-02B 仍须独立复跑命令并完成人工语义审查。

## 新会话启动指令

当主会话把 P0-02B 标为 `ready` 后，把下面整段原样发送给一个未参与 P0-02A 的新 Codex 会话：

```text
请执行 cloud-ops-roadmap 的 P0-02B“AI 规则基线独立审查”任务。

你的身份是独立审查会话，不是 P0-02A 执行者、项目领导者或最终验收者。你必须没有参与 P0-02A 的规则编写。工作目录固定为 C:\Workspace\Projects\cloud-ops-roadmap。你只负责复验 P0-02A 的交付并形成审查报告，不得修复发现的问题，不得执行 P0-03 或任何后续任务，不得把审查委派给其他会话。本任务是用户已批准治理流程的一部分，明确在当前 main 分支和固定工作目录执行；不得另建分支或 Git worktree。

采取任何写操作前，必须完整阅读：
1. 根目录 AGENTS.md；
2. 根目录 CODEX-PRD.md；
3. 根目录 AI-CODEX-RULES.md；
4. 根目录 README.md；
5. 项目管理/任务包/P0-02B-AI规则基线独立审查.md 全文；
6. 项目管理/执行计划/2026-07-11-AI-CODEX-RULES-设计说明.md 全文；
7. 项目管理/执行计划/2026-07-11-AI-CODEX-RULES-实施计划.md 全文；
8. 项目管理/任务包/P0-02A-AI内容写作与验证规则基线.md；
9. 项目管理/执行报告/P0-02A-执行报告.md；
10. 项目记忆/patterns.md；
11. 项目管理/任务看板.md。

唯一目标：独立判断 AI-CODEX-RULES.md 是否符合批准设计、没有成为第二份 PRD、没有污染既有治理和技术基线，并复跑 P0-02A 的关键自动验证。不能信任执行报告的成功声明代替复验。

本任务原则上只读。唯一允许创建的文件是 项目管理/验收记录/P0-02B-独立审查报告.md。禁止修改 AI-CODEX-RULES.md、AGENTS.md、CODEX-PRD.md、README.md、项目记忆、任务看板、任务包、计划、执行报告或其他文件。所有报告修改必须使用 apply_patch。发现问题只记录证据和建议，不得顺手修复。

启动时运行 git status --short --branch、git branch --show-current、git remote get-url origin，并检查任务看板中 P0-02A 为 submitted、P0-02B 为 ready。预期工作区干净、分支 main、远程正确、P0-02A 执行报告和 AI-CODEX-RULES.md 已存在。被审查的规则提交固定为 bd23ca178eba99fa207a483af9ba9e1386c596e0，报告提交固定为 0c2b3761f0fb6737d963599874a4f7c971983537；任一条件不符立即停止。

你必须复跑规则行数、14 主题、必需词、禁止词、治理关键语句、相对链接、敏感信息、占位符和 git diff --check 检查；必须独立检查规则优先级、零基础教学、自适应结构、背景历史、可视化、真实性与来源、验证等级、安全成本、故障与面试内容，以及规则是否重复 PRD/模板/版本基线。不得因为命令退出 0 就跳过人工语义审查。

审查问题分为阻塞、必须修改、建议修改和通过项。结论只能是 passed、passed-with-notes 或 changes-required：有任何阻塞或必须修改时必须是 changes-required；仅有建议时可以 passed-with-notes；无问题时才是 passed。你只能给出审查建议，不能宣布 P0-02A/P0-02B accepted，也不能把 P0-03 改为 ready。

完成报告后，只提交 项目管理/验收记录/P0-02B-独立审查报告.md，提交信息必须是 docs: review AI content writing rules baseline。不得 push、创建 PR、发布网站或修改 GitHub 设置。结束前确认 git status --short 为空，并在最终回复给出报告路径、审查提交完整哈希、自动复验结果、问题分级、建议结论和远程操作确认。

遇到以下任一情况必须停止：审查者曾参与 P0-02A；任务状态不是 ready；工作区不干净；P0-02A 文件或报告缺失；需要修改报告外文件；发现提交范围与报告不一致且无法只读核实；发现敏感信息；同一外部阻塞连续出现三次。
```

## 目标

由未参与规则编写的会话独立复核 P0-02A，防止以下问题被执行会话自我确认后直接进入全局基线：

- 权威优先级倒置；
- 候选文件的旧版本、旧路径和错误项目结构污染；
- 规则变成第二份 PRD、模板或编码规范；
- 机械要求所有章节安装、实验、配图或固定面试题；
- 缺少技术真实性、来源、安全、成本和验证边界；
- 治理入口改动削弱主会话与执行会话的职责分离。

## 审查范围

- `AI-CODEX-RULES.md` 全文；
- P0-02A 对 `AGENTS.md`、`CODEX-PRD.md`、`README.md`、`项目记忆/patterns.md` 的差异；
- `项目管理/执行报告/P0-02A-执行报告.md` 的证据完整性；
- P0-02A 两个提交的文件范围；
- 自动验证与人工语义验收。

## 非范围

- 不修复问题；
- 不重写规则；
- 不修改任务状态；
- 不审查 P0-03 模板内容；
- 不重新设计项目阶段、技术路线或版本基线；
- 不引入外部动态事实；
- 不执行远程写操作。

## 唯一写入白名单

```text
项目管理/验收记录/P0-02B-独立审查报告.md
```

除此之外只能读取和运行不会修改仓库的检查命令。

## 启动前置

必须同时满足：

1. 审查会话未参与 P0-02A；
2. P0-02A 在任务看板中为 `submitted`；
3. P0-02B 在任务看板中为 `ready`；
4. `AI-CODEX-RULES.md` 与 P0-02A 执行报告存在；
5. 工作区干净；
6. P0-02A 规则提交为 `bd23ca178eba99fa207a483af9ba9e1386c596e0`，报告提交为 `0c2b3761f0fb6737d963599874a4f7c971983537`。

缺少任一条件必须停止。

## 必须复跑的自动检查

### 仓库与提交

```powershell
git status --short --branch
git branch --show-current
git remote get-url origin
git show --name-status --format=fuller bd23ca178eba99fa207a483af9ba9e1386c596e0
git show --name-status --format=fuller 0c2b3761f0fb6737d963599874a4f7c971983537
```

规则提交只能包含：

```text
AI-CODEX-RULES.md
AGENTS.md
CODEX-PRD.md
README.md
项目记忆/patterns.md
```

报告提交只能包含：

```text
项目管理/执行报告/P0-02A-执行报告.md
```

### 规则行数和主题

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
```

### 候选污染

```powershell
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
```

### 治理关键语句

```powershell
Select-String -LiteralPath 'AGENTS.md' -Pattern '主会话不直接编写','执行会话不得直接更新','不得自行 push','AI-CODEX-RULES.md'
Select-String -LiteralPath 'CODEX-PRD.md' -Pattern '知识库','1.36','AI-CODEX-RULES.md'
Select-String -LiteralPath 'README.md','项目记忆\patterns.md' -Pattern 'AI-CODEX-RULES.md'
```

### 敏感信息与占位符

```powershell
$secretHits = rg -n --hidden -g '!\.git/**' '(AKIA[0-9A-Z]{16}|BEGIN (RSA |OPENSSH )?PRIVATE KEY|access[_-]?key\s*[:=]\s*[^<\s]+|secret[_-]?key\s*[:=]\s*[^<\s]+)' AI-CODEX-RULES.md AGENTS.md CODEX-PRD.md README.md 项目记忆/patterns.md
if ($LASTEXITCODE -eq 0) { $secretHits; exit 1 }
if ($LASTEXITCODE -ne 1) { exit $LASTEXITCODE }

$placeholders = rg -n 'TODO|TBD|待补充|稍后完善|这里填写' AI-CODEX-RULES.md AGENTS.md CODEX-PRD.md README.md 项目记忆/patterns.md
if ($LASTEXITCODE -eq 0) { $placeholders; exit 1 }
if ($LASTEXITCODE -ne 1) { exit $LASTEXITCODE }

git diff --check
```

### 相对链接

独立检查本次修改的五个 Markdown 文件。忽略外部链接、邮件链接和页内锚点后，所有相对目标必须存在；失效链接数必须为 0。不得直接复制执行报告中的数字。

## 必须完成的人工审查

逐项给出“通过/不通过/需说明”和证据：

1. 权威优先级是否为用户指令、AGENTS、PRD/ADR/版本基线、AI 规则、模板、任务包；
2. 冲突时是否要求停止升级，而不是执行会话修改上层基线；
3. 是否真正解释零基础写作，而不只是出现“零基础”词语；
4. 是否按知识类型自适应，而非统一十一段、十八段或其他机械模板；
5. 是否合理保留技术背景、历史和演进；
6. 是否明确何时需要图、Mermaid 与 Draw.io 如何分工、何时不画图；
7. 是否禁止虚构命令、配置、版本、输出、来源和验证结果；
8. 是否区分来源核验、静态检查、环境验证、综合实验和生产证据；
9. 是否覆盖实验风险、资源清理、云/GPU 成本与敏感信息；
10. 企业案例、故障和面试内容是否要求来自真实学习产物与证据；
11. 文件是否保持为跨内容写作与验证规则，而非第二份 PRD；
12. 是否没有嵌入完整阶段、项目、目录、Front Matter、版本或状态定义；
13. 是否没有嵌入详细脚本编码规范和固定内容模板；
14. AGENTS 的主会话/执行会话/验收职责是否保持；
15. PRD 的 21 阶段、五个项目、Front Matter、版本和状态是否保持；
16. README 与 patterns 的接入是否最小、清晰、无重复正文；
17. P0-02A 执行报告是否记录命令、退出码、关键输出和真实提交哈希；
18. 候选条款是否按吸收、迁移、纠正、舍弃逐项可追溯。

## 问题分级与结论

### 问题分级

- **阻塞：** 治理倒置、错误版本/路径、范围越界、安全风险、关键规则不可执行；
- **必须修改：** 会造成长期内容漂移、零基础教学失效或验收证据失真；
- **建议修改：** 不影响规则基线启用，但可提升清晰度或维护性；
- **通过项：** 有直接文件、差异或命令证据支持。

### 建议结论

- `passed`：无阻塞、无必须修改、无建议；
- `passed-with-notes`：无阻塞、无必须修改，仅有建议；
- `changes-required`：存在任一阻塞或必须修改。

审查会话无权使用 `accepted`。

## 审查报告要求

`项目管理/验收记录/P0-02B-独立审查报告.md` 必须包含：

1. 任务编号、审查日期、独立性声明；
2. P0-02A 规则提交和报告提交完整哈希；
3. 自动复验命令、退出码、关键输出；
4. 规则行数、必需主题、禁止词、链接、敏感信息、占位符结果；
5. 18 项人工审查逐项结果和证据；
6. 阻塞、必须修改、建议修改、通过项分组；
7. 执行报告与实际仓库的一致性；
8. 风险和未决问题；
9. 建议结论 `passed`、`passed-with-notes` 或 `changes-required`；
10. 明确声明最终验收权属于主会话。

## 提交要求

只提交审查报告，提交信息：

```text
docs: review AI content writing rules baseline
```

禁止 amend P0-02A 提交，禁止修改交付物，禁止 push。

## 停止条件

- 当前会话参与过 P0-02A；
- P0-02B 未被主会话标为 `ready`；
- 工作区不干净、分支或远程不符；
- AI 规则、P0-02A 报告或提交哈希缺失；
- 需要修改审查报告以外的文件；
- 提交范围与执行报告不一致且无法只读核实；
- 发现敏感信息；
- 同一外部阻塞连续出现三次。

## 完成后的回复

```text
P0-02B 独立审查已提交。
审查报告：项目管理/验收记录/P0-02B-独立审查报告.md
审查提交：填写 docs: review AI content writing rules baseline 的完整哈希
规则提交：填写被审查的完整哈希
报告提交：填写被审查的完整哈希
自动复验：填写实际通过项数/总项数，并给出规则行数、失效链接、敏感信息、占位符和候选污染命中数
问题分级：填写阻塞/必须修改/建议修改/通过项数量
建议结论：passed、passed-with-notes 或 changes-required
风险：填写“无”或具体风险
未决问题：填写“无”或具体问题
远程操作：确认未 push、未创建 PR、未发布网站、未修改 GitHub 设置
```

审查会话不能宣布 `accepted`，不能更新任务看板，不能启动 P0-03。
