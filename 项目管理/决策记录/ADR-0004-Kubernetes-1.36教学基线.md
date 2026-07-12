# ADR-0004：采用 Kubernetes 1.36 教学基线

## 决策元数据

- 编号：ADR-0004
- 标题：采用 Kubernetes 1.36 与配套运行时/CNI 教学基线
- 状态：`accepted`
- 日期：2026-07-12
- 制定者：主会话；P0-05 执行会话按已批准决定记录
- 影响范围：阶段 14、Kubernetes 项目、容器运行时、节点 cgroup 与 CNI

## 背景

Kubernetes 教材需要一条处于支持期、可集中维护 patch、且与运行时和 CNI 有官方兼容交集的 minor。旧讨论中的 1.31 已于 2025-11-11 EOL，不能继续作为新实验默认线。执行日必须区分锁定的 1.36 minor、动态当前 patch 与尚未发生的环境验证。

## 约束与决策问题

- 决策问题：在执行日仍受支持的 Kubernetes 1.36 与 1.35 之间，选择哪条教学 minor，并采用什么配套组合？
- 产品与学习约束：教程需要较长维护窗口、统一 kubeadm 流程和可复现实验；历史版本只用于迁移说明。
- 技术与环境约束：组合必须支持 CRI v1、cgroup v2、`systemd` driver，并与 containerd 和 Calico 官方范围形成交集。
- 时间与成本约束：Phase 0 不搭建集群；patch 统一维护，避免各章节重复写死。
- 权限与治理约束：主会话已批准 1.36；minor、运行时 LTS 线或 CNI minor 的变化需替代 ADR。

## 选项 1：Kubernetes 1.36

- 方案：锁定 Kubernetes 1.36 minor，使用执行日当前 patch 1.36.2；采用 kubeadm、containerd 2.3 LTS/CRI v1、cgroup v2/`systemd` driver 和 Calico 3.32 minor。
- 优点：执行日 actively supported；维护模式从 2027-04-28 开始，EOL 为 2027-06-28，维护窗口长于 1.35；containerd 官方表列出 Kubernetes 1.36 对应 2.3.0+，Calico 3.32 官方测试包含 1.36。
- 缺点：相对 1.35 更新，后续实验、依赖包和教学资料需要以 1.36 行为重新验证；当前 patch 的来源核验不能替代完整集群测试。
- 实施与迁移：在阶段 14 快照环境按 kubeadm 验证节点、运行时、CNI 与应用；patch 升级集中更新。回退只能在保留数据、API 与版本偏差评估后，由替代决策选择受支持 minor。
- 证据：Kubernetes 1.36 Release、containerd 兼容表、Kubernetes 运行时要求和 Calico 3.32 测试矩阵，均于 2026-07-12 核验。

## 选项 2：Kubernetes 1.35

- 方案：锁定 Kubernetes 1.35 minor，使用执行日当前 patch 1.35.6，并为其核定受支持的 containerd 与 Calico 组合。
- 优点：执行日同样 actively supported；发布时间更早，可获得更多既有实践资料；Calico 3.32 官方测试包含 1.35。
- 缺点：维护模式 2026-12-28、EOL 2027-02-28，窗口短于 1.36；项目会更早面对 minor 升级和教材迁移。
- 实施与迁移：若采用，需要重新定义主基线、验证运行时/CNI 并安排更早升级；从 1.36 回退到 1.35 不是普通 patch 回退，需评估 API、对象和 kubeadm 支持边界。
- 证据：[Kubernetes 1.35](https://kubernetes.io/releases/1.35/)与 Calico 3.32 系统要求，核验日期 2026-07-12。

## 决定

选择：选项 1。锁定 Kubernetes 1.36 minor 和 kubeadm；配套锁定 containerd 2.3 LTS、CRI v1、cgroup v2、`systemd` driver 与 Calico 3.32 minor。执行日当前 patch 分别为 Kubernetes 1.36.2、containerd 2.3.3、Calico 3.32.1，证据状态仅为 `source-verified`。

Kubernetes 1.31 已被排除为当前选项，仅登记为 `reference-only`，不得用于新实验。

## 理由

1.36 与 1.35 都是真实可行且受支持的教学线，但 1.36 提供更长维护窗口。containerd 官方兼容表明确给出 1.36 与 2.3.0+ / CRI v1 的组合，Calico 3.32 官方测试范围包含 1.36，形成可证明的来源兼容交集。1.31 已 EOL，不能作为受支持候选方案。

## 后果

### 正面后果

- 后续材料共享统一 minor、安装方式、运行时和 CNI 方向；
- 更长支持窗口降低短期内全量 minor 迁移概率；
- patch 由版本基线集中维护，正文减少漂移。

### 负面后果

- 1.36 组合仍需完整环境验证，来源矩阵不保证项目拓扑必然成功；
- 新 patch、安全问题或矩阵变化会产生持续验证与更新成本；
- minor 回退或升级涉及 API、数据和节点重建风险，不能当作普通包降级。

### 中性后果

- Kubernetes 1.31 保留历史记录但不再参与新实验；
- 章节引用 minor 与动态 patch 的职责被拆分到 ADR 和版本基线。

## 实施与迁移影响

- 实施步骤：阶段 14 前核验执行日 patch；准备快照；按 kubeadm 建群；验证 CRI、cgroup driver、节点、Calico 网络、升级和回退；保存命令与结果。
- 文件与系统影响：后续章节、实验和项目引用版本基线；本 ADR 不创建集群或配置文件。
- 兼容与迁移：从旧讨论 1.31 迁移到 1.36 时重做 API、镜像、kubeadm、运行时和 CNI 验证；遵守 Kubernetes 版本偏差与逐 minor 升级要求。
- 回退条件：1.36 不再受支持、官方组合交集消失、关键缺陷无法缓解或实验无法复现时，停止新实验，由新 ADR 选择仍受支持组合并从快照/备份恢复。
- 验证与验收：当前只有来源核验；环境门必须覆盖 kubeadm、containerd 2.3、CRI v1、cgroup v2/`systemd`、Calico 3.32 和应用连通性。

## 复审触发条件

- Kubernetes 1.36 进入维护模式或 EOL，或版本偏差/API 弃用规则改变；
- containerd 2.3 LTS 或 Calico 3.32 支持窗口、CRI 能力、测试矩阵发生变化；
- 安全 patch、关键 CVE、软件源不可用或阶段 14 实验无法复现；
- 最晚在阶段 14 首个集群实验进入 `ready` 前复核 patch，并在 2027-04-28 前复审 minor 迁移计划。

## 替代、废弃与关联决策

- 被本决策替代：旧讨论中的 Kubernetes 1.31 项目基线；保留为历史与迁移参考，不删除记录。
- 关联决策：[ADR-0001：主会话与执行会话分离](ADR-0001-主会话与执行会话分离.md)

## 参考证据

| 证据 | 类型 | 核验日期 | 支持范围 | 限制 |
|---|---|---|---|---|
| [Kubernetes 1.36](https://kubernetes.io/releases/1.36/) | 来源核验 | 2026-07-12 | 1.36.2、主动支持、维护与 EOL 日期 | 不证明集群已部署；1.36.3 当日仍是计划 patch |
| [Kubernetes 1.35](https://kubernetes.io/releases/1.35/) | 来源核验 | 2026-07-12 | 真实备选的支持与生命周期 | 不证明本项目采用或验证 1.35 |
| [Kubernetes 1.31](https://kubernetes.io/releases/1.31/) | 来源核验 | 2026-07-12 | 1.31 EOL 和无安全/缺陷更新 | 只用于历史排除 |
| [Patch Releases](https://kubernetes.io/releases/patch-releases/) | 来源核验 | 2026-07-12 | 当前与计划 patch | 计划日期可能变化，不等于发布 |
| [Container Runtimes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/) | 来源核验 | 2026-07-12 | CRI v1、cgroup v2 与 `systemd` driver | 不证明节点配置成功 |
| [Installing kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) | 来源核验 | 2026-07-12 | kubeadm 官方安装与建群入口 | 不证明本项目已安装 |
| [containerd Versioning and release](https://containerd.io/releases/) | 来源核验 | 2026-07-12 | 2.3 LTS、支持窗口、1.36/CRI v1 交集 | 不替代集成验证 |
| [containerd Releases](https://github.com/containerd/containerd/releases) | 来源核验 | 2026-07-12 | 当前 2.3.3 patch | 未下载或运行附件 |
| [Calico requirements](https://docs.tigera.io/calico/latest/getting-started/kubernetes/requirements) | 来源核验 | 2026-07-12 | 3.32 测试 Kubernetes 1.34–1.36 | 官方测试不等于本项目环境测试 |
| [Calico Releases](https://github.com/projectcalico/calico/releases) | 来源核验 | 2026-07-12 | 当前 3.32.1 patch | 未安装或运行 CNI |
