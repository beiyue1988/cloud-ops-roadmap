# AI-CODEX-RULES 规则基线实施计划

> **执行要求：** 本计划只能由主会话签发给独立新会话执行。P0-02A 执行会话必须先使用 `executing-plans` 技能逐项实施；规则实现、独立审查和最终验收必须由不同职责完成；主会话不直接编写正式规则正文。

**目标：** 在不复制第二份 PRD、不改变既有项目治理和技术基线的前提下，建立根目录 `AI-CODEX-RULES.md`，把零基础教学、内容研究、写作、图形、实验、安全、来源和验证要求固化为可执行的跨内容规则。

**实施架构：** 主会话先签发 P0-02A；独立执行会话实现规则并提交执行报告；另一个独立审查会话执行 P0-02B；主会话依据两份报告验收规则基线，最后才允许 P0-03 进入 `ready`。

**技术栈：** Markdown、PowerShell、Git。

**批准设计：** [AI-CODEX-RULES.md 设计说明](./2026-07-11-AI-CODEX-RULES-设计说明.md)，批准基线提交 `58a1471c747859c1517679b21c8bc6dea7a76a62`。

---

## 1. 实施边界

### 1.1 权威分层

实施后的职责必须保持为：

1. `AGENTS.md`：会话角色、权限、任务包和验收责任；
2. `CODEX-PRD.md`、ADR 与版本基线：项目范围、信息架构、阶段、产品决策和版本；
3. `AI-CODEX-RULES.md`：跨内容任务的研究、写作、可视化、安全、验证和完成声明；
4. `模板/`：具体文档类型的字段与结构，由 P0-03 创建；
5. 任务包：本次任务的文件白名单、验证命令、停止条件和交付格式。

冲突优先级必须是：用户当前明确指令 > 根 `AGENTS.md` > 已批准 PRD、ADR、版本基线 > `AI-CODEX-RULES.md` > 已批准模板 > 当前任务包的补充要求。任务包可以收紧范围，但不能改写上层规则。

### 1.2 本计划包含

- 建立 `AI-CODEX-RULES.md`；
- 在既有治理入口中增加最小化的规则路由；
- 记录候选文件条款的去向，不复制候选文件；
- 为规则建立自动检查和人工审查门禁；
- 建立 P0-02A 实现任务与 P0-02B 独立审查任务；
- 规则基线验收后，把 P0-03 的前置条件改为规则基线已接受。

### 1.3 本计划不包含

- 不创建学习章节、实验、项目脚本、配置、图表或面试内容；
- 不创建 P0-03 模板；
- 不创建 P0-04 校验工具；
- 不创建 P0-05 软件版本基线；
- 不改写阶段结构、五个贯穿项目、Front Matter 字段或版本结论；
- 不把桌面候选 `AGENTS.md` 或 `AI-CODEX-RULES.md` 复制进仓库；
- 不 push、不创建 Pull Request、不发布站点、不修改 GitHub 设置。

---

## 2. 任务与状态模型

在正式实施前，主会话应把下列两个治理子任务加入任务看板：

| 任务编号 | 名称 | 前置 | 执行者 | 结果 |
|---|---|---|---|---|
| P0-02A | AI 内容写作与验证规则基线 | P0-02 `accepted`、设计已批准 | 独立执行会话 | 规则文件、治理路由、执行报告 |
| P0-02B | AI 规则基线独立审查 | P0-02A `submitted` | 不参与 P0-02A 的独立审查会话 | 独立审查报告 |

P0-03 的前置条件应调整为：P0-02 `accepted`、P0-02A `accepted`、P0-02B `accepted`。在主会话完成最终验收前，P0-03 必须保持 `planned`。

状态责任：

- P0-02A 执行会话只能建议 `submitted`；
- P0-02B 审查会话只能建议 `passed`、`passed-with-notes` 或 `changes-required`；
- 只有主会话可以把 P0-02A、P0-02B 标为 `accepted`，并把 P0-03 标为 `ready`。

---

## 3. 预检基线

### Task 1：主会话签发任务包并锁定状态

**主会话允许修改：**

- 创建：`项目管理/任务包/P0-02A-AI内容写作与验证规则基线.md`
- 创建：`项目管理/任务包/P0-02B-AI规则基线独立审查.md`
- 修改：`项目管理/任务看板.md`

**步骤 1：确认批准设计和仓库状态**

运行：

```powershell
git status --short --branch
git branch --show-current
git remote get-url origin
git show -s --format='%H %s' 58a1471c747859c1517679b21c8bc6dea7a76a62
```

预期：工作区干净；分支为 `main`；远程为 `https://github.com/beiyue1988/cloud-ops-roadmap.git`；设计提交可达。

**步骤 2：创建 P0-02A 任务包**

任务包必须包含完整的新会话启动指令，并把本计划第 4、5、6、7 节转化为执行白名单、规则结构、验证命令、提交要求和停止条件。不得要求执行会话自行从候选文件猜测规则。

P0-02A 的唯一写入白名单：

```text
AI-CODEX-RULES.md
AGENTS.md
CODEX-PRD.md
README.md
项目记忆/patterns.md
项目管理/执行报告/P0-02A-执行报告.md
```

执行会话禁止修改任务看板、任务包、设计说明、实施计划和验收记录。

**步骤 3：创建 P0-02B 任务包**

P0-02B 必须是独立只读审查。除审查报告外不得修改 P0-02A 交付物。

P0-02B 的唯一写入白名单：

```text
项目管理/验收记录/P0-02B-独立审查报告.md
```

**步骤 4：更新任务看板**

- 增加 P0-02A，状态 `ready`；
- 增加 P0-02B，状态 `planned`；
- P0-03 保持 `planned`，前置条件增加 P0-02A、P0-02B `accepted`；
- 不修改已接受任务的结论。

**步骤 5：验证治理签发**

运行：

```powershell
Select-String -LiteralPath '项目管理\任务看板.md' -Pattern 'P0-02A','P0-02B','P0-03'
Select-String -LiteralPath '项目管理\任务包\P0-02A-AI内容写作与验证规则基线.md' -Pattern '新会话启动指令','唯一写入白名单','停止条件','不得 push'
Select-String -LiteralPath '项目管理\任务包\P0-02B-AI规则基线独立审查.md' -Pattern '独立审查','只读','唯一写入白名单','不得修改'
git diff --check
```

**步骤 6：提交治理签发**

提交信息：

```text
docs: issue AI rules baseline tasks
```

---

## 4. P0-02A：规则正文实现

### Task 2：先运行失败门禁，确认规则尚未被隐式实现

**执行会话允许写入：** 无。

**步骤 1：读取必需文件**

完整读取：

```text
AGENTS.md
CODEX-PRD.md
README.md
项目管理/任务包/P0-02A-AI内容写作与验证规则基线.md
项目管理/执行计划/2026-07-11-AI-CODEX-RULES-设计说明.md
项目管理/执行计划/2026-07-11-AI-CODEX-RULES-实施计划.md
项目管理/验收记录/P0-02-验收报告.md
项目记忆/patterns.md
项目管理/任务看板.md
```

桌面候选文件不是权威输入。执行会话不需要重新读取它们；候选条款去向以已批准设计和本计划为准。

**步骤 2：运行启动检查**

```powershell
git status --short --branch
git branch --show-current
git remote get-url origin
Test-Path -LiteralPath 'AI-CODEX-RULES.md'
Select-String -LiteralPath '项目管理\任务看板.md' -Pattern '^\| P0-02A .*`ready`'
```

预期：工作区干净、分支 `main`、远程正确、规则文件不存在、P0-02A 为 `ready`。任一不符即停止。

**步骤 3：运行预期失败检查**

```powershell
if (Test-Path -LiteralPath 'AI-CODEX-RULES.md') { exit 1 }
$routing = Select-String -Path 'AGENTS.md','CODEX-PRD.md','README.md','项目记忆\patterns.md' -Pattern 'AI-CODEX-RULES.md'
if ($routing) { $routing; exit 1 }
```

预期：命令以 0 退出，证明尚未存在规则正文或治理路由。若规则或路由已存在，停止并交由主会话判断是否发生范围重叠。

### Task 3：创建 `AI-CODEX-RULES.md`

**执行会话允许创建：** `AI-CODEX-RULES.md`

**步骤 1：按固定顺序写入 14 个一级主题**

文件必须保持在 220–300 行，并依次覆盖：

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

**步骤 2：落实内容规则，不机械套模板**

必须明确：

- 70% 实践、30% 理论是全项目方向，不是每个文件的字数配额；
- 技术定位、背景历史、工作原理、安装部署、实验、图和面试模块均按知识类型与学习价值选择；
- 基础理论、软件服务、平台、工具、语言、云服务、方法论和硬件主题不能套同一目录；
- 面向完全小白时，首次出现的术语、命令、参数、占位符、前置条件和验证结果要解释；
- 背景与历史只保留能够解释技术出现、取舍和现状的内容，不写年份堆砌；
- “有图”不等于“每章四张图”；只有关系、层级、流程、状态、拓扑或比较难以用短文本表达时才画图；
- Mermaid 用于简单流程、时序、关系和状态；Draw.io 用于正式架构、网络拓扑、云架构和多边界系统图；
- 正式图不得用 ASCII 画框替代；
- 实验必须有可复现前置、操作、验证、清理和风险提示，但不是每个知识点都强制有独立实验；
- 云资源和 GPU 实验必须写成本边界、停止/释放方式；
- 不得保存密码、Token、Cookie、私钥、AccessKey 或真实个人信息；
- 故障案例必须区分现象、假设、证据、根因、恢复和预防；
- 面试内容必须来自已建立的知识、实验、项目和故障证据，不建立脱离实践的背题库；
- 只对实际运行过的内容声明“已验证”；未运行内容必须降级为静态检查、文档核验或待环境验证；
- 命令、配置、版本、输出、测试和来源不得虚构。

**步骤 3：保持路由式引用**

- 链接已经存在的 `AGENTS.md` 和 `CODEX-PRD.md`；
- 对尚未由 P0-05 创建的 `版本记录/软件版本基线.md` 只使用代码路径引用，不创建失效 Markdown 链接；
- 不嵌入完整 Front Matter schema、章节模板、实验模板、项目模板、目录树、阶段表、项目清单或版本表；
- 不写固定 Kubernetes、Rocky Linux、Python 或其他产品版本；具体版本始终路由到 PRD、ADR 或版本基线。

**步骤 4：执行污染拦截**

下列候选材料中的错误不得进入正式规则：

```text
Kubernetes 初始教学基线：1.35.x
cloud-ops-roadmap-Codex-PRD.md
技术文档/
发现版本冲突时先修正基线
项目 0：
### Phase 6：AI Infra 与 AIOps
```

还不得出现以下语义：

- `AI-CODEX-RULES.md` 高于 `AGENTS.md`、PRD 或版本基线；
- 执行会话可自行修改全局基线；
- 所有章节必须安装、必须实验、必须四张图或必须固定数量面试题；
- 规则文件重新定义 21 阶段、五个项目、Phase 0–7 或 Front Matter 字段。

**步骤 5：运行正文静态验证**

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
git diff --check -- 'AI-CODEX-RULES.md'
```

### Task 4：接入治理入口

**执行会话允许修改：**

- `AGENTS.md`
- `CODEX-PRD.md`
- `README.md`
- `项目记忆/patterns.md`

**步骤 1：最小化修改 `AGENTS.md`**

只增加以下规则，不改写现有角色与治理原则：

- 内容正文、内容模板、实验、项目、故障、面试、图表和内容审查任务，写操作前必须完整阅读根 `AI-CODEX-RULES.md`；
- 纯 Git、目录骨架或治理元数据任务仅在任务包明确要求时读取；
- 若 AI 规则与 AGENTS、PRD、ADR、版本基线冲突，执行会话停止并上报，不自行修订基线。

**步骤 2：最小化修改 `CODEX-PRD.md`**

- 在根文件结构中加入 `AI-CODEX-RULES.md`；
- 在治理或内容生产规范处说明它负责“怎么研究、写作和验证”，PRD 仍负责“做什么”；
- 不复制 AI 规则正文；
- 不改变阶段、项目、Front Matter、版本和状态定义。

**步骤 3：修改 `README.md`**

在治理/贡献入口附近增加一条有效相对链接，说明内容贡献者和执行会话在开始内容任务前应阅读 AI 规则。不扩写 README 为第二份规则手册。

**步骤 4：修改 `项目记忆/patterns.md`**

新增可复用模式“规格与写作规则分层”，记录：

- AGENTS 管角色和权限；
- PRD/ADR/版本基线管产品与技术决策；
- AI 规则管跨内容写作与验证；
- 模板管类型结构；
- 任务包管当前白名单；
- 冲突停止升级，不在下层文件修上层规格。

**步骤 5：保护既有关键治理语句**

运行：

```powershell
Select-String -LiteralPath 'AGENTS.md' -Pattern '主会话不直接编写','执行会话不得直接更新','不得自行 push','AI-CODEX-RULES.md'
Select-String -LiteralPath 'CODEX-PRD.md' -Pattern '知识库','1.36','AI-CODEX-RULES.md'
Select-String -LiteralPath 'README.md','项目记忆\patterns.md' -Pattern 'AI-CODEX-RULES.md'
git diff --check
```

### Task 5：执行 P0-02A 综合验证并提交交付

**步骤 1：检查写入白名单**

在创建执行报告前，`git status --short` 只能包含：

```text
AI-CODEX-RULES.md
AGENTS.md
CODEX-PRD.md
README.md
项目记忆/patterns.md
```

额外文件或缺失文件均视为失败。

**步骤 2：检查 Markdown 相对链接**

对本任务修改的五个 Markdown 文件扫描 Markdown 链接。忽略 `http://`、`https://`、`mailto:` 和页内锚点后，所有相对目标必须存在。`版本记录/软件版本基线.md` 在尚不存在时不得写成 Markdown 链接。

**步骤 3：检查敏感信息与虚假占位**

```powershell
$secretHits = rg -n --hidden -g '!\.git/**' '(AKIA[0-9A-Z]{16}|BEGIN (RSA |OPENSSH )?PRIVATE KEY|access[_-]?key\s*[:=]\s*[^<\s]+|secret[_-]?key\s*[:=]\s*[^<\s]+)' AI-CODEX-RULES.md AGENTS.md CODEX-PRD.md README.md 项目记忆/patterns.md
if ($LASTEXITCODE -eq 0) { $secretHits; exit 1 }
if ($LASTEXITCODE -ne 1) { exit $LASTEXITCODE }

$placeholders = rg -n 'TODO|TBD|待补充|稍后完善|这里填写' AI-CODEX-RULES.md AGENTS.md CODEX-PRD.md README.md 项目记忆/patterns.md
if ($LASTEXITCODE -eq 0) { $placeholders; exit 1 }
if ($LASTEXITCODE -ne 1) { exit $LASTEXITCODE }
```

**步骤 4：检查规则没有变成第二份 PRD**

人工逐项确认：

- 没有完整阶段表、项目表、目录树、版本表或 Front Matter schema；
- 没有重新定义状态集合、提交工作流或会话权限；
- 没有详细 Shell/Python/YAML 编码规范；
- 没有固定章节、实验、项目或面试题结构；
- 候选材料的有价值原则已覆盖，冲突条款已排除或迁移。

**步骤 5：提交规则和治理路由**

提交信息：

```text
docs: add AI content writing rules baseline
```

提交必须只包含 Task 3 和 Task 4 的五个文件。

**步骤 6：创建执行报告**

创建 `项目管理/执行报告/P0-02A-执行报告.md`，至少记录：

- 实际修改文件；
- 规则正文行数；
- 14 个主题覆盖结果；
- 候选条款吸收、迁移、纠正、舍弃清单；
- 必需词和禁止词检查；
- 治理路由和既有关键语句保护；
- 链接、敏感信息、占位符、`git diff --check` 结果；
- 规则提交完整哈希；
- 异常、风险、未决问题；
- 建议状态 `submitted`。

报告正文不记录报告提交自身哈希；报告提交哈希由最终回复给出并由主会话写入验收记录。

**步骤 7：提交执行报告**

提交信息：

```text
docs: add P0-02A execution report
```

提交后运行：

```powershell
git log -5 --oneline
git show --stat --oneline HEAD~1
git show --stat --oneline HEAD
git status --short
```

预期：两个规定提交均存在，最终工作区干净，未 push。

---

## 5. P0-02B：独立审查

### Task 6：独立审查规则基线

**执行者：** 未参与 P0-02A 的新会话。

**唯一允许创建：** `项目管理/验收记录/P0-02B-独立审查报告.md`

**禁止：** 不修改规则正文、治理文件、任务看板、任务包、PRD 或执行报告；发现问题只记录，不顺手修复。

**步骤 1：读取审查输入**

完整读取：

```text
AGENTS.md
CODEX-PRD.md
AI-CODEX-RULES.md
README.md
项目管理/任务包/P0-02B-AI规则基线独立审查.md
项目管理/执行计划/2026-07-11-AI-CODEX-RULES-设计说明.md
项目管理/执行计划/2026-07-11-AI-CODEX-RULES-实施计划.md
项目管理/执行报告/P0-02A-执行报告.md
项目记忆/patterns.md
```

**步骤 2：复跑 P0-02A 自动检查**

复跑行数、必需主题、禁止词、治理关键语句、链接、敏感信息、占位符和 `git diff --check` 检查。审查报告记录命令、退出码和关键输出，不引用执行报告的结论代替复验。

**步骤 3：执行独立人工审查**

逐项判断：

1. 权威优先级是否正确，是否存在治理倒置；
2. 是否真正面向零基础，而非只声明“零基础”；
3. 是否允许按知识类型自适应，而非机械十一段或十八段模板；
4. 是否合理保留背景、历史与演进；
5. 是否明确何时用图、何时不用图；
6. 是否能防止命令、配置、版本、输出和验证结果被虚构；
7. 是否区分官方核验、静态检查、环境验证和生产验证；
8. 是否覆盖云/GPU 成本、资源清理和敏感信息；
9. 故障、企业场景和面试内容是否有证据来源；
10. 是否仍是一份写作与验证规则，而不是第二份 PRD、模板库或编码规范；
11. 是否保留现有 AGENTS 的职责分离与禁止自验收规则；
12. 是否未改变 PRD 的 21 阶段、五个项目、Front Matter 和版本基线。

**步骤 4：形成审查结论**

报告必须把问题分为：

- 阻塞：违反治理、错误版本/路径、不可执行、存在安全风险；
- 必须修改：会造成内容长期漂移或验收失真；
- 建议修改：不阻塞基线，但可提升清晰度；
- 通过项：有直接证据支持。

建议结论只能是：

- `passed`：无阻塞、无必须修改；
- `passed-with-notes`：无阻塞、无必须修改，仅有建议；
- `changes-required`：存在阻塞或必须修改。

**步骤 5：提交独立审查报告**

提交信息：

```text
docs: review AI content writing rules baseline
```

提交后确认工作区干净、未 push，并把提交完整哈希交给主会话。

---

## 6. 返工路径

### Task 7：仅在 P0-02B 为 `changes-required` 时执行

主会话先审查问题是否成立，再签发 P0-02A-R1 返工任务包。不得直接把审查意见发送给原执行会话并允许其自由修改。

返工任务包必须：

- 逐条引用已接受的问题；
- 重新限定允许文件；
- 要求复跑全部自动检查，而非只检查修复点；
- 生成独立返工报告；
- 由 P0-02B 审查会话或另一个独立会话复审。

返工提交信息：

```text
docs: revise AI content writing rules baseline
```

报告提交信息：

```text
docs: add P0-02A-R1 execution report
```

---

## 7. 主会话最终验收

### Task 8：接受规则基线并解锁 P0-03

**主会话允许修改：**

- 创建：`项目管理/验收记录/P0-02A-验收报告.md`
- 修改：`项目管理/任务看板.md`
- 必要时修改：`项目记忆/decisions.md`

**步骤 1：独立核对 Git 范围**

```powershell
git status --short --branch
git log -8 --oneline
git show --name-status --format=fuller <P0-02A规则提交完整哈希>
git show --name-status --format=fuller <P0-02A报告提交完整哈希>
git show --name-status --format=fuller <P0-02B审查提交完整哈希>
```

执行时把尖括号参数替换为执行会话和审查会话提供的真实完整哈希；不得把占位符写入仓库文件。

**步骤 2：主会话复验关键门禁**

至少复验：

- 规则行数 220–300；
- 14 个主题齐全；
- 六个候选污染字符串为 0；
- 五个规则/治理文件范围正确；
- 相对链接失效数为 0；
- 敏感信息和占位符命中为 0；
- AGENTS 角色和权限未被削弱；
- PRD 阶段、项目、Front Matter 和版本未被更改；
- P0-02B 无阻塞或必须修改。

**步骤 3：形成 P0-02A 验收报告**

验收报告记录：

- 三个交付提交哈希；
- 自动检查结果；
- 独立审查结论；
- 主会话对每项阻塞/建议的裁决；
- 是否接受规则基线；
- P0-03 是否可以进入 `ready`。

**步骤 4：更新任务看板**

仅在验收通过时：

- P0-02A → `accepted`；
- P0-02B → `accepted`；
- P0-03 → `ready`；
- P0-03 前置保留 P0-02、P0-02A、P0-02B `accepted`。

若验收不通过：P0-02A 保持 `submitted` 或按 PRD 状态规则调整，P0-03 继续 `planned`。

**步骤 5：提交验收决定**

提交信息：

```text
docs: accept AI content writing rules baseline
```

最终确认 `git status --short` 为空，不执行 push。

---

## 8. 候选条款去向清单

P0-02A 执行报告和 P0-02B 审查报告都必须使用本表核对，不得只写“已吸收精华”。

| 候选主题 | 处理 | 正式归属 |
|---|---|---|
| 全项目 70% 实践、30% 理论 | 吸收并澄清非逐文件配额 | `AI-CODEX-RULES.md` |
| 零基础术语、命令、参数解释 | 吸收 | `AI-CODEX-RULES.md` |
| 技术背景、历史和演进选择 | 吸收 | `AI-CODEX-RULES.md` |
| 按理论/服务/平台/工具/语言/云/方法论/硬件自适应 | 吸收 | `AI-CODEX-RULES.md` |
| Mermaid 与 Draw.io 分工 | 吸收原则 | `AI-CODEX-RULES.md` |
| Draw.io 配色、字体、导出规格 | 迁移 | P0-03 图表模板或企业规范 |
| 来源优先级、动态核验、过时标记 | 吸收 | `AI-CODEX-RULES.md` |
| 安全、清理、云成本、GPU 成本、敏感信息 | 吸收 | `AI-CODEX-RULES.md` |
| Front Matter 完整字段和状态值 | 迁移 | PRD 与 P0-03 模板 |
| 章节、实验、项目的固定详细结构 | 迁移并去机械化 | P0-03 各类型模板 |
| Shell/Python/YAML 详细编码规范 | 迁移 | 后续脚本模板或企业规范 |
| 目录、阶段、项目、版本和 Phase | 舍弃重复定义 | 仅 PRD/ADR/版本基线 |
| Kubernetes 1.35.x | 纠正并禁止进入 | 当前 PRD/未来版本基线 |
| `cloud-ops-roadmap-Codex-PRD.md` | 纠正为现有文件 | `CODEX-PRD.md` |
| `技术文档/` | 纠正为现有单一正文源 | `知识库/` |
| AI 规则高于 PRD | 舍弃 | 以本计划第 1.1 节为准 |
| 执行会话主动修订基线 | 舍弃 | 冲突时停止并上报 |
| 新增项目 0 或重写 Phase | 舍弃 | 维持已批准 PRD |

---

## 9. 完成定义

只有同时满足以下条件，AI 内容写作规则基线才算完成：

1. 设计说明已获用户批准；
2. P0-02A 任务包和 P0-02B 任务包已由主会话签发；
3. `AI-CODEX-RULES.md` 为 220–300 行并覆盖 14 个规定主题；
4. 五个规则/治理文件的职责清晰且无第二份 PRD；
5. 候选条款去向逐项可追溯；
6. 自动检查全部通过；
7. P0-02A 有独立执行报告和两个规定提交；
8. P0-02B 由不同会话完成，且无阻塞、无必须修改；
9. 主会话完成独立复验和验收报告；
10. 任务看板将 P0-02A、P0-02B 标为 `accepted`；
11. P0-03 只有在上述条件完成后才进入 `ready`；
12. 全过程未 push、未创建 PR、未发布站点、未修改 GitHub 设置；
13. 最终工作区干净。
