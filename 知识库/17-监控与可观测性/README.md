# 17 监控与可观测性

- **阶段编号：** 17
- **阶段名称：** 监控与可观测性

## 阶段目标

建立联动指标、日志和追踪来观测系统状态的能力。

## 主要主题

- Prometheus
- Alertmanager
- Grafana
- OpenTelemetry
- Jaeger/SkyWalking
- SLO

## 前置阶段

- [07 性能与安全](../07-性能与安全/README.md)
- [14 Kubernetes](../14-Kubernetes/README.md)
- [16 企业日志平台](../16-企业日志平台/README.md)

## 阶段产出

建立指标、日志、追踪联动。

## 章节清单

| 章节 ID | 预定文件 | 标题 | 主要目标 | type | 直接前置 | 建议投入 | 就业标签 | 实践锚点 |
|---|---|---|---|---|---|---|---|---|
| `17.01` | `17.01-monitoring-observability职责目标与边界.md` | monitoring、observability、职责、目标与边界 | 区分 monitoring 与 observability 并界定系统观测的责任、目标和证据边界 | `concept` | `16.37` | 30–60 分钟 | 就业后补学 | `CP-17` |
| `17.02` | `17.02-metric-log-trace-event与telemetry信号模型.md` | metric、log、trace、event 与 telemetry 信号模型 | 区分 metric、log、trace 和 event 并建立平台中立的 telemetry 信号模型 | `principle` | `17.01` | 60–90 分钟 | 就业后补学 | `CP-17` |
| `17.03` | `17.03-问题假设查询关联判断与证据链.md` | 问题、假设、查询、关联、判断与证据链 | 从问题和假设组织查询、关联、判断与可反驳的观测证据链 | `methodology` | `17.02` | 60–90 分钟 | 就业后补学 | `CP-17` |
| `17.04` | `17.04-counter-gauge-histogram-summary与基数.md` | counter、gauge、histogram、summary 与基数 | 区分指标类型并判断 label 和 cardinality 对计算与成本的影响 | `principle` | `17.02` | 60–90 分钟 | 就业后补学 | `CP-17` |
| `17.05` | `17.05-target-service-node-container-Kubernetes与应用数据源.md` | target、service、node、container、Kubernetes 与应用数据源 | 按观测问题识别 target、service、node、container、Kubernetes 和应用数据源 | `methodology` | `17.03` | 60–90 分钟 | 就业后补学 | `CP-17` |
| `17.06` | `17.06-Prometheus架构pull-scrape与本地存储.md` | Prometheus 架构、pull、scrape 与本地存储 | 关联 Prometheus 组件、pull、scrape、time series 和本地存储的职责 | `platform` | `17.04`, `17.05` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.07` | `17.07-service-discovery-target-relabel与采集边界.md` | service discovery、target、relabel 与采集边界 | 解释服务发现、target 和 relabel 如何共同限定采集对象与标签 | `principle` | `17.06` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.08` | `17.08-exporter-instrumentation与应用指标责任.md` | exporter、instrumentation 与应用指标责任 | 区分 exporter、自动与手工 instrumentation 以及应用指标责任 | `methodology` | `17.07` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.09` | `17.09-PromQL数据模型selector与向量类型.md` | PromQL 数据模型、selector 与向量类型 | 解释 PromQL selector、instant vector 和 range vector 的数据语义 | `principle` | `17.06` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.10` | `17.10-rate聚合operator与vector-matching.md` | rate、聚合、operator 与 vector matching | 使用 rate、aggregation、operator 和 vector matching 建立正确查询语义 | `principle` | `17.09` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.11` | `17.11-recording-rule命名成本与复用.md` | recording rule、命名、成本与复用 | 根据命名、计算成本和复用需求界定 recording rule 的责任 | `methodology` | `17.10` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.12` | `17.12-TSDB-retention-compaction-storage与恢复边界.md` | TSDB retention、compaction、storage 与恢复边界 | 解释 TSDB 保留、压缩和存储如何约束容量及恢复责任 | `principle` | `17.06` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.13` | `17.13-HA-federation-remote-write与长期存储边界.md` | HA、federation、remote write 与长期存储边界 | 比较 HA、federation 和 remote write 并保留长期存储及一致性选择门 | `methodology` | `17.08`, `17.12` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L4` |
| `17.14` | `17.14-Grafana-data-source-query-panel与dashboard.md` | Grafana data source、query、panel 与 dashboard | 关联 data source、query、panel、dashboard 和权限形成可视化入口 | `tool` | `17.10` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.15` | `17.15-dashboard受众层级上下文变量与反模式.md` | dashboard 受众、层级、上下文、变量与反模式 | 根据受众和决策场景组织 dashboard 层级、上下文、变量与反模式 | `methodology` | `17.14` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.16` | `17.16-告警哲学symptom-cause可操作性与噪声.md` | 告警哲学、symptom、cause、可操作性与噪声 | 区分 symptom 与 cause 并以可操作性和噪声预算界定告警价值 | `methodology` | `17.03` | 60–90 分钟 | 就业后补学 | `CP-17` |
| `17.17` | `17.17-Prometheus-alerting-rule状态for与证据.md` | Prometheus alerting rule、状态、for 与证据 | 解释 alerting rule、pending、firing 和 for 如何形成告警状态证据 | `principle` | `17.11`, `17.16` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.18` | `17.18-Alertmanager-grouping-routing-silence-inhibition与去重.md` | Alertmanager grouping、routing、silence、inhibition 与去重 | 区分 grouping、routing、silence、inhibition 和去重的告警处理职责 | `service` | `17.17` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.19` | `17.19-notification-ownership-escalation与事件边界.md` | notification、ownership、escalation 与事件边界 | 将通知、责任归属、升级和确认连接到事件响应边界 | `methodology` | `17.18` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.20` | `17.20-blackbox-synthetic外部视角与内部互证.md` | blackbox、synthetic、外部视角与内部互证 | 使用 blackbox 与 synthetic 外部观测校验内部 telemetry 和告警假设 | `methodology` | `17.19` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.21` | `17.21-日志查询correlation-ID与阶段16边界.md` | 日志查询、correlation ID 与阶段 16 边界 | 复用阶段 16 日志入口并以 correlation ID 建立跨信号查询边界 | `methodology` | `17.03` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.22` | `17.22-trace-span上下文传播与service-graph.md` | trace、span、上下文传播与 service graph | 关联 trace、span、父子关系和 context propagation 形成服务调用图 | `principle` | `17.02` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.23` | `17.23-head-tail-sampling代表性成本隐私与证据.md` | head/tail sampling、代表性、成本、隐私与证据 | 比较 head 与 tail sampling 对代表性、成本、隐私和故障证据的影响 | `methodology` | `17.22` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L4` |
| `17.24` | `17.24-OpenTelemetry-signal-context-resource-attribute与baggage.md` | OpenTelemetry signal、context、resource、attribute 与 baggage | 区分 OpenTelemetry signal、context、resource、attribute 和 baggage 的语义 | `principle` | `17.22` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.25` | `17.25-OpenTelemetry-API-SDK与自动手工instrumentation.md` | OpenTelemetry API、SDK 与自动/手工 instrumentation | 区分 API、SDK、自动与手工 instrumentation 及其语言责任边界 | `methodology` | `17.24` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.26` | `17.26-Collector-receiver-processor-exporter-connector与pipeline.md` | Collector receiver、processor、exporter、connector 与 pipeline | 关联 Collector receiver、processor、exporter、connector 和 pipeline 的职责 | `platform` | `17.25` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.27` | `17.27-semantic-conventions-resource-identity与一致性.md` | semantic conventions、resource identity 与一致性 | 使用 semantic conventions 和 resource identity 维持跨信号语义一致性 | `principle` | `17.26` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.28` | `17.28-Jaeger采集查询存储与运维职责.md` | Jaeger 采集、查询、存储与运维职责 | 区分 Jaeger 采集、查询、存储组件及其运维职责 | `platform` | `17.27` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.29` | `17.29-SkyWalking-agent-OAP-storage-UI与平台职责.md` | SkyWalking agent、OAP、storage、UI 与平台职责 | 区分 SkyWalking agent、OAP、storage 和 UI 的平台职责 | `platform` | `17.27` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.30` | `17.30-追踪后端协议兼容存储拓扑与迁移选择门.md` | 追踪后端、协议、兼容、存储、拓扑与迁移选择门 | 根据协议、兼容、存储、拓扑和迁移约束建立追踪后端选择门 | `methodology` | `17.23`, `17.28`, `17.29` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L4` |
| `17.31` | `17.31-RED-USE-Golden-Signals与分层选择.md` | RED、USE、Golden Signals 与分层选择 | 根据服务、资源和用户视角选择 RED、USE 与 Golden Signals | `methodology` | `17.04`, `17.05` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L3` |
| `17.32` | `17.32-SLI-SLO-error-budget测量接口与治理边界.md` | SLI、SLO、error budget 测量接口与治理边界 | 建立 SLI 的采集与计算接口并将 SLO 和 error budget 治理留给阶段 20 | `methodology` | `17.31` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L4` |
| `17.33` | `17.33-exemplar-correlation-ID-resource-identity跨信号关联.md` | exemplar、correlation ID、resource identity 与跨信号关联 | 使用 exemplar、correlation ID 和 resource identity 关联指标、日志与追踪 | `principle` | `17.14`, `17.21`, `17.27` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L4` |
| `17.34` | `17.34-遥测最小化敏感数据TLS租户保留与审计.md` | 遥测最小化、敏感数据、TLS、租户、保留与审计 | 以最小化、脱敏、TLS、权限、租户隔离、保留和审计保护遥测数据 | `methodology` | `17.33` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L4` |
| `17.35` | `17.35-可观测平台自观测队列容量基数保留与成本.md` | 可观测平台自观测、队列、容量、基数、保留与成本 | 评估可观测平台自身可用性、队列、容量、基数、保留和成本 | `methodology` | `17.13`, `17.30`, `17.34` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L4` |
| `17.36` | `17.36-缺失延迟乱序重复时钟身份与采样偏差排查.md` | 缺失、延迟、乱序、重复、时钟、身份与采样偏差排查 | 识别数据缺失、延迟、乱序、重复、错误身份、时钟和采样偏差 | `methodology` | `17.35` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L4` |
| `17.37` | `17.37-告警仪表盘指标日志追踪与事件证据闭环.md` | 告警、仪表盘、指标、日志、追踪与事件证据闭环 | 汇合告警、仪表盘、指标、日志和追踪形成可质疑的事件证据闭环 | `methodology` | `17.15`, `17.20`, `17.32`, `17.36` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L4` |
| `17.38` | `17.38-可观测性需求信号采集平台关联治理与完整设计.md` | 可观测性需求、信号、采集、平台、关联、治理与完整设计 | 汇合全部章节形成平台中立、可选型、可治理的可观测性完整设计 | `methodology` | `17.37` | 90–120 分钟 | 就业后补学 | `CP-17`, `LAB-L4` |

## 导航

- 上游：[知识库总览](../README.md)
- 前一阶段：[16 企业日志平台](../16-企业日志平台/README.md)
- 后续阶段：[18 AI Infra](../18-AI-Infra/README.md)
- 相关内容：[项目实战](../../项目实战/README.md)

## 边界

当前仅建立阶段骨架，不含正式正文、教学解释、操作步骤、配置、面试答案或故障案例。

- 平台中立主干先定义问题、假设、signal、telemetry、resource、attribute/label、time、identity、quality 和 evidence，再映射 Prometheus、Grafana、OpenTelemetry、Jaeger 与 SkyWalking。monitoring 与 observability 不作同义词，dashboard 数量不代表可观测性成熟度。
- Prometheus、Alertmanager、Grafana、OpenTelemetry、Jaeger/SkyWalking 的精确版本、部署拓扑、长期存储、remote write 后端、exporter、采样率、协议和兼容组合继续保持阶段门；Jaeger 与 SkyWalking 的职责差异必须单独核定，不宣布无差异替换。
- 阶段 16 继续拥有日志采集、处理、存储、查询和生命周期；阶段 17 只复用稳定日志入口，并负责 correlation ID、resource identity 和 exemplar 等跨信号关联语义。阶段 17 只建立 SLI 测量接口，阶段 20 负责 SLO、error budget 和 SRE 治理。
- 遥测可能包含凭据、个人数据、业务标识和拓扑信息，必须在采集前最小化与脱敏，并落实传输和存储权限、租户隔离、保留及审计。高基数、缺失、延迟、乱序、重复、采样偏差、时钟和资源身份漂移都可能改变结论；观测数据不是业务备份，也不是无条件的事实真相。
- 本阶段不安装、配置或运行监控与追踪平台，不创建数据源、仪表盘、查询、告警规则或采样策略，不采集或发送遥测，不选择托管服务，也没有环境验证结果。
