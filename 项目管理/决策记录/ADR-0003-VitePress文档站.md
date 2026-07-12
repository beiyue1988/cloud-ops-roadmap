# ADR-0003：采用 VitePress 作为默认文档站

## 决策元数据

- 编号：ADR-0003
- 标题：采用 VitePress 作为默认文档站
- 状态：`accepted`
- 日期：2026-07-12
- 制定者：主会话；P0-05 执行会话按已批准决定记录
- 影响范围：Markdown 发布形态、文档站任务、导航、搜索与构建工具链

## 背景

项目以 Markdown 为唯一正文源，未来需要生成带导航、代码展示、搜索和响应式主题的静态网站。工具选择必须适配现有 Front Matter 和技术文档内容，同时控制构建、扩展和迁移成本。具体依赖版本尚未进入文档站实施门，不能因选择工具而提前猜测 VitePress、Node.js 或包管理器版本。

## 约束与决策问题

- 决策问题：在保持 Markdown 单一正文源的前提下，默认使用哪一种真实可行的文档站生成器？
- 产品与学习约束：中文技术知识库需要清晰导航、代码内容、Front Matter 与本地搜索；发布物不得产生无法回写的独立正文。
- 技术与环境约束：仓库已有 Markdown 与 YAML Front Matter；具体构建依赖必须在网站任务进入 `ready` 前核定和验证。
- 时间与成本约束：Phase 0 只固化方向，不建设网站；后续应避免不必要的内容迁移。
- 权限与治理约束：主会话已批准 VitePress；执行会话只记录决定，不选择依赖版本或发布网站。

## 选项 1：VitePress

- 方案：使用 VitePress 将现有 Markdown 构建为静态网站，优先使用默认主题能力，按需扩展 Vite/Vue；Markdown 保持权威正文。
- 优点：官方定位面向内容型静态网站；内建适合技术文档的 Markdown 扩展、Front Matter 与代码块能力；默认主题支持本地模糊全文搜索；与既定 Markdown 源直接匹配。
- 缺点：引入 Node.js、包管理器、Vite/Vue 工具链和相应依赖维护；自定义 Vue 能力若滥用，会增加构建复杂度并让内容耦合表现层。
- 实施与迁移：网站任务核定依赖版本后建立最小配置、导航与搜索，运行完整构建和链接验证；回退时保留 Markdown，移除站点配置即可恢复为仓库阅读形态。
- 证据：[VitePress 定位](https://vitepress.dev/guide/what-is-vitepress)、[Front Matter](https://vitepress.dev/guide/frontmatter)、[本地搜索](https://vitepress.dev/reference/default-theme-search)，核验日期 2026-07-12。

## 选项 2：MkDocs

- 方案：使用 MkDocs 和 YAML 配置构建项目文档站，按实际需求选择主题与搜索/扩展能力。
- 优点：官方定位同样是面向项目文档的 Markdown 静态站生成器；配置模型直接，Python 工具链对部分运维学习者熟悉，是可实施的真实替代方案。
- 缺点：需要维护 Python 侧站点依赖、主题和插件组合；与项目已批准的 VitePress/Vue 发布方向不同，迁移需重做配置、主题适配和构建验证。
- 实施与迁移：建立 MkDocs 配置并逐项验证 Front Matter、导航、代码、搜索与链接；从 VitePress 迁移时保持 Markdown 正文，替换站点配置和扩展语法，必要时提供兼容转换。
- 证据：[MkDocs 官方站](https://www.mkdocs.org/)说明其为面向项目文档、使用 Markdown 与 YAML 配置的静态站生成器，核验日期 2026-07-12。

## 决定

选择：选项 1，采用 VitePress 作为默认文档站；Markdown 继续作为唯一正文源。VitePress、Node.js 与包管理器的具体版本维持 `phase-gated`，必须在文档站任务进入 `ready` 前核定。

## 理由

VitePress 的技术文档定位、Front Matter、代码内容和默认主题本地搜索直接适配本项目既有 Markdown 模型，并与 PRD 已批准方向一致。MkDocs 是真实可行替代方案，但会切换到另一套构建、主题和插件治理；当前没有足以抵消迁移成本的项目收益。本决定不依赖“MkDocs 停止维护”等未经核验说法。

## 后果

### 正面后果

- Markdown 可保持单一正文源，网站能力围绕现有内容建立；
- Front Matter、技术代码块和本地搜索有官方能力入口，后续可通过构建验证验收。

### 负面后果

- 项目需要维护 Node.js、包管理器和 VitePress 依赖线；
- 深度主题定制会增加 Vue/Vite 知识与升级成本，必须限制在发布层。

### 中性后果

- 网站任务需增加依赖核定门、构建产物边界和回归验证；
- 现阶段只确定工具方向，不创建配置、不锁定版本、不发布网站。

## 实施与迁移影响

- 实施步骤：文档站任务进入 `ready` 前核定依赖；建立最小站点；验证 Front Matter、导航、代码、搜索、内部链接和构建；再决定主题扩展。
- 文件与系统影响：未来由单独任务授权站点配置和发布工作；本 ADR 不授权任何站点文件。
- 兼容与迁移：现有 Markdown 保持权威；避免把正文写进 Vue 组件。若迁移到 MkDocs，优先转换配置与扩展语法，不复制正文。
- 回退条件：VitePress 无法构建现有内容、依赖进入不可接受生命周期、搜索或可访问性无法满足验收，且限定范围内无法修复时，回退为纯 Markdown 或新 ADR 选择替代工具。
- 验证与验收：Phase 0 仅取得来源核验；网站任务必须取得安装、完整构建、链接、搜索和发布前静态检查证据。

## 复审触发条件

- VitePress、Node.js 或关键依赖生命周期、安全和兼容要求发生实质变化；
- 完整仓库构建、搜索、导航、国际化或可访问性无法达到网站任务验收标准；
- 最晚在文档站任务进入 `ready` 前复审依赖版本与实施边界。

## 替代、废弃与关联决策

- 关联决策：[ADR-0001：主会话与执行会话分离](ADR-0001-主会话与执行会话分离.md)

## 参考证据

| 证据 | 类型 | 核验日期 | 支持范围 | 限制 |
|---|---|---|---|---|
| [What is VitePress?](https://vitepress.dev/guide/what-is-vitepress) | 来源核验 | 2026-07-12 | Markdown 静态站、技术文档与代码内容定位 | 不证明本仓库已构建，也不锁定版本 |
| [VitePress Frontmatter](https://vitepress.dev/guide/frontmatter) | 来源核验 | 2026-07-12 | YAML Front Matter 和自定义数据 | 不证明现有字段与主题已完成集成 |
| [VitePress Search](https://vitepress.dev/reference/default-theme-search) | 来源核验 | 2026-07-12 | 本地模糊全文搜索 | 不证明全量内容性能 |
| [MkDocs](https://www.mkdocs.org/) | 来源核验 | 2026-07-12 | Markdown 项目文档静态站替代方案 | 不证明主题或插件组合适配本项目 |
