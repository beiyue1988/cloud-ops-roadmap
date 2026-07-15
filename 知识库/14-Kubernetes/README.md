# 14 Kubernetes

- **阶段编号：** 14
- **阶段名称：** Kubernetes

## 阶段目标

建立使用 kubeadm 构建集群并在集群中部署和维护项目的能力。

## 主要主题

- 架构
- 对象
- 调度
- 网络
- 存储
- 配置
- 安全
- 扩缩容
- 升级
- 排障

## 前置阶段

- [02 网络基础](../02-网络基础/README.md)
- [05 Linux 系统管理](../05-Linux系统管理/README.md)
- [13 Docker 容器](../13-Docker容器/README.md)

## 阶段产出

用 kubeadm 建群并部署项目。

## 章节清单

| 章节 ID | 预定文件 | 标题 | 主要目标 | type | 直接前置 | 建议投入 | 就业标签 | 实践锚点 |
|---|---|---|---|---|---|---|---|---|
| `14.01` | `14.01-Kubernetes定位集群边界与容器分工.md` | Kubernetes 定位、集群边界与容器分工 | 区分 Kubernetes 集群编排与 Docker、Compose 单机容器交付的职责边界 | `concept` | `13.31` | 30–60 分钟 | 就业后补学 | `CP-14` |
| `14.02` | `14.02-声明式期望状态控制循环与最终一致性.md` | 声明式期望状态、控制循环与最终一致性 | 解释声明式期望状态如何通过 reconcile 控制循环逐步达到最终一致 | `principle` | `14.01` | 60–90 分钟 | 就业后补学 | `CP-14` |
| `14.03` | `14.03-control-plane-node与核心组件职责.md` | control plane、node 与核心组件职责 | 关联 API server、etcd、scheduler、controller、kubelet 和 runtime 的组件职责 | `platform` | `14.02` | 60–90 分钟 | 就业后补学 | `CP-14` |
| `14.04` | `14.04-API-object元数据期望状态与生命周期.md` | API object、元数据、期望状态与生命周期 | 区分 metadata、spec、status、resourceVersion 和对象生命周期的语义 | `principle` | `14.02` | 60–90 分钟 | 就业后补学 | `CP-14` |
| `14.05` | `14.05-kubectl上下文发现查询与变更证据.md` | kubectl 上下文、发现、查询与变更证据 | 界定 context、namespace、资源发现、查询和变更操作所能形成的证据 | `tool` | `14.04` | 60–90 分钟 | 就业后补学 | `CP-14` |
| `14.06` | `14.06-四层版本角色偏差与API弃用边界.md` | 四层版本角色、版本偏差与 API 弃用边界 | 按四层教学角色判断组件版本偏差、API 弃用和 patch 集中维护责任 | `methodology` | `14.03` | 60–90 分钟 | 就业后补学 | `CP-14` |
| `14.07` | `14.07-节点OS网络内核时间与安全前置.md` | 节点 OS、网络、内核、时间与安全前置 | 组织节点 OS、网络、内核、时间、swap、端口和安全条件的前置检查 | `methodology` | `14.05`, `14.06` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.08` | `14.08-containerd-CRI-cgroup与kubelet对齐.md` | containerd、CRI、cgroup 与 kubelet 对齐 | 解释 containerd、CRI v1、cgroup v2、systemd driver 与 kubelet 的一致性要求 | `principle` | `14.07` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.09` | `14.09-kubeadm拓扑证书镜像端口与preflight.md` | kubeadm 拓扑、证书、镜像、端口与 preflight | 界定 kubeadm 集群拓扑、证书、镜像、端口和 preflight 的验证责任 | `platform` | `14.08` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.10` | `14.10-kubeadm-init-join与节点信任.md` | kubeadm init、join 与节点信任 | 关联 init、join、bootstrap token 和 discovery 形成可追踪的节点信任链 | `tool` | `14.09` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.11` | `14.11-Calico-CNI节点Ready与连通证据.md` | Calico CNI、节点 Ready 与连通证据 | 界定 Calico CNI 安装、节点 Ready 状态和基础连通性证据的责任边界 | `platform` | `14.10` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.12` | `14.12-Namespace-label-annotation与selector.md` | Namespace、label、annotation 与 selector | 使用 Namespace、label、annotation 和 selector 组织并关联集群资源 | `concept` | `14.11` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L1` |
| `14.13` | `14.13-Pod生命周期容器组合与终止边界.md` | Pod 生命周期、容器组合与终止边界 | 解释 Pod 生命周期、init 与 sidecar 容器组合以及终止过程的边界 | `principle` | `14.12` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L1` |
| `14.14` | `14.14-startup-readiness-liveness-probe职责.md` | startup、readiness、liveness probe 职责 | 区分三类 probe 的职责及其失败对启动、流量和重启的影响 | `principle` | `14.13` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L1` |
| `14.15` | `14.15-requests-limits-QoS与资源失败.md` | requests、limits、QoS 与资源失败 | 关联 requests、limits、QoS 和 cgroup 落地判断资源分配与失败 | `principle` | `14.13` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L1` |
| `14.16` | `14.16-ReplicaSet-Deployment与副本管理.md` | ReplicaSet、Deployment 与副本管理 | 解释 ReplicaSet 和 Deployment 如何声明并维持应用副本 | `principle` | `14.13` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L1` |
| `14.17` | `14.17-Deployment-rollout-history与rollback.md` | Deployment rollout、history 与 rollback | 组织 Deployment rollout、pause、resume、history 和 rollback 的发布语义 | `methodology` | `14.16` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L1` |
| `14.18` | `14.18-StatefulSet身份顺序与持久状态.md` | StatefulSet 身份、顺序与持久状态 | 解释 StatefulSet 的稳定身份、顺序语义和持久状态责任边界 | `principle` | `14.16` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L1` |
| `14.19` | `14.19-DaemonSet与节点级工作负载.md` | DaemonSet 与节点级工作负载 | 说明 DaemonSet 如何按节点条件维持节点级工作负载 | `principle` | `14.16` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L1` |
| `14.20` | `14.20-Job-CronJob并发重试与历史清理.md` | Job、CronJob、并发、重试与历史清理 | 区分 Job 与 CronJob 的完成、并发、重试和历史清理语义 | `principle` | `14.13` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L1` |
| `14.21` | `14.21-ConfigMap创建注入更新与不可变边界.md` | ConfigMap 创建、注入、更新与不可变边界 | 解释 ConfigMap 的创建、注入、更新传播和不可变边界 | `principle` | `14.12` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L1` |
| `14.22` | `14.22-Secret编码存储分发与外部密钥边界.md` | Secret 编码、存储、分发与外部密钥边界 | 界定 Secret 的编码、存储、分发、挂载与外部密钥管理责任 | `principle` | `14.21` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L1` |
| `14.23` | `14.23-scheduler过滤评分与基础调度证据.md` | scheduler 过滤、评分与基础调度证据 | 解释 scheduler 过滤与评分并使用 nodeSelector 建立基础调度证据 | `principle` | `14.13` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.24` | `14.24-affinity-taint与topology-spread.md` | affinity、taint 与 topology spread | 比较 affinity、anti-affinity、taint、toleration 和 topology spread 的调度约束 | `principle` | `14.23` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.25` | `14.25-priority-preemption-eviction与PDB.md` | priority、preemption、eviction 与 PDB | 关联优先级、抢占、驱逐和 PDB 判断维护期间的可用性边界 | `methodology` | `14.17`, `14.24` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.26` | `14.26-Service-EndpointSlice与kube-proxy.md` | Service、EndpointSlice 与 kube-proxy | 关联 Service、EndpointSlice 和 kube-proxy 形成服务抽象与后端映射 | `principle` | `14.16` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.27` | `14.27-集群DNS服务发现与解析证据.md` | 集群 DNS、服务发现与解析证据 | 解释服务发现、搜索域和名称解析并建立 DNS 故障证据边界 | `principle` | `14.26` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.28` | `14.28-Ingress-IngressClass-TLS与Gateway边界.md` | Ingress、IngressClass、TLS 与 Gateway 边界 | 区分 Ingress、IngressClass、controller、TLS 终止和 Gateway API 的职责 | `platform` | `14.27` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.29` | `14.29-Pod-CNI-Service与跨节点数据路径.md` | Pod、CNI、Service 与跨节点数据路径 | 沿 Pod、CNI、Service 和节点网络解释跨节点通信的数据路径 | `principle` | `14.26` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.30` | `14.30-NetworkPolicy-Calico与默认拒绝验证.md` | NetworkPolicy、Calico 与默认拒绝验证 | 使用 NetworkPolicy 与 Calico 策略界定默认拒绝和连通性验证边界 | `methodology` | `14.29` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.31` | `14.31-emptyDir与配置投射临时卷.md` | emptyDir 与配置投射临时卷 | 区分 emptyDir、configMap、secret 和 projected 等临时卷的生命周期 | `principle` | `14.13` | 60–90 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.32` | `14.32-PV-PVC-StorageClass与绑定生命周期.md` | PV、PVC、StorageClass 与绑定生命周期 | 关联 PV、PVC、StorageClass、访问模式和绑定生命周期 | `principle` | `14.31` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.33` | `14.33-CSI动态供应扩容快照与数据保护.md` | CSI、动态供应、扩容、快照与数据保护 | 界定 CSI、动态供应、扩容、快照和数据保护的职责与验证边界 | `platform` | `14.32` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.34` | `14.34-ServiceAccount-RBAC与最小权限.md` | ServiceAccount、RBAC 与最小权限 | 使用 ServiceAccount、role 和 binding 建立可审计的最小权限模型 | `principle` | `14.12` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.35` | `14.35-securityContext-PSS与Admission边界.md` | securityContext、PSS 与 Admission 边界 | 关联 securityContext、Pod Security Standards、Admission 和其他准入控制边界 | `methodology` | `14.13`, `14.34` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.36` | `14.36-HPA指标目标稳定窗口与容量边界.md` | HPA 指标、目标、稳定窗口与容量边界 | 解释 HPA 指标、目标和稳定窗口并界定自动扩缩与容量责任 | `principle` | `14.15`, `14.23` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.37` | `14.37-事件日志指标与audit证据入口.md` | 事件、日志、指标与 audit 证据入口 | 组织 event、容器与节点日志、控制平面日志、metrics 和 audit 证据入口 | `methodology` | `14.05` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L2` |
| `14.38` | `14.38-工作负载probe调度与资源分层排障.md` | 工作负载、probe、调度与资源分层排障 | 沿对象状态、probe、控制器、调度和资源信号组织工作负载排障 | `methodology` | `14.14`, `14.15`, `14.17`, `14.20`, `14.24`, `14.37` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L3` |
| `14.39` | `14.39-Service-DNS网络与存储端到端排障.md` | Service、DNS、网络与存储端到端排障 | 沿 Service、DNS、CNI、策略和存储链路组织端到端故障证据 | `methodology` | `14.28`, `14.30`, `14.33`, `14.37` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L3` |
| `14.40` | `14.40-node-kubelet-runtime与control-plane排障.md` | node、kubelet、runtime 与 control plane 排障 | 沿 node、kubelet、runtime 和 control plane 分层定位集群基础故障 | `methodology` | `14.10`, `14.37` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L3` |
| `14.41` | `14.41-cordon-drain-PDB节点维护与证书责任.md` | cordon、drain、PDB、节点维护与证书责任 | 组织 cordon、drain、PDB、节点维护和证书责任形成可回退的维护边界 | `methodology` | `14.25`, `14.40` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L3` |
| `14.42` | `14.42-etcd备份恢复隔离验证与灾难边界.md` | etcd 备份、恢复、隔离验证与灾难边界 | 界定 etcd 备份、恢复、隔离验证和控制平面灾难恢复责任 | `methodology` | `14.40` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L3` |
| `14.43` | `14.43-kubeadm升级版本偏差与API迁移.md` | kubeadm 升级、版本偏差与 API 迁移 | 规划 patch 与逐 minor 升级、版本偏差、API 迁移和历史升级路径 | `methodology` | `14.41`, `14.42` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L3` |
| `14.44` | `14.44-Kubernetes项目运行与运维完整闭环.md` | Kubernetes 项目运行与运维完整闭环 | 汇合应用部署、发布回退、配置、存储、安全、观测和集群运维形成完整闭环 | `methodology` | `14.18`, `14.19`, `14.22`, `14.35`, `14.36`, `14.38`, `14.39`, `14.43` | 90–120 分钟 | 就业后补学 | `CP-14`, `LAB-L3` |

## 导航

- 上游：[知识库总览](../README.md)
- 前一阶段：[13 Docker 容器](../13-Docker容器/README.md)
- 后续阶段：[15 DevOps 与 CI/CD](../15-DevOps与CI-CD/README.md)
- 相关内容：[项目实战](../../项目实战/README.md)

## 边界

当前仅建立文件级章节清单，不含正式正文、教学解释、操作步骤、命令、manifest、YAML、配置、代码、实验、项目实现、面试答案或故障案例。

- 概念尽量保持版本中立；Kubernetes 1.36.x 是唯一主实验环境，1.35.x 只作企业兼容参考，1.31.14 只作 EOL 历史升级参考。patch 从软件版本基线集中读取，不在章节标题分散复制；历史升级必须逐 minor 规划，不从 1.31 直接跳到 1.36。
- 主组合保持 kubeadm、containerd 2.3 LTS、CRI v1、cgroup v2、systemd driver 与 Calico 3.32。官方兼容范围只达到来源核验，不证明集群已经安装或运行。
- kubelet 与 runtime 的 cgroup driver 必须一致；CRI 插件、端口、内核、网络、swap、代理和 Calico 数据面条件均留到实验门核验。CNI 就绪前节点 NotReady 是需要解释的状态，不是绕过安全控制的理由；防火墙与所需端口必须显式核验，不得静默关闭。
- 不教授已移除的 PodSecurityPolicy；安全章节以 Pod Security Standards、Pod Security Admission 和其他 admission 边界为准。
- 阶段 13 保有单机容器构建与 Compose，阶段 14 保有 Kubernetes 编排与集群生命周期，阶段 15 保有完整 CI/CD 与供应链，阶段 16/17 保有集中日志与完整观测平台。托管 Kubernetes、多集群、Service Mesh、Operator/CRD 开发、认证考试题库和 GPU 调度不在本阶段。
