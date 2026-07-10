# P0-01 Git、GitHub 远程与项目治理骨架任务包

## 任务信息

- **任务编号：** P0-01
- **所属阶段：** Phase 0
- **状态：** ready
- **执行方式：** 独立新会话
- **前置任务：** 无
- **制定者：** 主会话
- **执行计划：** [Phase 0 治理与仓库骨架实现计划](../执行计划/2026-07-10-Phase-0-治理与骨架-实现计划.md)

## 新会话启动指令

把下面整段原样发送给新会话：

```text
请执行 cloud-ops-roadmap 的 P0-01“Git、GitHub 远程与项目治理骨架”任务。

你的身份是独立执行会话，不是项目领导者。工作目录固定为 C:\Workspace\Projects\cloud-ops-roadmap。你只负责 P0-01，不得执行、规划或提前创建 P0-02 及后续任务的交付物，也不得把任务委派给其他会话。

采取任何写操作前，必须完整阅读以下文件：
1. 根目录 AGENTS.md；
2. 根目录 CODEX-PRD.md；
3. 项目管理/执行计划/2026-07-10-Phase-0-治理与骨架-实现计划.md 中的“执行规则”和“P0-01”；
4. 项目管理/任务包/P0-01-Git与项目治理骨架.md 全文。

严格以任务包中的“允许创建的文件”为写入白名单。禁止修改 AGENTS.md、CODEX-PRD.md、执行计划和任务包；禁止创建学习章节、实验、脚本、图表、模板或其他清单外文件。文件内容修改必须使用 apply_patch。

按实现计划逐步执行 Git 状态检查、Git 初始化、关联并验证 origin、治理文件创建、验证、治理提交、执行报告和报告提交。origin 必须精确设置为 https://github.com/beiyue1988/cloud-ops-roadmap.git；如果已有 origin 指向其他地址，停止并报告，不得覆盖。所有规定验证都必须实际运行并记录退出码与关键输出。若 Git 初始化或远程检查因沙箱权限或网络失败，按工具规则请求权限；不得删除、移动或重建现有 .git 目录来绕过限制。本任务不授权 push、Pull Request 或 GitHub 仓库设置修改。

遇到以下任一情况必须停止并报告主会话，不得自行扩大范围：规格互相冲突、需要清单外文件、需要改变全局规则、验证无法通过、发现敏感信息或连续三次遇到同一外部阻塞。

结束前生成 项目管理/执行报告/P0-01-执行报告.md，并按任务包要求完成两个提交。最终回复必须给出执行报告路径、治理提交哈希、报告提交哈希、验证通过项数、异常和建议状态 submitted。执行会话无权宣布 accepted，也不得直接更新项目管理/任务看板.md。
```

## 目标与学习者价值

建立可追踪的 Git 与多会话治理基础，使后续每个章节、实验和脚本都有明确任务、文件所有权、证据和验收记录，避免不同会话互相覆盖或擅自扩大范围。

## 范围

- 验证当前 Git 状态；
- 初始化 Git 并设置 `main` 分支；
- 配置 `origin = https://github.com/beiyue1988/cloud-ops-roadmap.git` 并验证远程连通性；
- 创建最小根 README；
- 创建任务、决策、计划、报告、验收和内容审计目录说明；
- 创建稀疏的项目记忆索引；
- 创建双许可证文件；
- 记录 ADR-0001 和 ADR-0002；
- 创建含 P0-01 至 P0-06 的初始任务看板；
- 运行规定验证，并分别提交治理文件和执行报告。

## 非范围

- 不创建学习路线或技术索引正文；
- 不创建知识章节、实验、项目代码、脚本、图表或面试题；
- 不创建内容模板；
- 不核验软件版本；
- 不修改全局规格和治理规则。
- 不执行 push，不创建 Pull Request，不修改 GitHub 仓库设置。

## 允许创建的文件

```text
README.md
LICENSE
LICENSE-CONTENT
LICENSE-CODE
THIRD-PARTY-NOTICES.md
项目管理/README.md
项目管理/任务看板.md
项目管理/决策记录/README.md
项目管理/决策记录/ADR-0001-主会话与执行会话分离.md
项目管理/决策记录/ADR-0002-双许可证策略.md
项目管理/执行计划/README.md
项目管理/任务包/README.md
项目管理/执行报告/README.md
项目管理/验收记录/README.md
项目管理/内容审计/README.md
项目记忆/MEMORY.md
项目记忆/decisions.md
项目记忆/patterns.md
项目记忆/resources.md
项目记忆/open-questions.md
项目记忆/deprecated.md
项目管理/执行报告/P0-01-执行报告.md
```

除 Git 元数据外，不允许修改或创建清单外文件。

## 必须参考的官方资料

- CC BY-SA 4.0：<https://creativecommons.org/licenses/by-sa/4.0/>
- Apache License 2.0 应用说明：<https://www.apache.org/legal/apply-license>
- RuoYi-Vue v3.9.2 Release：<https://gitee.com/y_project/RuoYi-Vue/releases/tag/v3.9.2>
- RuoYi-Vue MIT License：<https://gitee.com/y_project/RuoYi-Vue/blob/master/LICENSE>

许可文本和第三方声明必须根据上述官方来源编写，不使用博客转载版本。

## 内容要求

### 根 README

包含：项目定位、当前阶段、权威规范、如何参与、许可证。必须链接 `AGENTS.md`、`CODEX-PRD.md`、`项目管理/任务看板.md` 和根目录许可文件，并明确 Phase 1 才建设完整学习导航。

### 任务看板

表格字段：任务编号、名称、Phase、状态、前置、文件所有权、执行报告、验收记录。

初始任务：

- P0-01：`ready`；
- P0-02 至 P0-06：`planned`。

本任务执行结束时不要自行把 P0-01 改成 `accepted`。执行报告提交后由主会话更新状态。

### ADR-0001

必须包含：

- 状态：`accepted`；
- 背景：长周期知识库由多个新会话交付，单一长会话不能作为可靠记忆；
- 决定：主会话治理与验收，独立新会话执行，高风险任务独立审查；
- 后果：文件所有权清晰但需要任务包和验收开销；
- 复审触发：协作工具或工作流发生实质变化。

### 双许可证与 ADR-0002

- 原创 Markdown 正文、学习说明和原创图表采用 CC BY-SA 4.0；
- 原创脚本、配置、代码文件和明确标记的代码片段采用 Apache License 2.0；
- `LICENSE` 说明两类许可的适用范围；
- `LICENSE-CONTENT` 引用 CC BY-SA 4.0 官方许可；
- `LICENSE-CODE` 保存 Apache License 2.0 官方文本；
- `THIRD-PARTY-NOTICES.md` 记录 RuoYi-Vue v3.9.2、官方 Gitee 地址、release commit `0e2d75c` 和 MIT License；
- ADR-0002 记录双许可证选择、第三方内容不被再许可，以及未来新增第三方素材必须登记来源和许可证。

### 项目记忆

- `MEMORY.md` 不超过 80 行，只做索引；
- `decisions.md` 链接 ADR-0001 和 ADR-0002；
- `open-questions.md` 只保留 GPU 云实例、GPU 型号和目标模型匹配一个阶段性决策门；同时记录 VitePress、双许可证、RuoYi-Vue v3.9.2、阿里云预算不阻塞、GPU 使用云上租用资源五项已确认决定；
- 所有记忆文件声明不保存凭据和敏感数据。

## Git 初始化要求

当前已知状态：根目录存在空 `.git` 目录，但 `git rev-parse --is-inside-work-tree` 返回失败。

执行：

```powershell
git init
git branch -M main
git rev-parse --is-inside-work-tree
$expectedRemote = 'https://github.com/beiyue1988/cloud-ops-roadmap.git'
$existingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
  if ($existingRemote -ne $expectedRemote) {
    Write-Error "origin 已存在但地址不同：$existingRemote"
    exit 1
  }
} else {
  git remote add origin $expectedRemote
}
git remote get-url origin
git ls-remote origin
```

预期仓库检查输出 `true`，远程 URL 完全匹配，`git ls-remote origin` 退出码为 `0`；空仓库可以没有引用输出。如果沙箱禁止写入 `.git` 或网络检查失败，按工具规则请求权限；不得删除、重命名或绕开 `.git`。本任务不执行 push。

## 验收标准

1. Git 仓库有效，当前分支为 `main`；
2. `origin` 精确指向 `https://github.com/beiyue1988/cloud-ops-roadmap.git`，`git ls-remote origin` 通过，且没有执行 push；
3. 允许文件全部存在，清单外没有新增内容；
4. 任务看板列出 P0-01 至 P0-06；
5. ADR-0001 完整记录已批准的职责分离；
6. ADR-0002、许可文件和 RuoYi-Vue 第三方声明完整；
7. `MEMORY.md` 不超过 80 行且只做索引；
8. 1 个阶段性决策门和 5 项已确认决定完整；
9. `git diff --check` 通过；
10. 治理文件提交信息为 `chore: bootstrap project governance`；
11. 生成 `项目管理/执行报告/P0-01-执行报告.md`，写入治理文件提交哈希，并以 `docs: add P0-01 execution report` 单独提交；
12. 未生成任何正式学习内容。

## 必须运行的验证

```powershell
git rev-parse --is-inside-work-tree
git branch --show-current
git remote get-url origin
git ls-remote origin
$required = @(
  'README.md',
  'LICENSE',
  'LICENSE-CONTENT',
  'LICENSE-CODE',
  'THIRD-PARTY-NOTICES.md',
  '项目管理\任务看板.md',
  '项目管理\决策记录\ADR-0001-主会话与执行会话分离.md',
  '项目管理\决策记录\ADR-0002-双许可证策略.md',
  '项目记忆\MEMORY.md',
  '项目记忆\open-questions.md',
  '项目管理\执行报告\P0-01-执行报告.md'
)
$missing = @($required | Where-Object { -not (Test-Path $_) })
$missing
if ($missing.Count -gt 0) { exit 1 }
Select-String -Path '项目管理\任务看板.md' -Pattern 'P0-01|P0-02|P0-03|P0-04|P0-05|P0-06'
Select-String -Path '项目记忆\open-questions.md' -Pattern 'GPU实例|VitePress|CC BY-SA|Apache|RuoYi-Vue v3.9.2|预算不阻塞|云上租用'
Select-String -Path 'LICENSE','LICENSE-CONTENT','LICENSE-CODE','THIRD-PARTY-NOTICES.md' -Pattern 'CC BY-SA 4.0|Apache License|RuoYi-Vue|MIT'
git diff --check
git status --short
```

预期：Git 输出 `true` 和 `main`；远程 URL 完全匹配且连通检查退出码为 `0`；无缺失文件；任务、1 个决策门、5 项已确认决定、双许可证和第三方声明全部命中；`git diff --check` 为 0；提交后 `git status --short` 不含本任务文件的未提交修改。

## 执行报告格式

`项目管理/执行报告/P0-01-执行报告.md` 必须包含：

1. 任务编号和结论；
2. 创建文件清单；
3. 每项验收标准对应证据；
4. 实际运行命令、退出码和关键输出；
5. `origin` URL、`git ls-remote` 结果以及“未执行 push”的确认；
6. 治理文件 commit hash；
7. 权限请求或异常；
8. 风险和未解决问题；
9. 对后续 P0-02 的建议，但不得执行 P0-02。

## 完成后的回复

向主会话回复：

```text
P0-01 已提交审查。
执行报告：项目管理/执行报告/P0-01-执行报告.md
治理提交：填写 git log 中 chore: bootstrap project governance 对应的实际哈希
报告提交：填写 git log 中 docs: add P0-01 execution report 对应的实际哈希
远程仓库：https://github.com/beiyue1988/cloud-ops-roadmap.git，填写连通检查结果并确认未执行 push
验证：填写实际通过项数和总项数
异常：填写“无”或列出具体异常
建议状态：submitted
```

执行会话只能建议 `submitted`，不能宣布 `accepted`。
