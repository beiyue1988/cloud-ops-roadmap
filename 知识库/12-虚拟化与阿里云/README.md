# 12 虚拟化与阿里云

- **阶段编号：** 12
- **阶段名称：** 虚拟化与阿里云

## 阶段目标

建立规划和维护基础虚拟化与阿里云资源架构的能力。

## 主要主题

- KVM/VMware 原理
- ECS
- VPC
- 交换机
- 安全组
- SLB
- OSS
- 云盘
- RDS
- RAM

## 前置阶段

- [01 计算机与服务器基础](../01-计算机与服务器基础/README.md)
- [02 网络基础](../02-网络基础/README.md)
- [11 自动化与协作](../11-自动化与协作/README.md)

## 阶段产出

能搭建基础云上架构。

## 章节清单

| 章节 ID | 预定文件 | 标题 | 主要目标 | type | 直接前置 | 建议投入 | 就业标签 | 实践锚点 |
|---|---|---|---|---|---|---|---|---|
| `12.01` | `12.01-虚拟机云与容器的定位边界.md` | 虚拟机、云与容器的定位边界 | 区分虚拟机、云和容器的抽象层次，并定位硬件辅助、Type-1、Type-2、VMware 与 KVM | `concept` | `03.20` | 30–60 分钟 | 建议学 | `CP-12`, `LAB-L1` |
| `12.02` | `12.02-KVM-QEMU与libvirt职责模型.md` | KVM、QEMU 与 libvirt 职责模型 | 关联 KVM 内核加速、QEMU 设备模型和 libvirt 管理层形成虚拟化职责模型 | `principle` | `05.28`, `12.01` | 60–90 分钟 | 建议学 | `CP-12`, `LAB-L2` |
| `12.03` | `12.03-libvirt-domain配置与运行生命周期.md` | libvirt domain 配置与运行生命周期 | 区分 domain 持久配置与运行状态并建立启动、停止、重启和销毁的生命周期边界 | `principle` | `12.02` | 60–90 分钟 | 建议学 | `CP-12`, `LAB-L2` |
| `12.04` | `12.04-vCPU内存超配与宿主故障边界.md` | vCPU、内存超配与宿主故障边界 | 判断 vCPU、内存超配和资源争用的影响并界定宿主故障的作用范围 | `principle` | `07.13`, `12.02` | 60–90 分钟 | 建议学 | `CP-12`, `LAB-L2` |
| `12.05` | `12.05-raw-qcow2与libvirt存储模型.md` | raw、qcow2 与 libvirt 存储模型 | 关联 raw、qcow2、backing chain、storage pool 和 volume 形成虚拟磁盘存储模型 | `principle` | `12.03` | 60–90 分钟 | 建议学 | `CP-12`, `LAB-L2` |
| `12.06` | `12.06-bridge-NAT-isolated与vNIC模型.md` | bridge、NAT、isolated 与 vNIC 模型 | 区分 bridge、NAT、isolated 虚拟网络及 vNIC 的连通和隔离职责 | `principle` | `12.03` | 60–90 分钟 | 建议学 | `CP-12`, `LAB-L2` |
| `12.07` | `12.07-虚拟机状态复用与备份语义.md` | 虚拟机状态复用与备份语义 | 区分 snapshot、clone、template、save、checkpoint 与 backup 并闭合虚拟机状态保护边界 | `principle` | `12.04`, `12.05`, `12.06` | 90–120 分钟 | 建议学 | `CP-12`, `LAB-L2` |
| `12.08` | `12.08-IaaS共享责任与控制数据面.md` | IaaS、共享责任与控制数据面 | 解释 IaaS 中云厂商与用户的共享责任并区分控制面和数据面 | `concept` | `11.20` | 30–60 分钟 | 必须学 | `CP-12`, `LAB-L1` |
| `12.09` | `12.09-region-zone资源范围与故障域.md` | region、zone、资源范围与故障域 | 关联 region、zone、资源范围和故障域以判断资源放置与故障影响 | `principle` | `12.08` | 60–90 分钟 | 必须学 | `CP-12`, `LAB-L1` |
| `12.10` | `12.10-云资源身份配额依赖与控制入口.md` | 云资源身份、配额、依赖与控制入口 | 使用资源 ID、配额、依赖关系和控制入口建立可追踪的云资源模型 | `methodology` | `12.09` | 60–90 分钟 | 必须学 | `CP-12`, `LAB-L1`, `PRJ-01-M04` |
| `12.11` | `12.11-Account-RAM-STS与最小权限.md` | Account、RAM、STS 与最小权限 | 区分 Account、RAM user、group、role、policy 和 STS 并形成最小权限身份模型 | `methodology` | `12.10` | 90–120 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.12` | `12.12-资源组标签命名资产与成本归属.md` | 资源组、标签、命名、资产与成本归属 | 通过资源组、标签、命名和资产清单建立资源责任与成本归属 | `methodology` | `12.11` | 60–90 分钟 | 必须学 | `CP-12`, `LAB-L1` |
| `12.13` | `12.13-Console-API-IaC状态漂移与变更证据.md` | Console、API、IaC 状态漂移与变更证据 | 比较 Console、API 与 IaC 的状态来源并组织漂移和变更证据 | `methodology` | `11.29`, `12.12` | 90–120 分钟 | 建议学 | `CP-12`, `LAB-L2` |
| `12.14` | `12.14-计费成本预算与释放责任.md` | 计费、成本、预算与释放责任 | 根据计费模型、成本驱动、预算告警和生命周期建立资源释放责任 | `methodology` | `12.12` | 60–90 分钟 | 必须学 | `CP-12`, `LAB-L1` |
| `12.15` | `12.15-ECS组成与通用资源选型.md` | ECS 组成与通用资源选型 | 根据 CPU、内存、存储和网络建立明确排除 GPU 的 ECS 通用选型模型 | `cloud-service` | `12.14` | 60–90 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.16` | `12.16-ECS-image来源可信与区域复用.md` | ECS image 来源、可信与区域复用 | 判断 ECS image 的来源可信性、区域范围和复用边界 | `cloud-service` | `12.15` | 60–90 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.17` | `12.17-ECS创建变配事件状态与释放.md` | ECS 创建、变配、事件、状态与释放 | 围绕创建、变配、系统事件、状态和释放组织可恢复的 ECS 生命周期变更 | `cloud-service` | `12.16` | 90–120 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.18` | `12.18-VPC-vSwitch-CIDR与zone模型.md` | VPC、vSwitch、CIDR 与 zone 模型 | 关联 VPC、vSwitch、CIDR 和 zone 建立云网络地址与隔离模型 | `cloud-service` | `12.15` | 60–90 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.19` | `12.19-vRouter-route-table与next-hop.md` | vRouter、route table 与 next hop | 区分 vRouter、系统与自定义 route table 及 next hop 的转发职责 | `cloud-service` | `12.18` | 60–90 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.20` | `12.20-ENI私网IP公网IP与EIP生命周期.md` | ENI、私网 IP、公网 IP 与 EIP 生命周期 | 区分 ENI、私网 IP、静态公网 IP 和 EIP 的资源身份及生命周期 | `cloud-service` | `12.17`, `12.19` | 60–90 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.21` | `12.21-security-group有状态规则与最小暴露.md` | security group 有状态规则与最小暴露 | 根据有状态规则、作用域和默认行为规划 security group 的最小暴露边界 | `cloud-service` | `12.20` | 60–90 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.22` | `12.22-EIP-NAT-Gateway与SLB公网职责.md` | EIP、NAT Gateway 与 SLB 公网职责 | 区分 EIP、NAT Gateway 和 SLB 在公网入站与出站链路中的职责 | `cloud-service` | `12.21` | 60–90 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.23` | `12.23-SLB产品族listener-backend与健康检查.md` | SLB 产品族、listener、backend 与健康检查 | 关联 SLB 产品族、listener、backend 和 health check 形成流量分发模型 | `cloud-service` | `12.22` | 90–120 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.24` | `12.24-cloud-disk生命周期与guest边界.md` | cloud disk 生命周期与 guest 边界 | 区分 system 与 data cloud disk 的挂载、卸载、扩容、释放及 guest OS 责任 | `cloud-service` | `12.17` | 60–90 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.25` | `12.25-snapshot-image-backup与恢复一致性.md` | snapshot、image、backup 与恢复一致性 | 区分 snapshot、image、backup、restore 和 rollback 并判断恢复一致性边界 | `cloud-service` | `12.24` | 90–120 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.26` | `12.26-OSS对象生命周期与访问控制.md` | OSS 对象生命周期与访问控制 | 关联 bucket、object、key、endpoint、storage class、versioning、lifecycle 和访问控制形成 OSS 资源模型 | `cloud-service` | `12.14` | 90–120 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.27` | `12.27-RDS托管责任访问备份与监控.md` | RDS 托管责任、访问、备份与监控 | 界定 RDS 实例、网络访问、备份监控与自建数据库之间的托管责任 | `cloud-service` | `12.21`, `12.25` | 90–120 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.28` | `12.28-CloudMonitor指标事件与基础告警.md` | CloudMonitor 指标、事件与基础告警 | 使用资源指标、系统事件和基础告警界定 CloudMonitor 与业务可用性的观测边界 | `cloud-service` | `12.23`, `12.27` | 90–120 分钟 | 必须学 | `CP-12`, `LAB-L2` |
| `12.29` | `12.29-云架构依赖故障域与单点.md` | 云架构依赖、故障域与单点 | 关联 ECS、VPC、security group、cloud disk 及可选 SLB、OSS、RDS 判断架构依赖、故障域和单点 | `methodology` | `12.26`, `12.28` | 90–120 分钟 | 必须学 | `CP-12`, `LAB-L3` |
| `12.30` | `12.30-阿里云资源治理就业证据闭环.md` | 阿里云资源治理就业证据闭环 | 汇合资源计划、变更回滚、关联清理和账单复核形成阿里云就业证据闭环 | `methodology` | `12.29` | 90–120 分钟 | 必须学 | `CP-12`, `LAB-L3` |
| `12.31` | `12.31-虚拟化-IaC与云治理完整证据闭环.md` | 虚拟化、IaC 与云治理完整证据闭环 | 汇合虚拟化、IaC 漂移和阿里云资源治理形成完整证据闭环 | `methodology` | `12.07`, `12.13`, `12.30` | 90–120 分钟 | 建议学 | `CP-12`, `LAB-L3` |

## 导航

- 上游：[知识库总览](../README.md)
- 前一阶段：[11 自动化与协作](../11-自动化与协作/README.md)
- 后续阶段：[13 Docker 容器](../13-Docker容器/README.md)
- 相关内容：[项目实战](../../项目实战/README.md)

## 边界

当前仅建立阶段骨架，不含正式正文、教学解释、操作步骤、面试答案或故障案例。
