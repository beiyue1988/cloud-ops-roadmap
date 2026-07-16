# 15 DevOps 与 CI/CD

- **阶段编号：** 15
- **阶段名称：** DevOps 与 CI/CD

## 阶段目标

建立设计和维护可回滚交付流水线的能力。

## 主要主题

- Git 工作流
- Jenkins/GitLab CI/GitHub Actions
- 制品库
- 镜像库
- 发布策略

## 前置阶段

- [11 自动化与协作](../11-自动化与协作/README.md)
- [13 Docker 容器](../13-Docker容器/README.md)
- [14 Kubernetes](../14-Kubernetes/README.md)

## 阶段产出

建立可回滚交付流水线。

## 章节清单

| 章节 ID | 预定文件 | 标题 | 主要目标 | type | 直接前置 | 建议投入 | 就业标签 | 实践锚点 |
|---|---|---|---|---|---|---|---|---|
| `15.01` | `15.01-DevOps-CI持续交付部署与价值流边界.md` | DevOps、CI、持续交付、持续部署与价值流边界 | 区分 DevOps、CI、持续交付和持续部署在价值流中的目标与责任边界 | `methodology` | `11.20` | 30–60 分钟 | 就业后补学 | `CP-15` |
| `15.02` | `15.02-pipeline-as-code版本控制与评审.md` | pipeline as code、版本控制与评审 | 通过版本控制、评审和变更历史建立 pipeline as code 的可追溯责任 | `methodology` | `15.01` | 60–90 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.03` | `15.03-触发器来源身份与运行入口.md` | 触发器、来源身份与运行入口 | 区分 commit、branch、tag、PR/MR、schedule 和 manual 触发器及其来源身份 | `principle` | `15.02` | 60–90 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.04` | `15.04-分支保护评审check与合并门.md` | 分支保护、评审、check 与合并门 | 关联分支保护、代码评审和 status/check 形成可审计的合并门 | `methodology` | `15.03` | 60–90 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.05` | `15.05-pipeline-stage-job-step与DAG模型.md` | pipeline、stage、job、step 与 DAG 模型 | 解释 pipeline、stage、job、step、条件和依赖如何组成 DAG 执行模型 | `principle` | `15.04` | 60–90 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.06` | `15.06-runner-agent-executor与高信任执行面.md` | runner、agent、executor 与高信任执行面 | 界定 runner、agent、executor、workspace、隔离和高信任执行面的责任 | `principle` | `15.05` | 60–90 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.07` | `15.07-cache-artifact-workspace与job-output生命周期.md` | cache、artifact、workspace 与 job output 生命周期 | 区分 cache、artifact、workspace 和 job output 的生命周期与可发布边界 | `principle` | `15.06` | 60–90 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.08` | `15.08-variable-secret-mask-scope与OIDC.md` | variable、secret、mask、scope 与 OIDC | 按 scope 管理变量与 Secret 并界定 mask、credential 和短期身份 OIDC 的安全边界 | `methodology` | `15.07` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.09` | `15.09-environment权限分离保护与审批.md` | environment、权限分离、保护与审批 | 使用 environment、保护规则、权限分离和人工审批约束交付目标 | `methodology` | `15.08` | 60–90 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.10` | `15.10-concurrency取消超时重试与失败恢复.md` | concurrency、取消、超时、重试与失败恢复 | 通过并发控制、取消、超时、重试和幂等形成可恢复的流水线运行边界 | `methodology` | `15.09` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.11` | `15.11-测试分层与质量门.md` | 测试分层与质量门 | 组合单元、集成和端到端测试分层形成与风险相称的质量门 | `methodology` | `15.10` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.12` | `15.12-lint静态分析规则与误报例外.md` | lint、静态分析、规则与误报例外 | 使用 lint、静态分析和质量规则建立可审查的误报例外边界 | `methodology` | `15.11` | 60–90 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.13` | `15.13-构建环境依赖锁定与build-once.md` | 构建环境、依赖锁定与 build once | 通过固定构建环境和依赖输入落实可复现构建与 build once 原则 | `methodology` | `15.12` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.14` | `15.14-制品命名版本checksum与不可变身份.md` | 制品命名、版本、checksum 与不可变身份 | 关联制品命名、版本、checksum 和 metadata 形成不可变身份 | `methodology` | `15.13` | 60–90 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.15` | `15.15-制品库上传下载promotion与留存.md` | 制品库上传、下载、promotion 与留存 | 界定制品上传、下载、跨环境 promotion、retention 和清理责任 | `methodology` | `15.14` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.16` | `15.16-镜像流水线tag-digest与可验证输入.md` | 镜像流水线、tag、digest 与可验证输入 | 将容器镜像构建、tag、digest 和 metadata 纳入可验证流水线输入与输出 | `methodology` | `13.31`, `15.15` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.17` | `15.17-registry认证权限promotion与清理.md` | registry 认证、权限、promotion 与清理 | 围绕认证、权限、promotion、retention 和清理建立 registry 生命周期责任 | `methodology` | `15.16` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L2` |
| `15.18` | `15.18-SBOM格式关联与使用边界.md` | SBOM 格式、关联与使用边界 | 解释 SBOM 的生成、格式、制品关联和使用边界 | `principle` | `15.17` | 60–90 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.19` | `15.19-依赖源码镜像扫描与结果解释.md` | 依赖、源码、镜像扫描与结果解释 | 区分依赖、源码和镜像漏洞扫描并解释结果及例外责任 | `methodology` | `15.18` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.20` | `15.20-provenance签名attestation与验证.md` | provenance、签名、attestation 与验证 | 区分 provenance、签名和 attestation 并建立验证与密钥责任边界 | `principle` | `15.19` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.21` | `15.21-policy-gate风险接受与审计证据.md` | policy gate、风险接受与审计证据 | 通过 policy gate、审批、期限和证据管理风险接受与例外 | `methodology` | `15.20` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.22` | `15.22-软件供应链威胁模型.md` | 软件供应链威胁模型 | 沿 source、dependency、build、runner、registry 和 deploy 建立供应链威胁模型 | `principle` | `15.21` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.23` | `15.23-环境配置secret参数与差异控制.md` | 环境配置、Secret、参数与差异控制 | 管理环境配置、Secret 和部署参数并控制环境差异 | `methodology` | `15.22` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.24` | `15.24-recreate-rolling-update与回退边界.md` | recreate、rolling update 与回退边界 | 比较 recreate 与 rolling update 的可用性、容量和回退边界 | `methodology` | `15.23` | 60–90 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.25` | `15.25-blue-green流量切换验证与回退.md` | blue-green 流量切换、验证与回退 | 通过双环境、流量切换和发布验证建立 blue-green 回退模型 | `methodology` | `15.24` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.26` | `15.26-canary渐进交付指标与停止条件.md` | canary、渐进交付、指标与停止条件 | 使用指标判断和停止条件界定 canary 渐进交付的推进与回退 | `methodology` | `15.25` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.27` | `15.27-数据库迁移兼容性与发布顺序.md` | 数据库迁移、兼容性与发布顺序 | 根据向前向后兼容关系规划数据库迁移与应用发布顺序 | `methodology` | `15.26` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.28` | `15.28-发布审批变更窗口与证据包.md` | 发布审批、变更窗口与证据包 | 组织发布审批、变更记录、窗口、责任分离和审计证据包 | `methodology` | `15.27` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.29` | `15.29-rollback-roll-forward与恢复决策.md` | rollback、roll-forward 与恢复决策 | 结合已验证制品 promotion 判断 rollback、roll-forward 和恢复路径 | `methodology` | `15.28` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3`, `PRJ-03-M04` |
| `15.30` | `15.30-Kubernetes交付rollout与rollback.md` | Kubernetes 交付、rollout 与 rollback | 将已验证制品交付到 Kubernetes 并界定 rollout、status 和 rollback 自动化边界 | `methodology` | `14.44`, `15.29` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3`, `PRJ-03-M03` |
| `15.31` | `15.31-GitOps-reconcile期望状态与drift边界.md` | GitOps reconcile、期望状态与 drift 边界 | 解释 GitOps 的 desired state、reconcile 和 drift 并保留产品选型边界 | `principle` | `15.30` | 60–90 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.32` | `15.32-Jenkins-controller-agent与Pipeline适配.md` | Jenkins controller、agent 与 Pipeline 适配 | 将平台中立交付语义映射到 Jenkins controller、agent、Jenkinsfile、plugin 和 credentials | `tool` | `15.31` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.33` | `15.33-GitLab-pipeline-runner与environment适配.md` | GitLab pipeline、runner 与 environment 适配 | 将平台中立交付语义映射到 GitLab pipeline、job、runner、environment、variable 和 component | `tool` | `15.31` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.34` | `15.34-GitHub-workflow-runner与permission适配.md` | GitHub workflow、runner 与 permission 适配 | 将平台中立交付语义映射到 GitHub workflow、job、runner、environment、secret、permission 和 action | `tool` | `15.31` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.35` | `15.35-平台托管runner生态权限成本选择门.md` | 平台、托管、runner、生态、权限与成本选择门 | 依据可迁移合同评估平台、托管方式、runner、插件生态、权限与成本 | `methodology` | `15.32`, `15.33`, `15.34` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3` |
| `15.36` | `15.36-可回滚交付与排障完整闭环.md` | 可回滚交付与排障完整闭环 | 汇合提交、验证、制品、供应链、环境、发布、回退和排障形成完整交付闭环 | `methodology` | `15.35` | 90–120 分钟 | 就业后补学 | `CP-15`, `LAB-L3`, `PRJ-03-M04` |

## 导航

- 上游：[知识库总览](../README.md)
- 前一阶段：[14 Kubernetes](../14-Kubernetes/README.md)
- 后续阶段：[16 企业日志平台](../16-企业日志平台/README.md)
- 相关内容：[项目实战](../../项目实战/README.md)

## 边界

当前仅建立阶段骨架，不含正式正文、教学解释、操作步骤、代码、面试答案或故障案例。

- pipeline、stage、job、step、DAG、runner/agent、artifact、cache、environment、approval 与 release 先按平台中立语义组织；Jenkins、GitLab CI 和 GitHub Actions 只作为适配器，不在本阶段选择唯一平台、托管方式、plugin、runner、action、component、制品库、registry 或 GitOps 产品。
- pipeline as code 必须进入版本控制与评审。runner/agent 是高信任执行面；第三方 plugin、action 和 component 必须固定来源与版本并审查权限。masked secret 不等于不会泄露，优先短期身份与 OIDC，禁止把长期凭据写入仓库、配置或日志。
- cache 不得冒充可发布 artifact；同一已验证制品应跨环境 promotion，避免按环境重新构建。SBOM、扫描、provenance、签名与 attestation 分责；策略例外必须有审批、期限和证据。
- Jenkins/GitLab CI/GitHub Actions 版本、服务 tier、配额、保留期、计费、插件兼容、hosted runner 镜像与仓库产品均保持 phase-gated。本清单不证明任何平台已经安装、授权或运行。
- 阶段 11 保有 Git、协作与制品治理基础，阶段 13 保有镜像构建与单机容器，阶段 14 保有 Kubernetes 对象和人工发布语义；阶段 15 只负责自动化交付编排与供应链基础。阶段 16/17 保有集中日志和完整可观测平台，本阶段只保留流水线日志、状态、通知和发布验证入口。
