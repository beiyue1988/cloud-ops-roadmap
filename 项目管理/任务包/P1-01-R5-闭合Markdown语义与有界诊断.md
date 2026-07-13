# P1-01-R5 闭合 Markdown 语义与有界诊断任务包

## 新会话启动指令

```text
请执行 cloud-ops-roadmap 的 P1-01-R5“闭合 Markdown 语义与有界诊断”返工任务。

你的身份是独立返工执行会话，不是项目领导者、规格制定者、发现问题的代码质量审查者、规格复审者或最终验收者。优先由原 P1-01/R1/R2/R3/R4 执行会话承担；主会话及两类审查会话不得实施产品修复。工作目录固定为 C:\Workspace\Projects\cloud-ops-roadmap，分支固定为 main。只执行本任务，不得扩大范围、委派或并发修改相同文件。

任何写操作前，按顺序完整阅读：
1. AGENTS.md；
2. CODEX-PRD.md，重点第 15、17、18 节；
3. 项目管理/任务包/P1-01-R5-闭合Markdown语义与有界诊断.md；
4. 项目管理/任务包/P1-01-R4-闭合混合缩进代码边界.md；
5. 项目管理/任务包/P1-01-R3-闭合HTML-br属性边界.md；
6. 项目管理/任务包/P1-01-R2-加固大纲解析与诊断边界.md；
7. 项目管理/任务包/P1-01-R1-闭合贯穿项目总视图.md；
8. 项目管理/任务包/P1-01-大纲合同与校验门.md；
9. 项目管理/执行计划/2026-07-13-Phase-1导航与完整大纲-设计说明.md；
10. 项目管理/执行计划/2026-07-13-Phase-1导航与完整大纲-实施计划.md；
11. 项目管理/执行报告/P1-01-R4-执行报告.md；
12. 脚本资源/项目校验/README.md；
13. 脚本资源/项目校验/validate_repository.py；
14. 脚本资源/项目校验/tests/test_validate_repository.py；
15. 模板/执行报告模板.md。

先使用 receiving-code-review 独立复现七项固化发现，再用 executing-plans 跟踪；修改实现或 README 前必须使用 test-driven-development，先只增加十三项规定测试并取得正确红灯；异常时使用 systematic-debugging；提交/完成前使用 verification-before-completion。不得用 brainstorming 改变批准合同。

唯一目标：在不改变四级门禁、OL001–OL012 责任、公开 API 和默认 CLI 的前提下，一次性关闭最终代码质量审查确认的七项同模块缺陷：缩进伪关闭围栏、非法 backtick info string、受控表结构错误派生闭合诊断、章节字段解析失败被当空集合、内联/转义 br 误拒绝、密集环物化失控，以及 OL007 伪造箭头路径。

唯一写入白名单：
- C:\Workspace\Projects\cloud-ops-roadmap\脚本资源\项目校验\README.md；
- C:\Workspace\Projects\cloud-ops-roadmap\脚本资源\项目校验\validate_repository.py；
- C:\Workspace\Projects\cloud-ops-roadmap\脚本资源\项目校验\tests\test_validate_repository.py；
- C:\Workspace\Projects\cloud-ops-roadmap\项目管理\执行报告\P1-01-R5-执行报告.md。

禁止修改旧报告、任务包、看板、设计、计划、PRD、治理文件、版本基线或正式内容；禁止改变门禁名称、OL 编号/责任、公开函数签名、默认校验行为、表头或字段；禁止引入完整 Markdown/HTML 解析器、第三方依赖、新模块、schema、CI、配置或仓库内临时文件；禁止删除、跳过或弱化现有 105 项测试；禁止 amend/reset/rebase、push、PR、发布或 GitHub 设置修改。

启动门禁：工作区干净、main、origin 精确为 https://github.com/beiyue1988/cloud-ops-roadmap.git、Python 3.11.15；R4 产品 01832f92a3b6615ada61b855f609af609d0565f1、R4 报告 aef57bd5a77dcbac7b85aa25332a62ba2929a95c 和本任务包提交均在历史；看板 P1-01/R1/R2/R3/R4 为 rework、R5 为 assigned、P1-01B 为 planned；实现、测试、README blob 依次为 d66ac1eb99b84896085888bfc7e72404f4b22641、532e9dad6789f8b1f188d22ff3b5a06a1844de4b、6d71a07675ddb5ae598fe78007e00e2544d03009；105/105、默认、partial 退出 0。任一不符立即停止。

写前必须用系统临时目录和当前公开/内部入口独立复现七项发现，不得复用主会话或审查会话输出代替证据：
1. 外层围栏中的 4 空格、Tab、空格+Tab 伪关闭标记使围栏内表被错误接受；
2. backtick 围栏 info string 含 backtick 时错误遮蔽后续真实表；
3. 项目总视图数据行缺首/尾外侧管道或多余列时，OL002 缺失或伴随派生 OL011；
4. 项目总视图或项目 README 的章节单元格去掉反引号时，OL002 伴随一个或两个派生 OL011；
5. 标题和 `_require_text` 字段中的内联代码 `<br>` 或奇数反斜杠转义 `\<br>` 被错误当作 HTML br；原始 `<br>` 仍应拒绝；
6. 100/200/300 节点完全强连通图的 cycle tuple 成员呈三次增长；
7. 实际边 00.01→00.03→00.02→00.01 被报告成不存在的排序箭头路径。
所有临时目录必须清理。

TDD 第一步只能修改测试文件，增加以下十三个独立测试方法：
1. test_catalogs_keeps_table_masked_after_indented_pseudo_closing_fence；
2. test_catalogs_accepts_table_after_valid_closing_fence_indent；
3. test_catalogs_does_not_open_backtick_fence_with_backtick_info；
4. test_complete_malformed_project_view_rows_emit_only_direct_errors；
5. test_complete_malformed_project_mapping_rows_emit_only_direct_errors；
6. test_complete_blank_line_terminates_controlled_table_before_prose；
7. test_complete_invalid_project_view_chapters_do_not_emit_ol011；
8. test_complete_invalid_project_mapping_chapters_do_not_emit_ol011；
9. test_complete_allows_html_break_literal_in_inline_code；
10. test_complete_allows_odd_escaped_html_break_literal；
11. test_complete_rejects_raw_and_even_escaped_html_break；
12. test_catalog_cycles_collapses_dense_strong_component；
13. test_catalogs_reports_cycle_component_without_fabricated_path。

红灯阶段至少 118 个测试方法；第 1、3、4、5、7、8、9、10、12、13 项必须因对应固化缺陷失败，第 2、6、11 项合法/原始 br 对照必须通过，原 105 项必须全部通过。失败只能来自规定断言，不得来自语法、导入、路径、夹具、性能阈值或环境。红灯阶段实现和 README blob 必须保持写前值。

随后按以下冻结语义实施最小修复：

A. fenced code：开启围栏只允许 0–3 个前导空格；backtick 围栏的 info string 含 backtick 时不是围栏，tilde 围栏不受此限制。关闭围栏必须与开启字符相同、长度不少于开启长度、前导只能是 0–3 个空格、围栏后只能有空白；4 空格、Tab 或任意达到第 4 列的混合缩进标记都是围栏内容，不得关闭。合法关闭后真实表继续解析；保留行数和 LF/CRLF/无末尾换行。

B. 受控表结构与比较资格：受控表从表头/分隔行开始，连续数据区域以空行终止；空行后的普通说明即使含竖线也不属于表。数据区域中缺首/尾外侧管道、列数不等或中途截断必须产生 OL002，并显式使该表失去结构比较资格。结构失败不得派生 OL010/OL011 闭合诊断；完整合法表干净删除一行仍必须以 OL011 报告真实缺项。

C. 字段解析资格：章节列表解析必须同时返回值和成功/失败状态。非法章节单元格不得被登记为合法空集合；项目总视图或项目 README 的章节字段失败只保留其直接 OL002，不得派生双向或逐里程碑 OL011。只有结构、里程碑和章节集合均成功解析的记录/完整侧才参与 D=V 与双向闭合；不得用全局跳过掩盖其他独立合法记录的直接错误。

D. HTML br 上下文：HTML br 检查只作用于实际 Markdown HTML 起始标签。任意长度的闭合 inline code span 中的 `<br>` 以及 `<` 前连续奇数个反斜杠的转义字面量允许；连续偶数个反斜杠后的 `<br>` 仍是未转义标签并按原 OL005/OL002 拒绝。原始大小写、属性、空白、自闭合和尖括号属性变体继续拒绝；普通 br、`<bracket>` 等继续允许。只实现项目所需代码跨度与转义屏蔽，不构建通用 Markdown/HTML 解析器。

E. 依赖环：用非递归强连通分量算法替代回边路径后缀物化；确定性邻接归一化之后，时间和附加内存为 O(V+E)。每个含多节点或自环的循环分量只产生一条 OL007，定位在分量最小章节 ID；诊断使用“循环分量”及确定性成员列表，不得用排序成员伪装箭头路径。无环、两个不相交环、自环、重复边、2,079/5,000 深链和 2,079 节点稠密 DAG 行为稳定；100 节点完全强连通图只返回一个含 100 个唯一成员的分量。

README 只同步上述受控 Markdown 子集、直接诊断隔离、literal br 和有界 SCC 合同，不扩大到完整 CommonMark、HTML 解析、教学质量或动态版本事实。

修复后运行十三项目标测试、完整 unittest 至少 118/118且原 105/105、默认两次一致、--help、非法 gate、缺失根、partial、catalogs 21 OL001、系统临时目录七项正反矩阵、行/换行保持、深链/稠密 DAG/密集 SCC、此前 R2/R3/R4 全部边界、标准库/AST/公开 API/范围/README/正式内容/缓存/diff 检查。禁止用宽松时间阈值作为正确性断言；以输出基数、确定性、无异常和结构证据验证复杂度。

验证通过后形成两个提交：产品提交只含 README、实现和测试，信息固定 `fix: bound outline Markdown semantics`；报告提交只含 项目管理/执行报告/P1-01-R5-执行报告.md，信息固定 `docs: report P1-01-R5 bounded semantics`。不得改写历史。

报告必须记录：七项写前复现；十三项红灯/对照；围栏、表结构/字段资格、br 上下文、SCC 根因与最小修复；产品提交完整哈希；至少 118/118与原 105/105；全部矩阵和旧边界；CLI；README/依赖/公开 API/范围/正式内容/缓存/清理；性能结构证据；风险、未决、远程确认和 submitted/rework/blocked 建议。不得宣布 accepted 或启动 P1-01B。

停止条件：身份/门禁/固定对象/blob 不符；任一固化反例不成立或规定红灯原因错误；需要白名单外写入、第三方依赖、完整 Markdown/HTML 解析器、新 OL、公开 API/CLI/表头变化或全局规格修改；无法同时保留合法围栏/表/br 对照和关闭七项缺陷；原 105 项或此前 R2/R3/R4 边界回归；SCC 仍物化每条回边路径或依赖递归；敏感信息、并发冲突或外部写需求。

完成回复包含：状态建议；四个白名单文件；两个完整提交哈希/范围；七项写前复现；十三项红灯/对照；105 基线和最终总数；围栏、表资格、字段资格、br、SCC 全部正反证据；CLI、README、依赖、公开 API、范围、正式内容、缓存、清理；异常、风险、未决和远程操作。不得宣布 accepted。
```

## 门禁 1：任务信息

- 任务编号：`P1-01-R5`
- 任务名称：闭合 Markdown 语义与有界诊断
- 所属 Phase：Phase 1
- 当前状态：`ready`；只读预检后由主会话改为 `assigned`
- 执行方式：单一校验器模块的综合串行返工；产品三文件
- 制定者：Phase 1 主会话

## 门禁 2：裁决、目标与学习者价值

R4 产品正确关闭混合缩进边界并通过规格复审，但最终代码质量审查以独立夹具确认 1 项 Critical、4 项 Important、2 项 Minor。主会话逐项复现后裁决全部七项成立；内联代码和奇数反斜杠转义中的 `<br>` 是字面 Markdown，不是 HTML 起始标签，允许它们不改变既有“拒绝 HTML 换行”决定。

- 唯一目标：闭合七项解析、诊断和复杂度边界。
- 学习者价值：让后续完整大纲既不能被伪 Markdown 绕过，也不会误拒合法技术文本或在大型依赖输入上失控。

## 门禁 3：范围与非范围

### 范围

1. 十三项精确 TDD 测试；
2. 围栏开启/关闭子集修复；
3. 受控表和章节字段的解析资格传播；
4. 实际 HTML br 上下文识别；
5. 非递归有界 SCC 与准确 OL007 诊断；
6. README 合同同步；
7. R5 执行报告。

### 非范围

- 不构建通用 CommonMark/HTML 解析器；
- 不改目录、表头、字段、OL 或四级门禁；
- 不生产正式大纲、正文、实验、项目或图表；
- 不改旧提交/报告或执行远程写。

## 门禁 4：允许修改文件

```text
脚本资源/项目校验/README.md
脚本资源/项目校验/validate_repository.py
脚本资源/项目校验/tests/test_validate_repository.py
项目管理/执行报告/P1-01-R5-执行报告.md
```

## 门禁 5：前置、基线与必读文件

- R4 产品：`01832f92a3b6615ada61b855f609af609d0565f1`
- R4 报告：`aef57bd5a77dcbac7b85aa25332a62ba2929a95c`
- 实现 blob：`d66ac1eb99b84896085888bfc7e72404f4b22641`
- 测试 blob：`532e9dad6789f8b1f188d22ff3b5a06a1844de4b`
- README blob：`6d71a07675ddb5ae598fe78007e00e2544d03009`
- 工具：Python 3.11.15、标准库、105 项测试。
- 必读文件：启动指令十五项，全部完整读取。
- 本任务不生产正式内容，不要求读取 `AI-CODEX-RULES.md`；越界即停止。

## 门禁 6：资料与证据

- 权威来源：本任务包、P1-01/R1/R2/R3/R4 合同、批准设计/计划、R4 报告、当前 README。
- 固定语义：任务包 A–E 五组合同；无需联网或动态版本。
- 最高证据：TDD 红绿灯、公开 API 综合夹具、结构化 SCC 输出、完整回归、Git 固定对象。

## 门禁 7：交付物

| # | 交付物 | 路径 | 边界 |
|---:|---|---|---|
| 1 | 合同同步 | `脚本资源/项目校验/README.md` | 只记录 R5 受控子集 |
| 2 | 最小修复 | `脚本资源/项目校验/validate_repository.py` | 五组内部边界 |
| 3 | 回归测试 | `脚本资源/项目校验/tests/test_validate_repository.py` | 十三项；原 105 保留 |
| 4 | 执行报告 | `项目管理/执行报告/P1-01-R5-执行报告.md` | 红绿灯、提交、验证、风险 |

## 门禁 8：精确验收标准

1. 三种缩进伪关闭不能泄漏围栏表；0–3 空格合法关闭继续工作；非法 backtick info 不遮蔽真实表；
2. 项目表/视图结构或章节字段错误只产生直接规则，不派生 OL010/OL011；合法干净缺项仍 OL011；
3. inline code 与奇数转义 br 允许，raw/偶数转义 br 继续按原规则拒绝；
4. 每个循环 SCC 一条确定性 OL007，无虚假箭头，强连通密集图输出有界；
5. 行号、行数、换行、OL001–OL012、CLI、公开 API 和标准库边界不回归；
6. 至少 118/118、原 105/105、skip 0；此前全部边界通过；
7. README、范围、正式内容、缓存、临时清理和远程边界符合合同。

## 门禁 9：验证与预期

启动检查新增 R5 任务包提交、R5=`assigned` 和三个固定 blob。红灯阶段只有测试文件改变；十项缺陷测试失败，三项对照及原 105 通过。绿灯运行完整 unittest、默认确定性、帮助/非法 gate/缺失根、partial、catalogs、七组公共/内部矩阵、换行、深链/稠密 DAG/密集 SCC、旧边界、AST/依赖/公开 API、README、范围、正式内容 0、缓存 0、临时清理、精确提交和格式检查。

## 门禁 10：固定报告格式

报告路径：`项目管理/执行报告/P1-01-R5-执行报告.md`。必须包含角色/范围、七项写前复现、十三项红灯/对照、五组根因/修复、产品提交、105/最终测试、矩阵、SCC 结构证据、旧回归、CLI、README、依赖/公开 API/范围/卫生、风险/未决、远程确认和状态建议；不预测自身提交哈希。

## 门禁 11：提交、停止与回复

| 顺序 | 精确范围 | 固定提交信息 |
|---:|---|---|
| 1 | README、实现、测试 | `fix: bound outline Markdown semantics` |
| 2 | R5 执行报告 | `docs: report P1-01-R5 bounded semantics` |

禁止 amend、rebase、reset 和任何远程写。停止条件和完成回复以启动指令为准；状态和最终验收只由 Phase 1 主会话裁决。
