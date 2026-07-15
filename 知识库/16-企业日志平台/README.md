# 16 企业日志平台

- **阶段编号：** 16
- **阶段名称：** 企业日志平台

## 阶段目标

建立集中采集、传输、存储和查询企业日志的能力。

## 主要主题

- Filebeat/Fluent Bit
- Logstash
- Kafka
- Elasticsearch
- Kibana
- Loki
- 生命周期

## 前置阶段

- [06 Linux 日志体系](../06-Linux日志体系/README.md)
- [10 数据服务](../10-数据服务/README.md)
- [14 Kubernetes](../14-Kubernetes/README.md)

## 阶段产出

建立集中日志平台。

## 章节清单

| 章节 ID | 预定文件 | 标题 | 主要目标 | type | 直接前置 | 建议投入 | 就业标签 | 实践锚点 |
|---|---|---|---|---|---|---|---|---|
| `16.01` | `16.01-单机日志与集中平台职责边界.md` | 单机日志与集中平台职责边界 | 区分单机日志与集中日志平台的 SLA、共享责任和证据边界 | `concept` | `06.26` | 30–60 分钟 | 就业后补学 | `CP-16` |
| `16.02` | `16.02-日志事件记录字段流与事件身份.md` | 日志事件、记录、字段、流与事件身份 | 区分 log event、source、record、field 和 stream 并建立事件身份 | `principle` | `16.01` | 60–90 分钟 | 就业后补学 | `CP-16` |
| `16.03` | `16.03-source-collector-transport-processor-store-query管道.md` | source、collector、transport、processor、store 与 query 管道 | 使用六层角色建立与产品无关的集中日志管道模型 | `principle` | `16.02` | 60–90 分钟 | 就业后补学 | `CP-16` |
| `16.04` | `16.04-时间主机服务容器与correlation-ID身份.md` | 时间、主机、服务、容器与 correlation ID 身份 | 关联 timestamp、timezone、host、service、container 和 correlation ID 形成可追踪事件身份 | `principle` | `16.02` | 60–90 分钟 | 就业后补学 | `CP-16` |
| `16.05` | `16.05-文本JSON-schema字段命名与演进.md` | 文本、JSON、schema、字段命名与演进 | 区分文本与 JSON 日志并建立可演进的 schema 和字段命名边界 | `principle` | `16.04` | 60–90 分钟 | 就业后补学 | `CP-16` |
| `16.06` | `16.06-multiline-encoding截断与解析失败.md` | multiline、encoding、截断与解析失败 | 判断多行、编码、截断、超长事件和解析失败对事件边界的影响 | `principle` | `16.05` | 60–90 分钟 | 就业后补学 | `CP-16` |
| `16.07` | `16.07-敏感日志最小化脱敏租户权限与审计.md` | 敏感日志最小化、脱敏、租户、权限与审计 | 从采集前最小化、脱敏、租户隔离和最小权限界定敏感日志治理边界 | `methodology` | `16.05` | 90–120 分钟 | 就业后补学 | `CP-16` |
| `16.08` | `16.08-agent-daemon-sidecar-DaemonSet与gateway拓扑.md` | agent、daemon、sidecar、DaemonSet 与 gateway 拓扑 | 比较 agent、daemon、sidecar、DaemonSet 和 gateway 的采集职责与故障域 | `principle` | `16.03`, `16.07` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.09` | `16.09-Filebeat-input-harvester-registry与output边界.md` | Filebeat input、harvester、registry 与 output 边界 | 解释 Filebeat input、harvester、registry 和 output 的职责及 Elastic 输出边界 | `tool` | `16.08` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.10` | `16.10-Fluent-Bit-input-filter-buffer与output边界.md` | Fluent Bit input、filter、buffer 与 output 边界 | 解释 Fluent Bit input、filter、buffer 和 output 的职责及多后端边界 | `tool` | `16.08` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.11` | `16.11-Kubernetes节点文件runtime-metadata与采集拓扑.md` | Kubernetes 节点文件、runtime、metadata 与采集拓扑 | 关联节点日志文件、容器 runtime、metadata 和 DaemonSet 形成 Kubernetes 采集拓扑 | `methodology` | `14.44`, `16.08` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.12` | `16.12-offset-checkpoint-state与重复丢失边界.md` | offset、checkpoint、state 与重复丢失边界 | 关联采集状态、文件轮转、重复、丢失和幂等形成可验证的读取边界 | `principle` | `16.06`, `16.09`, `16.10`, `16.11` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.13` | `16.13-buffer-backpressure-batch-retry与delivery.md` | buffer、backpressure、batch、retry 与 delivery | 解释缓冲、背压、批次、重试和 delivery 语义如何影响重复、丢失与乱序 | `principle` | `16.12` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.14` | `16.14-网络TLS认证授权压缩与传输失败.md` | 网络、TLS、认证、授权、压缩与传输失败 | 从网络、TLS、身份、权限和压缩界定日志传输安全及失败证据 | `methodology` | `16.13` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.15` | `16.15-Logstash-input-filter-output-pipeline与worker.md` | Logstash input、filter、output、pipeline 与 worker | 解释 Logstash pipeline、plugin 和 worker 的处理职责与并发边界 | `tool` | `16.14` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.16` | `16.16-JSON-grok-dissect时间与多行解析策略.md` | JSON、grok、dissect、时间与多行解析策略 | 根据输入稳定性选择 JSON、grok、dissect、时间和多行解析策略 | `methodology` | `16.15` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.17` | `16.17-enrich-normalize-rename-drop与route治理.md` | enrich、normalize、rename、drop 与 route 治理 | 通过增强、规范化、重命名、丢弃和路由维持 schema 治理边界 | `methodology` | `16.16` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.18` | `16.18-parsing-failure隔离重放与证据.md` | parsing failure 隔离、重放与证据 | 使用 dead letter 或 quarantine 隔离解析失败并界定重放和验收证据 | `methodology` | `16.17` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.19` | `16.19-Kafka可选缓冲解耦保留与边界.md` | Kafka 可选缓冲、解耦、保留与边界 | 将 Kafka 限定为日志管道的可选缓冲与解耦层并复用阶段 10 的消息语义 | `service` | `10.27`, `16.14` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.20` | `16.20-Elasticsearch-document-index-mapping-search与聚合.md` | Elasticsearch document、index、mapping、search 与聚合 | 关联 document、index、mapping、search 和 aggregation 建立检索数据模型 | `service` | `16.18` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.21` | `16.21-shard-replica-allocation容量与故障域.md` | shard、replica、allocation、容量与故障域 | 解释 shard、replica 和 allocation 如何约束容量、可用性与故障域 | `principle` | `16.20` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.22` | `16.22-data-stream-index-template-mapping与rollover.md` | data stream、index template、mapping 与 rollover | 关联 data stream、index template、mapping template 和 rollover 形成时序日志生命周期入口 | `principle` | `16.20` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.23` | `16.23-ILM-retention冷热层与删除责任.md` | ILM、retention、冷热层与删除责任 | 使用 ILM 界定 hot、warm、cold、frozen、保留和删除责任 | `methodology` | `16.21`, `16.22` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.24` | `16.24-Kibana-data-view-Discover-query与dashboard.md` | Kibana data view、Discover、query 与 dashboard | 使用 data view、Discover、query、visualization 和 dashboard 建立日志查询入口 | `tool` | `16.20` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.25` | `16.25-Elastic-TLS用户角色API-key与最小权限.md` | Elastic TLS、用户、角色、API key 与最小权限 | 从 TLS、用户、角色和 API key 建立 Elastic 最小权限与凭据边界 | `methodology` | `16.23`, `16.24` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.26` | `16.26-OpenSearch-Dashboards-Data-Prepper插件与兼容边界.md` | OpenSearch、Dashboards、Data Prepper、插件与兼容边界 | 区分 OpenSearch、Dashboards、Data Prepper 和插件职责并保留客户端兼容选择门 | `platform` | `16.18` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.27` | `16.27-Loki-stream-label-chunk-index与低索引模型.md` | Loki stream、label、chunk、index 与低索引模型 | 解释 Loki 以 label 选择 stream 并分离 chunk 与 index 的低索引模型 | `principle` | `16.18` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.28` | `16.28-Loki-ingestion-storage-query-frontend与LogQL.md` | Loki ingestion、storage、query frontend 与 LogQL | 关联 Loki ingestion、storage、query frontend 和 LogQL 的组件职责 | `platform` | `16.27` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.29` | `16.29-Grafana-Explore-dashboard变量与日志查询.md` | Grafana Explore、dashboard、变量与日志查询 | 使用 Explore、dashboard 和变量建立 Loki 日志查询入口 | `tool` | `16.28` | 60–90 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.30` | `16.30-Promtail-EOL与采集客户端迁移选择门.md` | Promtail EOL 与采集客户端迁移选择门 | 根据 Promtail EOL 边界评估 Alloy、OpenTelemetry Collector、Fluent Bit 等受支持迁移路径 | `methodology` | `16.29` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L3` |
| `16.31` | `16.31-保留抽样压缩基数容量成本与查询性能.md` | 保留、抽样、压缩、基数、容量、成本与查询性能 | 综合三类后端的保留、丢弃、压缩、基数、容量、成本和查询性能形成容量模型 | `methodology` | `16.19`, `16.25`, `16.26`, `16.30` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L4` |
| `16.32` | `16.32-HA故障域snapshot-backup-restore与灾难边界.md` | HA、故障域、snapshot、backup、restore 与灾难边界 | 区分高可用、快照、备份和恢复并界定业务日志源与平台灾难恢复责任 | `methodology` | `16.31` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L4` |
| `16.33` | `16.33-日志管道各层自监控与SLI.md` | 日志管道各层自监控与 SLI | 为 collector、queue、processor、store 和 query 定义平台健康信号与 SLI | `methodology` | `16.32` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L4` |
| `16.34` | `16.34-source到collector权限路径轮转格式与状态排障.md` | source 到 collector 的权限、路径、轮转、格式与状态排障 | 沿 source 到 collector 检查权限、路径、轮转、格式和读取状态证据 | `methodology` | `16.33` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L4` |
| `16.35` | `16.35-transport-process-store-query分层排障与重放.md` | transport、process、store、query 分层排障与重放 | 沿传输、处理、存储和查询链路定位故障并界定重放的重复与安全边界 | `methodology` | `16.34` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L4` |
| `16.36` | `16.36-安全容量成本schema升级迁移与变更治理.md` | 安全、容量、成本、schema、升级、迁移与变更治理 | 汇合安全、容量、成本和 schema 证据形成可回退的升级迁移与变更治理门 | `methodology` | `16.35` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L4` |
| `16.37` | `16.37-日志平台选择架构运维恢复与完整证据闭环.md` | 日志平台选择、架构、运维、恢复与完整证据闭环 | 汇合需求、选择、架构、采集、查询、运维和恢复形成日志平台完整证据闭环 | `methodology` | `16.36` | 90–120 分钟 | 就业后补学 | `CP-16`, `LAB-L4` |

## 导航

- 上游：[知识库总览](../README.md)
- 前一阶段：[15 DevOps 与 CI/CD](../15-DevOps与CI-CD/README.md)
- 后续阶段：[17 监控与可观测性](../17-监控与可观测性/README.md)
- 相关内容：[故障案例](../../故障案例/README.md)

## 边界

当前仅建立阶段骨架，不含正式正文、教学解释、操作步骤、配置、面试答案或故障案例。

- 平台中立主干先定义 source、collector、transport、processor、store、query、事件身份、schema、delivery、backpressure、retention 和 evidence，再分别映射 Elastic、OpenSearch 与 Loki；三条后端不是无差异替换品，本阶段不选择全局主栈、组件版本、拓扑、存储、许可证或订阅、资源规格和托管方式。
- Elastic Stack 内部组件组合必须按官方 support matrix 取交集。Filebeat 官方直接输出目标为 Elasticsearch 或 Logstash，不得外推现代 Elastic Beats 可直接兼容 OpenSearch；OpenSearch 官方说明新于 Beats OSS 7.12.x 的 Beats 不受支持，后续只能在兼容 Logstash 与 OpenSearch output plugin 等路径重新核定后使用。
- Promtail 已于 2026-03-02 EOL，不得作为新部署默认采集器。Loki 采集在后续阶段门中比较 Grafana Alloy、OpenTelemetry Collector、Fluent Bit 和其他受支持客户端；第三方客户端的支持责任不得归为 Loki 官方同等责任。
- 日志可能包含凭据、个人数据和业务敏感数据，必须在采集前最小化和脱敏，并落实 TLS、认证、授权、租户隔离与审计。高基数 label 或 field、mapping explosion、重复、丢失、乱序、背压和 retention 成本均属于设计边界；平台备份、快照和恢复不能冒充业务日志源的恢复能力。
- Kafka 只作为可选缓冲和解耦层，不重复阶段 10 的消息系统运维。阶段 06 保有单机日志源、轮转和审计入口，阶段 13/14 保有容器与 Kubernetes 日志产生和运行语义；阶段 16 负责集中采集、处理、存储、查询和生命周期，阶段 17 负责指标、告警、追踪和跨信号可观测性。
- 本阶段不扩展到 SIEM/SOC、完整合规、日志驱动 AIOps、指标或追踪平台和云厂商托管选型；没有安装、启动、传输、建索引、集群变更或环境验证结果。
