# 20 SRE 与架构能力

- **阶段编号：** 20
- **阶段名称：** SRE 与架构能力

## 阶段目标

建立面向可靠性、容量、灾备和系统治理的中级运维思维。

## 主要主题

- SLA/SLO/SLI
- Error Budget
- 容量
- HA
- RTO/RPO
- 灾备
- CMDB
- 复盘

## 前置阶段

- [15 DevOps 与 CI/CD](../15-DevOps与CI-CD/README.md)
- [17 监控与可观测性](../17-监控与可观测性/README.md)
- [19 AIOps 与 MLOps 入门](../19-AIOps与MLOps/README.md)

## 阶段产出

形成中级运维工程思维。

## 章节清单

| 章节 ID | 预定文件 | 标题 | 主要目标 | type | 直接前置 | 建议投入 | 就业标签 | 实践锚点 |
|---|---|---|---|---|---|---|---|---|
| `20.01` | `20.01-SRE-DevOps运维产品与开发的可靠性责任边界.md` | SRE、DevOps、运维、产品与开发的可靠性责任边界 | 区分 SRE、DevOps、运维、产品和开发在可靠性工作中的责任与交接边界 | `concept` | `17.38` | 30–60 分钟 | 就业后补学 | `CP-20` |
| `20.02` | `20.02-user-journey服务边界依赖owner与criticality.md` | user journey、服务边界、依赖、owner 与 criticality | 以用户旅程、服务边界、依赖、所有者和关键性定义可靠性对象 | `methodology` | `20.01` | 60–90 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.03` | `20.03-SLA-SLO-SLI承诺目标度量与误用.md` | SLA、SLO、SLI 的承诺、目标、度量与误用 | 区分 SLA、SLO、SLI 的后果与责任并识别用基础设施 uptime 替代用户体验的误用 | `concept` | `20.02` | 60–90 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.04` | `20.04-valid-good-event数据源观察点窗口与缺失数据.md` | valid/good event、数据源、观察点、窗口与缺失数据 | 用有效事件、良好事件、数据源、观察点和窗口定义可审查的 SLI 计算语义 | `methodology` | `20.03` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.05` | `20.05-availability-latency-quality-freshness-durability与throughput-SLI.md` | availability、latency、quality、freshness、durability 与 throughput SLI | 根据用户结果区分可用性、延迟、质量、新鲜度、持久性和吞吐量 SLI | `principle` | `20.04` | 60–90 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.06` | `20.06-SLO-target-window-workload-class-proxy与业务取舍.md` | SLO target、window、workload class、proxy 与业务取舍 | 结合工作负载类别、代理指标、用户和业务取舍建立 SLO 目标选择边界 | `methodology` | `20.05` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.07` | `20.07-error-budget计算剩余消耗burn-rate与不确定性.md` | error budget 计算、剩余、消耗、burn rate 与不确定性 | 关联错误预算总量、剩余、消耗和 burn rate 并说明数据不确定性的影响 | `methodology` | `20.06` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.08` | `20.08-多窗口多burn-rate观测告警接口与行动边界.md` | 多窗口/多 burn rate 观测、告警接口与行动边界 | 用多窗口和多 burn rate 观测定义告警接口与行动边界而不生产具体规则 | `methodology` | `20.07` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.09` | `20.09-error-budget-policy发布功能可靠性工作与例外治理.md` | error budget policy、发布、功能、可靠性工作与例外治理 | 使用错误预算政策治理发布、功能和可靠性工作的取舍及例外 | `methodology` | `20.08` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.10` | `20.10-toil特征测量增长与工程工作边界.md` | toil 特征、测量、增长与工程工作边界 | 识别 toil 的特征与增长趋势并区分重复劳动和有价值的工程工作 | `methodology` | `20.02` | 60–90 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.11` | `20.11-toil减少自动化优先级风险维护成本与停止条件.md` | toil 减少、自动化优先级、风险、维护成本与停止条件 | 根据收益、风险、维护成本和停止条件确定 toil 自动化优先级 | `methodology` | `20.10` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.12` | `20.12-on-call-readiness-runbook接口升级与轮值健康.md` | on-call readiness、runbook 接口、升级与轮值健康 | 界定值班就绪、runbook 接口、升级路径、轮值健康和能力边界 | `methodology` | `20.11` | 60–90 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.13` | `20.13-incident-severity指挥角色沟通记录与责任.md` | incident severity、指挥角色、沟通、记录与责任 | 根据事件严重度组织指挥角色、沟通、记录和明确责任 | `methodology` | `20.12` | 60–90 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.14` | `20.14-事件时间线triage-containment-mitigation-recovery与验证.md` | 事件时间线、triage、containment、mitigation、recovery 与验证 | 沿时间线组织事件分诊、控制、缓解、恢复和恢复结果验证 | `methodology` | `20.13` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.15` | `20.15-blameless-postmortem贡献因素action-item与有效性验证.md` | blameless postmortem、贡献因素、action item 与有效性验证 | 通过无责复盘识别贡献因素并闭合行动项所有者和有效性验证 | `methodology` | `20.14` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.16` | `20.16-incident-problem-change-release职责与阶段15边界.md` | incident、problem、change、release 职责与阶段 15 边界 | 区分 incident、problem、change 和 release 的职责并连接阶段 15 交付能力 | `methodology` | `15.36`, `20.15` | 60–90 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.17` | `20.17-变更风险审批canary维护窗口回退与预算证据.md` | 变更风险、审批、canary、维护窗口、回退与预算证据 | 关联变更风险、渐进交付、维护窗口、回退证据和错误预算政策形成可靠变更门 | `methodology` | `20.09`, `20.16` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.18` | `20.18-redundancy故障域负载均衡quorum与HA边界.md` | redundancy、故障域、负载均衡、quorum 与 HA 边界 | 关联冗余、故障域、负载均衡和 quorum 并区分 HA 与备份 | `principle` | `20.02` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.19` | `20.19-state-replication-consistency-split-brain与数据完整性.md` | state、replication、consistency、split brain 与数据完整性 | 解释状态、复制和一致性取舍如何影响 split brain 与数据完整性 | `principle` | `20.18` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.20` | `20.20-业务影响service-tier-RTO-RPO与数据分类.md` | 业务影响、service tier、RTO、RPO 与数据分类 | 根据业务影响、服务等级和数据分类定义 RTO 与 RPO 的决策语义 | `methodology` | `20.19` | 60–90 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.21` | `20.21-backup-restore-DR-strategy依赖顺序与责任边界.md` | backup、restore、DR strategy、依赖顺序与责任边界 | 区分备份、恢复和灾备策略并确定恢复依赖顺序与责任边界 | `methodology` | `20.20` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.22` | `20.22-failover-failback演练证据缺口与改进闭环.md` | failover、failback、演练、证据、缺口与改进闭环 | 用切换、回切和演练证据识别灾备缺口并形成改进闭环 | `methodology` | `20.21` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.23` | `20.23-demand-baseline-seasonality-growth-workload与容量模型.md` | demand、baseline、seasonality、growth、workload 与容量模型 | 根据需求基线、季节性、增长和工作负载建立容量模型 | `methodology` | `20.02` | 60–90 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.24` | `20.24-utilization-saturation-queue-headroom-bottleneck与限制.md` | utilization、saturation、queue、headroom、bottleneck 与限制 | 关联利用率、饱和度、队列、余量和瓶颈判断容量限制 | `principle` | `20.23` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.25` | `20.25-forecast-threshold-scale-procurement-cost与容量决策.md` | forecast、threshold、scale、procurement、cost 与容量决策 | 综合预测、阈值、扩缩容、采购和成本形成容量决策 | `methodology` | `20.24` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.26` | `20.26-load-stress-soak-chaos与failure-injection安全边界.md` | load、stress、soak、chaos 与 failure injection 安全边界 | 区分负载、压力、浸泡和故障注入的目标、风险与安全停止边界 | `methodology` | `20.25` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.27` | `20.27-service-catalog资源清单configuration-item与owner.md` | service catalog、资源清单、configuration item 与 owner | 区分服务目录、资源清单和配置项并建立所有权合同 | `concept` | `20.02` | 60–90 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.28` | `20.28-relationship-dependency-source-of-truth-reconciliation与新鲜度.md` | relationship、dependency、source of truth、reconciliation 与新鲜度 | 用关系、依赖、权威来源、对账和新鲜度治理 CMDB 数据质量 | `methodology` | `20.27` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L3` |
| `20.29` | `20.29-criticality-single-point-blast-radius风险登记与优先级.md` | criticality、single point、blast radius、风险登记与优先级 | 根据关键性、单点和爆炸半径登记风险并确定治理优先级 | `methodology` | `20.28` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.30` | `20.30-security-reliability-cost-performance-operability-complexity取舍.md` | security、reliability、cost、performance、operability、complexity 取舍 | 在约束下权衡安全、可靠性、成本、性能、可运维性和复杂度 | `methodology` | `20.29` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.31` | `20.31-quality-attribute-NFR场景约束验收与证据.md` | quality attribute/NFR 场景、约束、验收与证据 | 用场景、约束、响应和证据表达可验收的质量属性与 NFR | `methodology` | `20.30` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.32` | `20.32-ADR选项证据可逆性决策时点与复审触发.md` | ADR、选项、证据、可逆性、决策时点与复审触发 | 通过选项、证据、可逆性和复审触发条件建立 ADR 决策记录边界 | `methodology` | `20.31` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.33` | `20.33-architecture-review-failure-mode技术债生命周期与演进.md` | architecture review、failure mode、技术债、生命周期与演进 | 通过架构评审、失败模式和技术债管理推动系统生命周期演进 | `methodology` | `20.32` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.34` | `20.34-operating-model-ownership-runbook-standard接口与成熟度路线.md` | operating model、ownership、runbook/standard 接口与成熟度路线 | 关联运营模式、所有权、runbook/standard 接口和成熟度形成持续改进路线 | `methodology` | `20.33` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |
| `20.35` | `20.35-用户目标度量预算运营韧性容量治理与完整架构闭环.md` | 用户目标、度量、预算、运营、韧性、容量、治理与完整架构闭环 | 汇合全部章节形成从用户目标到度量、预算、运营、韧性、容量和架构治理的完整闭环 | `methodology` | `20.17`, `20.22`, `20.26`, `20.34` | 90–120 分钟 | 就业后补学 | `CP-20`, `LAB-L4` |

## 导航

- 上游：[知识库总览](../README.md)
- 前一阶段：[19 AIOps 与 MLOps 入门](../19-AIOps与MLOps/README.md)
- 相关内容：[运维思维训练](../../运维思维训练/README.md)
- 相关内容：[企业规范](../../企业规范/README.md)

## 边界

当前仅建立阶段骨架，不含正式正文、教学解释、操作步骤、面试答案或故障案例。

- 可靠性从用户旅程、服务边界、依赖、所有者、关键性和不可接受结果开始。SLA 是带后果的业务或合同承诺，SLO 是目标，SLI 是度量；基础设施 uptime 和阶段 17 的现成指标都不能自动替代面向用户结果的 SLI。
- 阶段 17 负责指标、告警和 SLI 测量接口，阶段 20 负责 SLO、error budget 及其治理语义；本阶段不填写具体 SLO 数值、阈值或告警规则，也不把 100% 作为默认目标。阶段 15 继续拥有 CI/CD 实现，本阶段只治理变更风险、发布证据、维护窗口、回退和错误预算政策的关系。
- incident、problem、change、release、service catalog、configuration item 和 CMDB 只按职责与数据合同解释，保持产品和版本中立，不绑定 ITIL 版本、认证产品或厂商流程。无责复盘不等于无责任，本阶段不制定真实值班表、组织名单、制度或事件内容。
- HA、备份和灾备分别处理冗余与故障域、数据保护、业务连续性和恢复责任。快照、复制或高可用都不能单独冒充完整灾备；本阶段不选择拓扑、地域、云产品或灾备方案，不执行压测、故障注入、切换、回切或恢复操作。
- 容量结论不能只依赖平均利用率，必须同时考虑需求、季节性、增长、饱和度、队列、余量、瓶颈、成本和安全验证边界。CMDB 不是自动正确的真相源，关系、来源、对账、新鲜度、漂移和所有权必须进入治理。
- 架构章节只建立质量属性、约束、权衡、ADR、评审、技术债、演进和运营成熟度的方法边界，不修改本项目 ADR，不把单一参考架构当作所有组织的答案。阶段 19 的 AIOps/MLOps 不是通用 SRE 与架构能力的硬前置。
