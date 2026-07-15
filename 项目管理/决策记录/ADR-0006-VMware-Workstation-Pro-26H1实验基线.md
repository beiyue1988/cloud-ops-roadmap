# ADR-0006：采用 VMware Workstation Pro 26H1 作为阶段 03 本地实验基线

## 决策元数据

- 编号：ADR-0006
- 标题：采用 VMware Workstation Pro 26H1 作为阶段 03 本地实验基线
- 状态：`accepted`
- 日期：2026-07-15
- 制定者：主会话；P1-02-03G 执行会话按已批准决定记录
- 影响范围：阶段 03 本地实验环境、宿主系统边界、Rocky Linux 客体工具与后续环境验证门

## 背景

阶段 03 需要把 PRD 中的 VMware 方向收敛为可追溯的产品线和宿主边界，否则后续章节清单、安装实验和故障验证会随浮动下载对象漂移。执行日官方已发布 VMware Workstation Pro 26H1，Windows 版本转为 64 位应用，并提供 26H1 的宿主系统矩阵；现有版本基线仍把 VMware 保持为 `phase-gated`。本决定只关闭产品与日历发布线门，不把来源核验伪装为本项目已经安装或兼容。

## 约束与决策问题

- 决策问题：阶段 03 应采用当前 Workstation Pro 26H1，还是采用仍受支持的上一发布线 25H2 作为本地虚拟化主线？
- 产品与学习约束：零基础学习者需要统一的快照、克隆和虚拟机环境入口；Windows x86-64 是主教学宿主，Linux 宿主只作为逐次核验的兼容路径，macOS/Fusion 不在本决定范围。
- 技术与环境约束：主客体必须保持架构和支持边界可追溯；Rocky Linux 9.8 x86_64 沿用既有锁定线；不得把官方支持矩阵外推为当前宿主、Hyper-V、VBS 或内存完整性组合已经运行成功。
- 时间与成本约束：锁定产品和 26H1 日历发布线，但不锁死下载 build；具体 build 必须在首个安装实验前重新核验，以免把动态下载对象固化为长期正文。
- 权限与治理约束：主会话已批准 26H1；本任务不得安装或下载 VMware/Rocky Linux，不得关闭安全控制，日历发布线变化必须由替代 ADR 决定。

## 选项 1：VMware Workstation Pro 26H1

- 方案：锁定 Workstation Pro 26H1；以 Windows 10 20H1+ 或 Windows 11 的 64 位 x86 宿主为主教学路径，Linux 宿主按执行时官方发行版和内核矩阵逐次核验；下载 build 保持动态。
- 优点：26H1 是执行日官方 GA 的当前日历发布线；Windows 应用已转为 64 位；宿主支持表、下载入口和已知问题入口均有官方路由；与上一线同为虚拟硬件版本 22，不要求仅为跟随发布线而升级已有虚拟机兼容级别。
- 缺点：当前来源只能证明发布、许可和厂商支持边界，不能证明学习者宿主、Hyper-V/VBS/内存完整性组合或 Rocky Linux 9.8 客体已经运行；免费用户主要依赖自助资料与社区资源；动态 build 会在安装门再次产生核验工作。
- 实施与迁移：先更新 ADR 与版本基线；首个安装实验前核验当时 build、Release Notes、处理器和宿主要求，并在不关闭安全控制的前提下验证宿主组合。若已有虚拟机能满足教学目标，不强制升级其虚拟硬件版本；失败时从实验前快照回退并停止扩展。
- 证据：[26H1 公告](https://blogs.vmware.com/cloud-foundation/2026/05/14/announcing-vmware-workstation-and-fusion-26h1/)、[宿主支持矩阵](https://knowledge.broadcom.com/external/article?legacyId=80807)、[虚拟硬件版本](https://knowledge.broadcom.com/external/article?legacyId=1003746)与[安装入口](https://knowledge.broadcom.com/external/article/387947/installing-vmware-workstation-pro.html)，核验日期 2026-07-15。

## 选项 2：VMware Workstation Pro 25H2

- 方案：采用上一日历发布线 Workstation Pro 25H2，并在阶段 03 使用同一 Windows 主宿主和逐次核验的 Linux 兼容路径。
- 优点：官方宿主矩阵仍列出 25H2；与 26H1 同为虚拟硬件版本 22，已有 25H2 虚拟机不因硬件版本产生额外迁移；作为较早发布线可能已有更多现成问题记录。
- 缺点：它不是执行日当前发布线；选择上一线会更早产生升级与再验证工作，且不能获得 26H1 的当前架构和修复入口；较早发布不等于已在本项目环境验证。
- 实施与迁移：若采用，需要重新核验 25H2 的下载可用性、Release Notes、宿主组合与 build，并在新日历发布线到来时安排迁移；从 26H1 回退到 25H2 不是普通 build 回退，必须由替代 ADR 说明原因和验证范围。
- 证据：[宿主支持矩阵](https://knowledge.broadcom.com/external/article?legacyId=80807)同时列出 25H2/26H1，[虚拟硬件版本表](https://knowledge.broadcom.com/external/article?legacyId=1003746)将两者映射到版本 22；核验日期 2026-07-15。

## 决定

选择：选项 1。阶段 03 锁定 VMware Workstation Pro 26H1 产品和日历发布线；Windows 10 20H1+ 或 Windows 11 的 64 位 x86 宿主是主教学路径，Linux 宿主只作为按执行时官方发行版/内核矩阵核验的兼容路径，macOS/Fusion 不在本决定范围。具体下载 build 不锁定，必须在首个安装实验前重新核验。

Rocky Linux 9.8 x86_64 继续作为主客体。Rocky Linux 8 及以上客体采用发行版提供的 `open-vm-tools` 路径；这不证明 Rocky Linux 9.8 已在本项目安装成功。Workstation/Fusion 对个人、教育和商业用途免费，但下载和使用仍须遵守执行时适用条款；没有有效支持合同的免费用户主要依赖文档、知识库和社区资源。

26H1 与 25H2 均对应虚拟硬件版本 22，不因可升级就强制升级已有虚拟机兼容级别。Hyper-V、VBS、内存完整性与 Workstation 的实际组合仅登记为首个实验前验证点，本决定不授权关闭任何安全控制。

## 理由

26H1 是执行日官方宣布 GA 并提供下载入口的当前日历发布线，Windows 架构和主宿主边界明确；25H2 仍是真实可行的兼容备选，但选择上一线会缩短教材保持当前状态的时间。两条线共享虚拟硬件版本 22，采用 26H1 不要求为了版本名称而升级已有 VM 的硬件兼容级别。将 build 和真实宿主组合留在安装实验门，可以同时获得统一教学线与诚实的证据边界。

## 后果

### 正面后果

- 阶段 03 后续清单和实验共享同一产品、日历发布线与主宿主边界；
- Windows 64 位要求、Linux 兼容路径、Rocky 客体工具和动态 build 门均可追溯；
- 来源核验与环境验证保持分离，学习者不会把厂商支持表误读为自己的电脑必然可用。

### 负面后果

- 首个安装实验仍需核验 build、处理器、宿主版本、Hyper-V/VBS/内存完整性组合和 Rocky Linux 9.8 运行结果；
- 免费用户缺少新的 Broadcom 全局支持工单权益，故障处理更依赖自助资料与社区；
- 日历发布线、下载门户或宿主矩阵变化会触发持续维护和可能的替代 ADR。

### 中性后果

- VMware 在版本基线中由 `phase-gated`/`not-yet-verified` 移入 `locked`/`source-verified`；
- 下载 build 保持动态，不在章节标题或长期基线中写死；
- Linux 宿主和 macOS/Fusion 不成为 Windows 主路径的隐含前置或替代主线。

## 实施与迁移影响

- 实施步骤：本任务记录 ADR、索引、版本基线与更新日志；阶段 03 首个安装实验前重新核验当前 build 和官方要求，再在明确宿主上取得环境证据。
- 文件与系统影响：后续阶段 03 清单和实验引用本 ADR 与版本基线；本决定不授权下载、安装、配置或安全控制变更。
- 兼容与迁移：25H2 与 26H1 同为虚拟硬件版本 22；已有 VM 仅在确有功能或安全需求且完成兼容评估时升级硬件版本。其他旧版本迁移必须先保留快照和可回退副本。
- 回退条件：26H1 下载不可用、官方支持交集消失、关键安全问题无法缓解，或目标宿主/客体实验无法复现时，停止阶段 03 安装扩展并从实验前快照恢复；改变发布线必须由替代 ADR 批准，不静默改用 25H2 或其他虚拟化产品。
- 验证与验收：当前最高证据为 `source-verified`；`environment-verified` 必须记录实际 build、宿主系统与安全功能状态、处理器、Rocky Linux 9.8 客体、`open-vm-tools`、快照/克隆和回退结果。

## 复审触发条件

- 26H1 被新日历发布线取代、下载不可用、许可/支持模式、宿主矩阵或处理器要求发生实质变化；
- 首个安装实验发现目标 Windows 宿主、Hyper-V/VBS/内存完整性组合或 Rocky Linux 9.8 客体无法在不降低安全基线的前提下复现；
- 虚拟硬件版本升级成为功能或安全必需，或 Linux 宿主需要提升为主教学路径；
- 最晚在阶段 03 首个安装实验进入执行前重新核验 build、Release Notes、宿主要求、适用条款和回退条件。

## 替代、废弃与关联决策

- 关联决策：[ADR-0001：主会话与执行会话分离](ADR-0001-主会话与执行会话分离.md)

## 参考证据

| 证据 | 类型 | 核验日期 | 支持范围 | 限制 |
|---|---|---|---|---|
| [Workstation/Fusion 26H1 公告](https://blogs.vmware.com/cloud-foundation/2026/05/14/announcing-vmware-workstation-and-fusion-26h1/) | 来源核验 | 2026-07-15 | 26H1 GA、Windows 64 位架构、Broadcom Support Portal 可用性与免费用途 | 不锁定 build，不证明本项目已下载、安装或运行 |
| [Workstation Pro 26H1 Release Notes](https://techdocs.broadcom.com/us/en/vmware-cis/desktop-hypervisors/workstation-pro/26H1.html) | 来源核验受限 | 2026-07-15 | 官方公告路由到该当前发布说明入口 | 自动访问返回 403；未用搜索摘要补足已知问题，也不据此声明环境兼容 |
| [支持的宿主操作系统（Article 315653）](https://knowledge.broadcom.com/external/article?legacyId=80807) | 来源核验 | 2026-07-15 | 26H1/25H2 的 64 位宿主边界、Windows 10 20H1+、Windows 11 与 Linux 发行版/内核表 | 厂商矩阵不证明任一实际宿主组合已经运行 |
| [Installing VMware Workstation Pro（Article 387947）](https://knowledge.broadcom.com/external/article/387947/installing-vmware-workstation-pro.html) | 来源核验 | 2026-07-15 | 下载经 Broadcom Support Portal，安装前核对 Release Notes、处理器与宿主要求 | 本任务未登录、下载或安装，不能证明门户账户、build 或安装成功 |
| [虚拟硬件版本（Article 315655）](https://knowledge.broadcom.com/external/article?legacyId=1003746) | 来源核验 | 2026-07-15 | 26H1/25H2 对应虚拟硬件版本 22，升级需按功能与安全需求评估 | 不证明已有 VM 应升级或升级后兼容 |
| [VMware Tools 与客体兼容性（Article 313371）](https://knowledge.broadcom.com/external/article/313371/vmware-tools-compatibility-with-guest-op.html) | 来源核验 | 2026-07-15 | Linux 推荐 `open-vm-tools`，Rocky Linux 8+ 由发行版提供 | 不证明 Rocky Linux 9.8 客体或工具已安装成功 |
| [Workstation/Fusion 对所有用户免费](https://blogs.vmware.com/cloud-foundation/2024/11/11/vmware-fusion-and-workstation-are-now-free-for-all-users/) | 来源核验 | 2026-07-15 | 个人、教育、商业用途免费及在线自助资源边界 | 免费不等于附带新的企业支持合同，也不取代适用条款核验 |
| [下载与许可（Article 368667）](https://knowledge.broadcom.com/external/article/368667/download-and-license-vmware-desktop-hype.html) | 来源核验 | 2026-07-15 | 免费版本无需许可证密钥、门户账户与下载条款确认 | 不证明具体账户通过合规审核，也不锁定 26H1 build |
| [Desktop Hypervisor FAQ](https://www.vmware.com/docs/desktop-hypervisor-faqs) | 来源核验 | 2026-07-15 | 无付费许可证密钥、免费用户自助支持模式和 Workstation x86-64 宿主范围 | FAQ 不替代具体 Release Notes、宿主矩阵或环境实验 |
| [Rocky Linux 9.8 GA](https://rockylinux.org/news/rocky-linux-9-8-ga-release) | 来源核验 | 2026-07-15 | Rocky Linux 9.8 已 GA 并提供 x86_64 等镜像入口 | 不证明镜像已下载或 VMware 安装成功 |
| [Rocky Linux 版本指南](https://wiki.rockylinux.org/rocky/version/) | 来源核验 | 2026-07-15 | 9.8 是当前受支持的 Rocky Linux 9 minor | 不证明 Workstation 客体兼容性或项目环境运行结果 |
