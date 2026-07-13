# P1-01-R3 闭合 HTML br 属性边界任务包

## 新会话启动指令

```text
请执行 cloud-ops-roadmap 的 P1-01-R3“闭合 HTML br 属性边界”返工任务。

你的身份是独立返工执行会话，不是项目领导者、规格制定者、代码质量审查者或最终验收者。优先由原 P1-01/R1/R2 执行会话承担；发现本缺陷的主会话不实施产品修复。工作目录固定为 C:\Workspace\Projects\cloud-ops-roadmap，分支固定为 main。只执行本任务，不得扩大范围、委派或并发修改相同文件。

任何写操作前，按顺序完整阅读：
1. AGENTS.md；
2. CODEX-PRD.md，重点第 15、17、18 节；
3. 项目管理/任务包/P1-01-R3-闭合HTML-br属性边界.md；
4. 项目管理/任务包/P1-01-R2-加固大纲解析与诊断边界.md；
5. 项目管理/任务包/P1-01-R1-闭合贯穿项目总视图.md；
6. 项目管理/任务包/P1-01-大纲合同与校验门.md；
7. 项目管理/执行计划/2026-07-13-Phase-1导航与完整大纲-设计说明.md；
8. 项目管理/执行计划/2026-07-13-Phase-1导航与完整大纲-实施计划.md；
9. 项目管理/执行报告/P1-01-R2-执行报告.md；
10. 脚本资源/项目校验/README.md；
11. 脚本资源/项目校验/validate_repository.py；
12. 脚本资源/项目校验/tests/test_validate_repository.py；
13. 模板/执行报告模板.md。

先使用 receiving-code-review 核对固化反例，再用 executing-plans 跟踪；修改实现前必须使用 test-driven-development，先只增加两项规定测试并取得正确红灯；异常时使用 systematic-debugging；提交/完成前使用 verification-before-completion。不得用 brainstorming 改变批准合同。

唯一目标：让单行字段对 HTML `br` 起始标签的识别只依赖标签名及其紧随分隔符，从而拒绝属性值中包含 `<`/`>` 的所有 `br` 变体，同时不误拒绝普通 `br` 文本、`<bracket>`、`<br-description>`、`<br:custom>` 或其他非 `br` 标签名。

唯一写入白名单：
- C:\Workspace\Projects\cloud-ops-roadmap\脚本资源\项目校验\validate_repository.py；
- C:\Workspace\Projects\cloud-ops-roadmap\脚本资源\项目校验\tests\test_validate_repository.py；
- C:\Workspace\Projects\cloud-ops-roadmap\项目管理\执行报告\P1-01-R3-执行报告.md。

校验器 README 必须保持 blob 6d71a07675ddb5ae598fe78007e00e2544d03009。禁止修改 README、旧报告、任务包、看板、设计、计划、PRD、治理文件、版本基线或正式内容；禁止改变围栏屏蔽、迭代图算法、项目视图可比较状态、OL 责任、CLI、公开函数、字段/表头；禁止引入 HTML 解析器、第三方依赖、新模块、schema、CI、配置或仓库内临时文件；禁止删除/跳过/弱化现有 101 项测试；禁止 amend/reset/rebase、push、PR、发布或 GitHub 设置修改。

启动门禁：工作区干净、main、origin 精确为 https://github.com/beiyue1988/cloud-ops-roadmap.git、Python 3.11.15；R2 产品 6ee194a19ed4bf9d3dfccfe80e50494a52b0524b、R2 报告 7192bc324d04017c41ff3b38d7a6b034c5275562 和本任务包提交均在历史；看板 P1-01/R1/R2 为 rework、R3 为 assigned、P1-01B 为 planned；实现、测试、README blob 依次为 1e988a979b7c62decae6ce3827c6b0848005aabb、3fea550e4ee46310c32076d4764fc1ccc4ca31f9、6d71a07675ddb5ae598fe78007e00e2544d03009；101/101、默认、partial 退出 0。任一不符立即停止。

TDD 第一步只能修改测试文件，增加两个独立测试：一项用完整 `complete` 夹具逐个验证 `<br title="<x>">`、`<BR title="<x>" />`、`<br data-note="a > b < c">` 和单引号等变体分别触发原有 OL005/OL002；另一项验证普通 br、`<bracket>`、`<br-description>`、`<br:custom>`、`<brx>` 不误报。当前实现应只在属性尖括号变体测试红灯，合法对照应通过；原 101 项必须全部通过。

随后实施最小修复。识别语义为：大小写不敏感的 `<br` 后一个字符必须是 HTML 标签名分隔符（空白、`/` 或 `>`）；一旦标签名确定为 br，无需也不得解析后续属性值。不得用宽泛 `<br` 前缀误拒绝更长标签名，不得以 `[^<>]` 扫描属性体，不得拒绝全部 HTML。章节标题/目标继续 OL005，派生文本字段继续 OL002。

修复后运行两个目标测试、完整 unittest 至少 103/103且原 101/101、默认两次一致、--help、partial、catalogs 预期 21 OL001、系统临时目录公共 API 正反例、R2 四类主边界抽查、标准库/AST/范围/README blob/正式内容/缓存/diff 检查。所有临时夹具在系统临时目录自动清理。

验证通过后形成两个提交：产品提交只含实现和测试，信息固定 `fix: close HTML break attribute boundary`；报告提交只含 项目管理/执行报告/P1-01-R3-执行报告.md，信息固定 `docs: report P1-01-R3 HTML break closure`。不得改写历史。

报告必须记录固化反例、两项正确红灯、最小标签名边界修复、产品提交完整哈希、至少 103/103与原 101/101、全部变体/合法对照、R2 四类回归、默认/partial/catalogs、README blob、依赖、范围、正式内容、缓存、清理、风险、未决问题、远程写确认和 submitted/rework/blocked 建议。不得宣布 accepted 或启动 P1-01B。

停止条件：身份/门禁/固定对象/blob 不符；反例不成立或红灯原因错误；需要 README/白名单外写入、HTML 解析器、第三方依赖、规则/CLI/公开接口变化或无关重构；原 101 项或 R2 四类边界回归；无法同时拒绝 br 与保留非 br 标签名；敏感信息、并发冲突或外部写需求。

完成回复包含：状态建议；三个白名单文件；两个提交完整哈希/范围；两项红灯；101 基线和最终总数；全部变体、合法对照与 R2 回归；默认/partial/catalogs；README blob、依赖、范围、正式内容、缓存、清理；异常、风险、未决问题和远程操作。不得宣布 accepted。
```

## 门禁 1：任务信息

- 任务编号：`P1-01-R3`
- 任务名称：闭合 HTML br 属性边界
- 所属 Phase：Phase 1
- 当前状态：`ready`；只读预检后由主会话改为 `assigned`
- 执行方式：最小串行返工；产品只允许两文件
- 制定者：Phase 1 主会话

## 门禁 2：裁决、目标与学习者价值

R2 产品正确关闭围栏假表、深图递归和项目视图诊断串扰，并通过现有 101 项测试。产品提交后，主会话继续用系统临时目录抽查：`<br title="<x>">` 和 `<BR title="<x>" />` 均未匹配，公共 `complete` 仍为 0 错误。根因是属性体正则 `[^<>]*?` 把引号属性值内的尖括号当作不可接受字符，导致整个 br 标签识别失败。

- 唯一目标：以标签名边界识别 br，不解析属性体。
- 学习者价值：确保文件级章节清单不会因合法属性写法绕过单行约束，同时避免普通技术文本被误报。

## 门禁 3：范围与非范围

### 范围

1. 两项精确 TDD 测试；
2. HTML br 标签名识别的最小修复；
3. 完整 P1-01/R1/R2 回归；
4. 独立 R3 执行报告。

### 非范围

- 不重新设计通用 HTML/Markdown 解析；
- 不改围栏、DAG、项目闭合或其他 OL 行为；
- 不改 README、依赖、CLI、公开接口或正式内容；
- 不改旧提交/报告或执行远程写。

## 门禁 4：允许修改文件

```text
脚本资源/项目校验/validate_repository.py
脚本资源/项目校验/tests/test_validate_repository.py
项目管理/执行报告/P1-01-R3-执行报告.md
```

README 固定 blob：`6d71a07675ddb5ae598fe78007e00e2544d03009`。

## 门禁 5：前置、基线与必读文件

- R2 产品：`6ee194a19ed4bf9d3dfccfe80e50494a52b0524b`
- R2 报告：`7192bc324d04017c41ff3b38d7a6b034c5275562`
- 实现 blob：`1e988a979b7c62decae6ce3827c6b0848005aabb`
- 测试 blob：`3fea550e4ee46310c32076d4764fc1ccc4ca31f9`
- README blob：`6d71a07675ddb5ae598fe78007e00e2544d03009`
- 工具：Python 3.11.15、标准库、101 项测试。
- 必读文件：启动指令十三项，全部完整读取。
- 本任务不生产正式内容，不要求读取 `AI-CODEX-RULES.md`；越界即停止。

## 门禁 6：资料与证据

- 权威来源：本任务包、P1-01/R1/R2 合同、批准设计/计划、R2 报告。
- 无动态事实、无需联网。
- 最高证据：TDD 红绿灯、公开 `complete` API、完整回归、Git 固定对象。

## 门禁 7：交付物

| # | 交付物 | 路径 | 边界 |
|---:|---|---|---|
| 1 | 最小修复 | `脚本资源/项目校验/validate_repository.py` | 只调整 br 标签名识别 |
| 2 | 回归测试 | `脚本资源/项目校验/tests/test_validate_repository.py` | 两项独立测试；原 101 保留 |
| 3 | 执行报告 | `项目管理/执行报告/P1-01-R3-执行报告.md` | 红绿灯、提交、验证、风险 |

## 门禁 8：精确验收标准

1. `<br` 后为空白、`/` 或 `>` 时识别为 br，后续属性内容不影响识别；
2. 大小写、单双引号、自闭合、属性值内 `<`/`>` 变体均触发原规则；
3. 普通 `br`、`<bracket>`、`<br-description>`、`<br:custom>`、`<brx>` 不触发；
4. 不使用属性体解析器、`[^<>]` 式完整标签扫描或第三方依赖；
5. 标题/目标仍为 `OL005`，派生文本仍为 `OL002`；
6. 至少 103/103、原 101/101、skip 0；R2 四类主边界不回归；
7. README blob、默认 CLI、范围、仓库卫生和远程边界符合合同。

## 门禁 9：验证与预期

启动命令与 R2 相同，并新增 R3 任务包提交、R3=`assigned`、固定 blob 检查。红灯阶段仅测试文件改变；属性尖括号测试失败、合法对照通过、原 101 通过。绿灯阶段运行完整 unittest、默认确定性、帮助、partial、catalogs 21 OL001、公共 API 变体表、R2 围栏/深图/项目视图回归、标准库/AST、README blob、正式内容 0、缓存 0、精确提交范围和 `git diff --check`。

## 门禁 10：固定报告格式

报告路径：`项目管理/执行报告/P1-01-R3-执行报告.md`。必须包含角色/范围、主会话复现、两项红灯、根因/修复、产品提交、101/最终测试、变体矩阵、R2 回归、CLI、README blob、依赖/范围/卫生、风险/未决、远程确认和状态建议；不预测自身提交哈希。

## 门禁 11：提交、停止与回复

| 顺序 | 精确范围 | 固定提交信息 |
|---:|---|---|
| 1 | 实现与测试 | `fix: close HTML break attribute boundary` |
| 2 | R3 执行报告 | `docs: report P1-01-R3 HTML break closure` |

禁止 amend、rebase、reset 和任何远程写。停止条件和完成回复以启动指令为准；状态和最终验收只由 Phase 1 主会话裁决。
