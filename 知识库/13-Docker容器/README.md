# 13 Docker 容器

- **阶段编号：** 13
- **阶段名称：** Docker 容器

## 阶段目标

建立将传统项目容器化并维护其运行环境的能力。

## 主要主题

- 镜像
- 容器
- Dockerfile
- 网络
- 存储
- Compose
- 安全
- 排障

## 前置阶段

- [09 企业基础服务](../09-企业基础服务/README.md)
- [10 数据服务](../10-数据服务/README.md)
- [11 自动化与协作](../11-自动化与协作/README.md)

## 阶段产出

将传统项目容器化。

## 章节清单

| 章节 ID | 预定文件 | 标题 | 主要目标 | type | 直接前置 | 建议投入 | 就业标签 | 实践锚点 |
|---|---|---|---|---|---|---|---|---|
| `13.01` | `13.01-容器虚拟机与传统进程的边界.md` | 容器、虚拟机与传统进程的边界 | 区分容器、虚拟机和传统进程在隔离、内核共享与交付单元上的边界 | `concept` | `11.20` | 30–60 分钟 | 必须学 | `CP-13`, `LAB-L1`, `PRJ-02-M01` |
| `13.02` | `13.02-OCI镜像运行时与分发规范边界.md` | OCI 镜像、运行时与分发规范边界 | 解释 OCI image、runtime、distribution 三类规范与 Docker 实现之间的边界 | `principle` | `13.01` | 30–60 分钟 | 建议学 | `CP-13`, `LAB-L1` |
| `13.03` | `13.03-Docker-CLI-API-daemon-containerd与runc职责.md` | Docker CLI、API、daemon、containerd 与 runc 职责 | 关联 Docker CLI、API、daemon、containerd 和 runc 的职责并界定 Kubernetes runtime 归属 | `principle` | `13.01` | 60–90 分钟 | 必须学 | `CP-13`, `LAB-L1` |
| `13.04` | `13.04-namespace-rootfs进程树与内核共享.md` | namespace、rootfs、进程树与内核共享 | 解释 namespace、rootfs、容器进程树和主机内核共享构成的隔离模型 | `principle` | `13.03` | 60–90 分钟 | 必须学 | `CP-13`, `LAB-L1` |
| `13.05` | `13.05-cgroup资源核算与隔离上限.md` | cgroup 资源核算与隔离上限 | 解释 cgroup 对 CPU、内存与 PID 的资源核算、限制和非安全隔离边界 | `principle` | `07.12`, `13.04` | 60–90 分钟 | 必须学 | `CP-13`, `LAB-L1` |
| `13.06` | `13.06-Engine来源平台daemon与升级阶段门.md` | Engine 来源、平台、daemon 与升级阶段门 | 根据支持平台、软件来源、daemon 状态和升级证据建立 Docker Engine 版本阶段门 | `service` | `13.05` | 90–120 分钟 | 必须学 | `CP-13`, `LAB-L1` |
| `13.07` | `13.07-Docker对象与生命周期.md` | Docker 对象与生命周期 | 区分 image、container、network、volume 和 registry 对象及其生命周期责任 | `concept` | `13.06` | 30–60 分钟 | 必须学 | `CP-13`, `LAB-L1` |
| `13.08` | `13.08-PID-1信号退出码与优雅停止.md` | PID 1、信号、退出码与优雅停止 | 关联 PID 1、信号传递、退出码和停止超时形成可判断的容器终止模型 | `principle` | `13.07` | 60–90 分钟 | 必须学 | `CP-13`, `LAB-L1` |
| `13.09` | `13.09-重启策略健康检查与高可用边界.md` | 重启策略、健康检查与高可用边界 | 区分 restart policy、healthcheck 和真正高可用机制的职责与失效边界 | `principle` | `13.08` | 60–90 分钟 | 必须学 | `CP-13`, `LAB-L1`, `PRJ-02-M03` |
| `13.10` | `13.10-镜像名称tag-digest与platform身份.md` | 镜像名称、tag、digest 与 platform 身份 | 关联镜像名称、tag、digest 和 platform 形成可追溯且不可变的镜像身份 | `principle` | `13.07` | 30–60 分钟 | 必须学 | `CP-13`, `LAB-L1`, `PRJ-02-M01` |
| `13.11` | `13.11-registry认证凭据与发布责任.md` | registry 认证、凭据与发布责任 | 界定 registry 登录、凭据存储、pull、push 和外部发布的权限与责任边界 | `methodology` | `13.10` | 60–90 分钟 | 建议学 | `CP-13`, `LAB-L1` |
| `13.12` | `13.12-build-context与dockerignore输入边界.md` | build context 与 .dockerignore 输入边界 | 使用 build context 和 .dockerignore 界定发送给 builder 的构建输入 | `methodology` | `13.10` | 60–90 分钟 | 必须学 | `CP-13`, `LAB-L1`, `PRJ-02-M01` |
| `13.13` | `13.13-基础镜像可信最小化与固定输入.md` | 基础镜像可信、最小化与固定输入 | 根据来源、digest、内容最小化和更新责任选择可信且可复现的基础镜像输入 | `methodology` | `13.12` | 60–90 分钟 | 必须学 | `CP-13`, `LAB-L1`, `PRJ-02-M01` |
| `13.14` | `13.14-Dockerfile核心指令层与构建结果.md` | Dockerfile 核心指令、层与构建结果 | 关联 Dockerfile 核心指令、镜像层和构建结果形成基础构建模型 | `tool` | `13.13` | 90–120 分钟 | 必须学 | `CP-13`, `LAB-L1`, `PRJ-02-M01` |
| `13.15` | `13.15-CMD-ENTRYPOINT-ARG与ENV职责.md` | CMD、ENTRYPOINT、ARG 与 ENV 职责 | 区分 CMD、ENTRYPOINT、ARG 和 ENV 在构建期与运行期的职责 | `principle` | `13.14` | 60–90 分钟 | 必须学 | `CP-13`, `LAB-L1` |
| `13.16` | `13.16-layer缓存失效与可复现构建.md` | layer、缓存失效与可复现构建 | 根据 layer 与 cache invalidation 判断构建效率并界定可复现构建证据 | `methodology` | `13.14` | 90–120 分钟 | 建议学 | `CP-13`, `LAB-L2` |
| `13.17` | `13.17-multi-stage-build与运行镜像收敛.md` | multi-stage build 与运行镜像收敛 | 使用 multi-stage build 分离构建依赖并收敛运行镜像内容 | `methodology` | `13.15` | 90–120 分钟 | 必须学 | `CP-13`, `LAB-L2`, `PRJ-02-M01` |
| `13.18` | `13.18-BuildKit-Buildx与多平台阶段门.md` | BuildKit、Buildx 与多平台阶段门 | 区分 BuildKit、Buildx、builder 和 multi-platform 构建职责并保留兼容组合阶段门 | `tool` | `13.17` | 90–120 分钟 | 建议学 | `CP-13`, `LAB-L2` |
| `13.19` | `13.19-build-secret与SSH-mount安全边界.md` | build secret 与 SSH mount 安全边界 | 使用 secret mount 与 SSH mount 传递构建秘密并排除 ARG、ENV 泄露路径 | `methodology` | `13.17` | 60–90 分钟 | 必须学 | `CP-13`, `LAB-L2` |
| `13.20` | `13.20-writable-layer存储后端与image-store差异.md` | writable layer、存储后端与 image store 差异 | 区分 writable layer、经典 storage driver 与 containerd image store 的职责和迁移风险 | `principle` | `13.07` | 90–120 分钟 | 建议学 | `CP-13`, `LAB-L2` |
| `13.21` | `13.21-volume-bind-mount与tmpfs边界.md` | volume、bind mount 与 tmpfs 边界 | 比较 volume、bind mount 和 tmpfs 的所有权、生命周期与适用范围 | `principle` | `13.07` | 60–90 分钟 | 必须学 | `CP-13`, `LAB-L2`, `PRJ-02-M02` |
| `13.22` | `13.22-持久数据备份恢复迁移与清理.md` | 持久数据备份、恢复、迁移与清理 | 围绕持久数据组织备份、恢复、迁移、清理和删除结果的证据边界 | `methodology` | `13.21` | 90–120 分钟 | 必须学 | `CP-13`, `LAB-L2`, `PRJ-02-M03` |
| `13.23` | `13.23-user-defined-bridge与DNS服务发现.md` | user-defined bridge 与 DNS 服务发现 | 解释 user-defined bridge、容器 DNS 和单机服务发现的连接模型 | `principle` | `13.07` | 60–90 分钟 | 必须学 | `CP-13`, `LAB-L2`, `PRJ-02-M02` |
| `13.24` | `13.24-port-publishing-NAT监听与防火墙边界.md` | port publishing、NAT、监听与防火墙边界 | 关联端口发布、NAT、监听地址与主机防火墙判断实际暴露面 | `principle` | `13.23` | 90–120 分钟 | 必须学 | `CP-13`, `LAB-L2`, `PRJ-02-M03` |
| `13.25` | `13.25-容器网络分层排障证据.md` | 容器网络分层排障证据 | 沿容器、bridge、主机、防火墙和上游链路组织分层网络排障证据 | `methodology` | `13.24` | 90–120 分钟 | 必须学 | `CP-13`, `LAB-L2`, `PRJ-02-M04` |
| `13.26` | `13.26-运行时环境配置secret与不可变单元.md` | 运行时环境、配置、secret 与不可变单元 | 区分运行时 env、配置、secret 和 mount 并形成不可变运行单元边界 | `methodology` | `13.19`, `13.21` | 90–120 分钟 | 必须学 | `CP-13`, `LAB-L2`, `PRJ-02-M02` |
| `13.27` | `13.27-CPU内存PID限制与OOM证据.md` | CPU、内存、PID 限制与 OOM 证据 | 根据 CPU、内存和 PID 限制及 OOM 信号形成资源容量与失败证据 | `methodology` | `13.05` | 90–120 分钟 | 必须学 | `CP-13`, `LAB-L2`, `PRJ-02-M03` |
| `13.28` | `13.28-stdout-stderr日志驱动与轮转边界.md` | stdout、stderr、日志驱动与轮转边界 | 关联 stdout、stderr、logging driver 和轮转形成单机日志责任并界定集中日志边界 | `methodology` | `13.08` | 60–90 分钟 | 必须学 | `CP-13`, `LAB-L2`, `PRJ-02-M03` |
| `13.29` | `13.29-Compose-Specification与应用模型.md` | Compose Specification 与应用模型 | 使用 project、service、network 和 volume 建立 Compose 多容器应用模型 | `principle` | `13.17`, `13.22`, `13.25` | 90–120 分钟 | 必须学 | `CP-13`, `LAB-L2`, `PRJ-02-M02` |
| `13.30` | `13.30-Compose变量配置profile与健康顺序.md` | Compose 变量、配置、profile 与健康顺序 | 关联变量、config、secret、profile、依赖和健康条件组织 Compose 启动顺序 | `methodology` | `13.09`, `13.26`, `13.27`, `13.28`, `13.29` | 90–120 分钟 | 必须学 | `CP-13`, `LAB-L2`, `PRJ-02-M02` |
| `13.31` | `13.31-Compose生命周期与传统项目容器化闭环.md` | Compose 生命周期与传统项目容器化闭环 | 汇合 Compose 重建、健康、回退和传统项目交付证据形成容器化就业核心闭环 | `methodology` | `13.30` | 90–120 分钟 | 必须学 | `CP-13`, `LAB-L3`, `PRJ-02-M03` |
| `13.32` | `13.32-daemon-socket-rootless与userns信任边界.md` | daemon socket、rootless 与 userns 信任边界 | 界定 daemon socket、docker group、远程 daemon、rootless 与 userns 的高权限信任边界 | `principle` | `13.31` | 90–120 分钟 | 建议学 | `CP-13`, `LAB-L2` |
| `13.33` | `13.33-non-root-capability-seccomp与privileged风险.md` | non-root、capability、seccomp 与 privileged 风险 | 通过 non-root、capability、seccomp 和 read-only 收敛权限并识别 privileged 风险 | `methodology` | `13.31` | 90–120 分钟 | 必须学 | `CP-13`, `LAB-L2`, `PRJ-02-M04` |
| `13.34` | `13.34-镜像来源digest更新扫描与供应链边界.md` | 镜像来源、digest、更新、扫描与供应链边界 | 根据镜像来源、digest、更新和扫描证据界定阶段 13 与完整供应链治理边界 | `methodology` | `13.11`, `13.18`, `13.33` | 90–120 分钟 | 建议学 | `CP-13`, `LAB-L2`, `PRJ-02-M04` |
| `13.35` | `13.35-Docker综合排障与完整证据闭环.md` | Docker 综合排障与完整证据闭环 | 汇合 build、daemon、process、network、storage、permission、resource 和 log 证据形成完整排障闭环 | `methodology` | `13.02`, `13.16`, `13.20`, `13.32`, `13.34` | 90–120 分钟 | 建议学 | `CP-13`, `LAB-L3`, `PRJ-02-M04` |

## 导航

- 上游：[知识库总览](../README.md)
- 前一阶段：[12 虚拟化与阿里云](../12-虚拟化与阿里云/README.md)
- 后续阶段：[14 Kubernetes](../14-Kubernetes/README.md)
- 相关内容：[项目实战](../../项目实战/README.md)

## 边界

当前仅建立阶段骨架，不含正式正文、教学解释、操作步骤、代码、面试答案或故障案例。
