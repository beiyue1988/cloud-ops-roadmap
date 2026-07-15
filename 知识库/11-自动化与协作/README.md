# 11 自动化与协作

- **阶段编号：** 11
- **阶段名称：** 自动化与协作

## 阶段目标

建立通过协作、配置管理和基础设施即代码批量管理资源的能力。

## 主要主题

- Git
- Ansible
- 制品
- 配置管理
- Terraform/OpenTofu 基础
- 运维 API

## 前置阶段

- [08 Shell 与 Python](../08-Shell与Python/README.md)
- [09 企业基础服务](../09-企业基础服务/README.md)

## 阶段产出

能批量配置和管理资源。

## 章节清单

| 章节 ID | 预定文件 | 标题 | 主要目标 | type | 直接前置 | 建议投入 | 就业标签 | 实践锚点 |
|---|---|---|---|---|---|---|---|---|
| `11.01` | `11.01-自动化协作标准化审计与责任边界.md` | 自动化、协作、标准化、审计与责任边界 | 从标准化、协作、审计和变更责任判断自动化的适用边界 | `methodology` | `10.28` | 30–60 分钟 | 必须学 | `CP-11` |
| `11.02` | `11.02-Git分布式仓库快照对象与身份.md` | Git 分布式仓库、快照、对象与身份 | 解释分布式仓库、快照、对象和身份如何构成 Git 的可追溯记录 | `principle` | `11.01` | 60–90 分钟 | 必须学 | `CP-11`, `LAB-L1` |
| `11.03` | `11.03-Git工作区暂存区提交与原子变更.md` | Git 工作区、暂存区、提交与原子变更 | 关联工作区、暂存区和提交形成边界清楚的原子变更 | `tool` | `11.02` | 60–90 分钟 | 必须学 | `CP-11`, `LAB-L1` |
| `11.04` | `11.04-Git历史差异引用与安全撤销.md` | Git 历史、差异、引用与安全撤销 | 根据 history、diff 和引用证据选择安全撤销并识别破坏性历史重写边界 | `methodology` | `11.03` | 60–90 分钟 | 必须学 | `CP-11`, `LAB-L1` |
| `11.05` | `11.05-Git分支合并rebase与冲突责任.md` | Git 分支、合并、rebase 与冲突责任 | 判断分支、合并和 rebase 的适用责任并形成可审查的冲突解决证据 | `methodology` | `11.04` | 90–120 分钟 | 必须学 | `CP-11`, `LAB-L2` |
| `11.06` | `11.06-Git远程跟踪fetch-pull-push边界.md` | Git 远程跟踪与 fetch、pull、push 边界 | 区分 remote、远程跟踪、fetch、pull 和 push 的数据流及外部写责任 | `tool` | `11.05` | 60–90 分钟 | 必须学 | `CP-11`, `LAB-L1` |
| `11.07` | `11.07-Git协作评审tag与版本证据.md` | Git 协作、评审、tag 与版本证据 | 用提交身份、评审入口和 tag 组织可追溯的协作与版本证据 | `methodology` | `11.06` | 90–120 分钟 | 必须学 | `CP-11`, `LAB-L2` |
| `11.08` | `11.08-配置环境Secret与泄露边界.md` | 配置、环境、Secret 与泄露边界 | 按环境与敏感度管理配置、Secret、忽略和属性规则并识别泄露责任 | `methodology` | `11.07` | 90–120 分钟 | 必须学 | `CP-11`, `LAB-L2` |
| `11.09` | `11.09-制品身份版本校验和与来源责任.md` | 制品身份、版本、校验和与来源责任 | 通过身份、版本、校验和、来源和留存边界建立可验证的制品责任 | `methodology` | `11.08` | 60–90 分钟 | 必须学 | `CP-11` |
| `11.10` | `11.10-Ansible控制端受管端SSH与兼容边界.md` | Ansible 控制端、受管端、SSH 与兼容边界 | 解释控制端、受管端、SSH 和 Python 兼容关系并界定执行链责任 | `tool` | `03.16`, `11.09` | 60–90 分钟 | 必须学 | `CP-11`, `LAB-L1` |
| `11.11` | `11.11-Ansible-Inventory-Host-Group与Pattern.md` | Ansible Inventory、Host、Group 与 Pattern | 使用 Inventory、Host、Group、Pattern 和连接变量描述受管范围 | `tool` | `11.10` | 60–90 分钟 | 必须学 | `CP-11`, `LAB-L1` |
| `11.12` | `11.12-Ansible配置发现变量作用域与优先级.md` | Ansible 配置发现、变量作用域与优先级 | 根据配置发现、变量来源、作用域和优先级判断最终生效值 | `principle` | `11.11` | 60–90 分钟 | 必须学 | `CP-11`, `LAB-L1` |
| `11.13` | `11.13-Ansible-Ad-hoc-Module与结果边界.md` | Ansible Ad hoc、Module 与结果边界 | 区分 Ad hoc、Module、command 和 shell 并解释返回结果的证据边界 | `tool` | `11.12` | 60–90 分钟 | 必须学 | `CP-11`, `LAB-L1` |
| `11.14` | `11.14-Ansible-Playbook-FQCN与幂等目标.md` | Ansible Playbook、FQCN 与幂等目标 | 关联 Playbook、Play、Task、Module 和 FQCN 表达幂等的目标状态 | `tool` | `11.13` | 90–120 分钟 | 必须学 | `CP-11`, `LAB-L2` |
| `11.15` | `11.15-Ansible-Facts-register条件循环与数据流.md` | Ansible Facts、register、条件、循环与数据流 | 通过 Facts、register、条件和循环组织可检查的执行数据流 | `principle` | `11.14` | 60–90 分钟 | 必须学 | `CP-11`, `LAB-L1` |
| `11.16` | `11.16-Ansible-file-template与Handler.md` | Ansible file、template 与 Handler | 使用 file、template 和 Handler 形成受控配置生成与按需变更链 | `methodology` | `11.15` | 90–120 分钟 | 必须学 | `CP-11`, `LAB-L2` |
| `11.17` | `11.17-Ansible-Role-Collection与复用边界.md` | Ansible Role、Collection 与复用边界 | 根据 Role、Collection、Import、Include 和依赖关系判断复用边界 | `methodology` | `11.16` | 90–120 分钟 | 必须学 | `CP-11`, `LAB-L2` |
| `11.18` | `11.18-Ansible-Vault-become与最小权限.md` | Ansible Vault、become 与最小权限 | 界定 Vault、Secret、become、执行身份和最小权限之间的安全责任 | `methodology` | `11.17` | 90–120 分钟 | 必须学 | `CP-11`, `LAB-L2` |
| `11.19` | `11.19-Ansible检查批次失败与回滚证据.md` | Ansible 检查、批次、失败与回滚证据 | 组合 check、diff、syntax、tag、limit、批次和失败控制形成回滚证据 | `methodology` | `11.18` | 90–120 分钟 | 必须学 | `CP-11`, `LAB-L2` |
| `11.20` | `11.20-Git-Ansible批量配置核心证据闭环.md` | Git 与 Ansible 批量配置核心证据闭环 | 汇合 Git 评审、Ansible 目标状态、二次运行和失败证据形成就业核心闭环 | `methodology` | `11.19` | 90–120 分钟 | 必须学 | `CP-11`, `LAB-L2` |
| `11.21` | `11.21-运维API认证幂等限流与审计交付.md` | 运维 API 认证、幂等、限流与审计交付 | 组织认证、幂等、分页、限流、错误和审计证据形成运维 API 交付边界 | `methodology` | `08.32`, `11.20` | 90–120 分钟 | 建议学 | `CP-11`, `LAB-L2` |
| `11.22` | `11.22-IaC声明式资源依赖图与Provider边界.md` | IaC 声明式资源、依赖图与 Provider 边界 | 解释声明式资源、依赖图、Provider 和 API 之间的职责边界 | `principle` | `11.20` | 60–90 分钟 | 建议学 | `CP-11`, `LAB-L1` |
| `11.23` | `11.23-HCL-block-expression与输入输出.md` | HCL block、expression 与输入输出 | 使用 block、expression、variable、locals 和 outputs 表达 IaC 输入与结果 | `language` | `11.22` | 60–90 分钟 | 建议学 | `CP-11`, `LAB-L1` |
| `11.24` | `11.24-IaC初始化校验plan-apply与审查.md` | IaC 初始化、校验、plan、apply 与审查 | 关联 init、fmt、validate、plan 和 apply 建立计划审查与变更边界 | `methodology` | `11.23` | 90–120 分钟 | 建议学 | `CP-11`, `LAB-L2` |
| `11.25` | `11.25-IaC-State对象身份安全与锁.md` | IaC State 对象身份、安全与锁 | 解释 State 中的对象身份并界定保护、远端存储和锁的安全责任 | `principle` | `11.24` | 90–120 分钟 | 建议学 | `CP-11`, `LAB-L2` |
| `11.26` | `11.26-IaC-Module输入输出组合与复用.md` | IaC Module 输入输出、组合与复用 | 使用 Module 输入输出组合资源并判断复用与抽象边界 | `methodology` | `11.25` | 60–90 分钟 | 建议学 | `CP-11`, `LAB-L1` |
| `11.27` | `11.27-Provider-Module版本锁定与供应链.md` | Provider、Module 版本锁定与供应链 | 通过版本约束、锁文件、来源和校验责任控制 Provider 与 Module 供应链 | `methodology` | `11.26` | 90–120 分钟 | 建议学 | `CP-11`, `LAB-L2` |
| `11.28` | `11.28-IaC漂移import-moved与恢复边界.md` | IaC 漂移、import、moved 与恢复边界 | 围绕漂移、import、moved、重构和替换组织可恢复的状态变更 | `methodology` | `11.27` | 90–120 分钟 | 建议学 | `CP-11`, `LAB-L2` |
| `11.29` | `11.29-Terraform-OpenTofu选择与IaC证据闭环.md` | Terraform、OpenTofu 选择与 IaC 证据闭环 | 比较许可证与兼容边界并汇合计划、State、供应链和漂移证据形成完整 IaC 闭环 | `methodology` | `11.28` | 90–120 分钟 | 建议学 | `CP-11`, `LAB-L2` |

## 导航

- 上游：[知识库总览](../README.md)
- 前一阶段：[10 数据服务](../10-数据服务/README.md)
- 后续阶段：[12 虚拟化与阿里云](../12-虚拟化与阿里云/README.md)
- 相关内容：[脚本资源](../../脚本资源/README.md)

## 边界

当前仅建立阶段骨架，不含正式正文、教学解释、操作步骤、代码、面试答案或故障案例。
