# 19 AIOps 与 MLOps 入门

- **阶段编号：** 19
- **阶段名称：** AIOps 与 MLOps 入门

## 阶段目标

建立判断 AIOps 与 MLOps 入门场景、收益和风险边界的能力。

## 主要主题

- AI 辅助运维边界
- 日志分析
- 告警降噪
- 知识库
- MLflow/Kubeflow 概览

## 前置阶段

- [16 企业日志平台](../16-企业日志平台/README.md)
- [17 监控与可观测性](../17-监控与可观测性/README.md)
- [18 AI Infra](../18-AI-Infra/README.md)

## 阶段产出

能判断可用场景与风险。

## 章节清单

| 章节 ID | 预定文件 | 标题 | 主要目标 | type | 直接前置 | 建议投入 | 就业标签 | 实践锚点 |
|---|---|---|---|---|---|---|---|---|
| `19.01` | `19.01-AIOps-MLOps-AI-Infra角色对象责任与交接边界.md` | AIOps、MLOps、AI Infra 角色、对象、责任与交接边界 | 区分 AIOps、MLOps 与 AI Infra 的服务对象、责任和交接边界 | `concept` | `17.38` | 30–60 分钟 | 就业后补学 | `CP-19` |
| `19.02` | `19.02-AI辅助增强自动决策分级与问题边界.md` | AI 辅助、增强、自动决策分级与问题边界 | 按辅助、增强和自动决策分级定义问题、责任与不可接受结果 | `methodology` | `19.01` | 60–90 分钟 | 就业后补学 | `CP-19` |
| `19.03` | `19.03-log-metric-trace-alert-ticket-change-topology数据源.md` | log、metric、trace、alert、ticket、change 与 topology 数据源 | 识别运维 AI 场景所需数据源及各自能够提供的证据 | `concept` | `19.02` | 60–90 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.04` | `19.04-时间身份拓扑schema新鲜度缺失与数据质量.md` | 时间、身份、拓扑、schema、新鲜度、缺失与数据质量 | 从时间、身份、拓扑、schema、新鲜度和缺失判断运维数据质量 | `methodology` | `19.03` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.05` | `19.05-ground-truth-label弱监督leakage-bias与代表性.md` | ground truth、label、弱监督、leakage、bias 与代表性 | 评估 ground truth、label、弱监督、leakage、bias 和样本代表性边界 | `methodology` | `19.04` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.06` | `19.06-用例价值可行性风险基线成本与停止条件.md` | 用例价值、可行性、风险、基线、成本与停止条件 | 以价值、可行性、风险、基线和成本建立用例进入与停止条件 | `methodology` | `19.05` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.07` | `19.07-日志模板聚类异常语义归组与证据边界.md` | 日志模板、聚类、异常、语义归组与证据边界 | 判断日志模板、聚类、异常和语义归组结果能够支持的证据范围 | `methodology` | `19.06` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.08` | `19.08-指标基线趋势季节性异常与概念漂移.md` | 指标基线、趋势、季节性、异常与概念漂移 | 区分指标趋势、季节性、异常和概念漂移并保留误判边界 | `methodology` | `19.06` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.09` | `19.09-告警去重抑制关联根因假设与误报漏报.md` | 告警去重、抑制、关联、根因假设与误报漏报 | 将告警去重、抑制和关联限定为可验证的根因假设而非根因结论 | `methodology` | `19.06` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.10` | `19.10-服务拓扑依赖变更事件时间线与因果边界.md` | 服务拓扑、依赖、变更、事件时间线与因果边界 | 关联服务拓扑、依赖、变更和事件时间线并区分相关与因果 | `methodology` | `19.06` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.11` | `19.11-incident摘要证据引用不确定性与事实推断分离.md` | incident 摘要、证据引用、不确定性与事实推断分离 | 生成可追溯事件摘要并明确区分事实、推断、假设与不确定性 | `methodology` | `19.07`, `19.08`, `19.09`, `19.10` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.12` | `19.12-运维知识库来源所有权版本审查过期与反馈.md` | 运维知识库来源、所有权、版本、审查、过期与反馈 | 建立运维知识来源从所有权、版本、审查到过期反馈的生命周期 | `methodology` | `19.11` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.13` | `19.13-chunk-metadata-ACL检索rerank与上下文构建.md` | chunk、metadata、ACL、检索、rerank 与上下文构建 | 解释 chunk、metadata、ACL、检索和 rerank 如何形成受控上下文 | `principle` | `19.12` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.14` | `19.14-embedding向量索引数据库reranker模型与成本选择门.md` | embedding、向量索引/数据库、reranker、模型与成本选择门 | 建立 embedding、向量存储、reranker、模型和成本的后续选择门 | `methodology` | `19.13` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.15` | `19.15-RAG-query-retrieve-rerank-generate-citation与失败模式.md` | RAG query、retrieve、rerank、generate、citation 与失败模式 | 解释 RAG 全流程及检索、生成、引用和权限失败模式 | `principle` | `19.14` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.16` | `19.16-prompt间接注入泄露越权工具与不安全输出.md` | prompt/indirect injection、泄露、越权工具与不安全输出 | 识别直接与间接注入、数据泄露、越权工具调用和不安全输出风险 | `methodology` | `19.15` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L4` |
| `19.17` | `19.17-输出校验来源核对不确定性人类批准与责任.md` | 输出校验、来源核对、不确定性、人类批准与责任 | 通过来源核对、输出校验、不确定性披露和人类批准维持责任边界 | `methodology` | `19.16` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L4` |
| `19.18` | `19.18-自动动作风险最小权限dry-run回退审计与kill-switch.md` | 自动动作风险、最小权限、dry-run、回退、审计与 kill switch | 按动作风险建立最小权限、预演、影响预览、回退、限速、审计和停止控制 | `methodology` | `19.17` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L4` |
| `19.19` | `19.19-离线golden-set回放任务业务效用与安全评估.md` | 离线 golden set、回放、任务、业务效用与安全评估 | 组合离线 golden set、回放、任务指标、业务效用和安全指标形成评估基线 | `methodology` | `19.18` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.20` | `19.20-shadow-AB-canary人工反馈在线监控与回滚.md` | shadow、A/B、canary、人工反馈、在线监控与回滚 | 使用 shadow、A/B、canary 和人工反馈界定在线验证、停止与回滚 | `methodology` | `19.19` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L4` |
| `19.21` | `19.21-AIOps系统数据质量延迟成本失败采纳与自观测.md` | AIOps 系统数据质量、延迟、成本、失败、采纳与自观测 | 为 AIOps 系统建立数据质量、延迟、成本、失败和用户采纳的自观测边界 | `methodology` | `19.20` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L4` |
| `19.22` | `19.22-data-concept-model-drift信号误判与再验证.md` | data、concept、model drift、信号、误判与再验证 | 区分 data、concept 与 model drift 并用多信号触发再验证 | `methodology` | `19.21` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L4` |
| `19.23` | `19.23-data-code-model-environment-lineage与MLOps生命周期.md` | data、code、model、environment、lineage 与 MLOps 生命周期 | 关联数据、代码、模型和环境 lineage 建立 MLOps 生命周期 | `methodology` | `19.22` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.24` | `19.24-MLflow-experiment-run-metric-artifact与registry概览.md` | MLflow experiment、run、metric、artifact 与 registry 概览 | 概览 MLflow 的 experiment、run、metric、artifact 和 model registry 职责 | `tool` | `19.23` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.25` | `19.25-Kubeflow-component-pipeline-training-serving与平台概览.md` | Kubeflow component、pipeline、training/serving 与平台概览 | 概览 Kubeflow component、pipeline 以及训练与服务交接的平台职责 | `platform` | `19.23` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.26` | `19.26-model-packaging-serving-handoff接口环境与AI-Infra边界.md` | model packaging、serving handoff、接口、环境与 AI Infra 边界 | 界定模型封装、服务交接、接口和环境与阶段 18 运行基础设施的责任边界 | `methodology` | `19.24`, `19.25` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L3` |
| `19.27` | `19.27-approval-release-rollback-promotion-lineage与审计.md` | approval、release、rollback、promotion、lineage 与审计 | 通过审批、发布、回退、promotion、lineage 和审计治理模型交付 | `methodology` | `19.26` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L4` |
| `19.28` | `19.28-数据模型代码安全隐私许可证供应链与治理.md` | 数据、模型、代码安全、隐私、许可证、供应链与治理 | 评估数据、模型和代码的安全、隐私、许可证与供应链治理责任 | `methodology` | `19.27` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L4` |
| `19.29` | `19.29-build-buy平台供应商锁定运营成本ROI与采用门.md` | build/buy、平台、供应商、锁定、运营成本、ROI 与采用门 | 基于 build/buy、供应商锁定、运营成本和 ROI 建立平台采用门 | `methodology` | `19.28` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L4` |
| `19.30` | `19.30-问题数据模型评估发布监控治理与完整决策闭环.md` | 问题、数据、模型、评估、发布、监控、治理与完整决策闭环 | 汇合全部章节形成可停止、可回退、可审计的 AIOps/MLOps 评估与治理闭环 | `methodology` | `19.29` | 90–120 分钟 | 就业后补学 | `CP-19`, `LAB-L4` |

## 导航

- 上游：[知识库总览](../README.md)
- 前一阶段：[18 AI Infra](../18-AI-Infra/README.md)
- 后续阶段：[20 SRE 与架构能力](../20-SRE与架构能力/README.md)
- 相关内容：[运维思维训练](../../运维思维训练/README.md)

## 边界

当前仅建立阶段骨架，不含正式正文、教学解释、操作步骤、代码、面试答案或故障案例。

- AI Infra 负责 GPU、推理运行与资源基础设施，AIOps 负责使用 AI 辅助日志、指标、告警、故障假设、巡检和处置决策，MLOps 负责数据、代码、实验、模型、环境、发布、监控与治理生命周期；三者不合并成单一平台，AIOps 也不等同于大模型聊天助手。
- AIOps 场景先定义问题、不可接受结果、数据身份、时间、拓扑、变更、ticket、ground truth、label leakage、偏差、质量和停止条件。日志、指标、告警、拓扑和事件摘要的输出只形成待验证假设或建议，不冒充已经确认的根因。
- 知识库与 RAG 只保留文档生命周期、权限、chunk、metadata、retrieve、rerank、generate、citation 和反馈流程。embedding、向量索引或数据库、reranker、模型、上下文、托管 API、部署方式和成本均为后续选择门；检索命中不自动证明来源正确、权限合规或答案可信。
- 直接与间接 prompt injection、敏感信息泄露、越权工具调用、不安全输出、过度代理和供应链都属于治理边界。高风险动作必须经过人类批准、最小权限、dry-run、影响预览、幂等、回退、限速、审计和 kill switch；本阶段不设计实际自动处置工作流。
- 评估区分离线 golden set 与回放、检索/生成/分类/排序任务指标、业务效用、安全指标，以及 shadow、A/B、canary、人工反馈、在线监控和回滚。数据、概念或模型漂移必须由多项证据和再验证判断，不能凭单一指标直接下结论。
- MLOps 覆盖 data/code/model/environment lineage、experiment、run、artifact、model registry、pipeline、orchestration、packaging、serving handoff、approval、release、rollback、monitoring、drift 与治理。MLflow 和 Kubeflow 仅作不同职责的教学概览，不选择版本、部署、存储、registry、pipeline engine、Kubernetes 组合或生产主平台，也不进行训练。
- NIST AI RMF 1.0 官方入口当前明确处于修订中，Playbook 将在框架修订后更新。本阶段只借鉴 Govern、Map、Measure、Manage 等自愿风险管理思想，不锁定框架版本，也不把自愿指南表述为强制合规；NIST、MLflow、Kubeflow 和 OWASP 入口在正式正文或实验进入 `ready` 前重新核定。
- 本阶段不选择模型、embedding、向量库、AI 平台或自动处置方案，不依赖阶段 18 的 GPU 或推理平台选型，不创建 prompt、查询、规则、工作流、配置或代码，不安装、下载、训练、导入数据、调用外部 AI API、触发自动动作、使用凭据或执行远程写。
