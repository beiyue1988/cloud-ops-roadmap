# 18 AI Infra

- **阶段编号：** 18
- **阶段名称：** AI Infra

## 阶段目标

建立部署并观测基础大模型推理服务的入门能力。

## 主要主题

- GPU
- 驱动
- CUDA
- 显存
- 互联
- 容器工具包
- PyTorch
- vLLM
- Kubernetes GPU

## 前置阶段

- [01 计算机与服务器基础](../01-计算机与服务器基础/README.md)
- [13 Docker 容器](../13-Docker容器/README.md)
- [14 Kubernetes](../14-Kubernetes/README.md)
- [17 监控与可观测性](../17-监控与可观测性/README.md)

## 阶段产出

部署并观测基础推理服务。

## 章节清单

| 章节 ID | 预定文件 | 标题 | 主要目标 | type | 直接前置 | 建议投入 | 就业标签 | 实践锚点 |
|---|---|---|---|---|---|---|---|---|
| `18.01` | `18.01-AI-Infra责任推理范围与相邻领域边界.md` | AI Infra 责任、推理范围与相邻领域边界 | 界定 AI Infra 的推理基础设施责任以及与训练、AIOps 和 MLOps 的边界 | `concept` | `17.38` | 30–60 分钟 | 就业后补学 | `CP-18` |
| `18.02` | `18.02-GPU计算架构执行单元Tensor-Core与精度边界.md` | GPU 计算架构、执行单元、Tensor Core 与精度边界 | 解释 GPU 执行单元、Tensor Core 和精度能力对推理负载的约束 | `hardware` | `18.01` | 60–90 分钟 | 就业后补学 | `CP-18` |
| `18.03` | `18.03-register-cache-shared-global-memory与显存带宽.md` | register、cache、shared/global memory 与显存带宽 | 区分 GPU 存储层次并判断 HBM 或 VRAM 的容量与带宽边界 | `hardware` | `18.02` | 90–120 分钟 | 就业后补学 | `CP-18` |
| `18.04` | `18.04-PCIe-NVLink-NUMA多GPU拓扑与故障域.md` | PCIe、NVLink、NUMA、多 GPU 拓扑与故障域 | 关联 PCIe、NVLink、NUMA 和多 GPU 互联来判断拓扑与故障域 | `hardware` | `18.03` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L4` |
| `18.05` | `18.05-云上GPU共享责任与动态资源选择门.md` | 云上 GPU 共享责任与动态资源选择门 | 建立优先阿里云 GPU ECS 且不锁定实例组合的动态资源选择门 | `cloud-service` | `18.04` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L4` |
| `18.06` | `18.06-NVIDIA-driver-kernel-module-device-node与宿主责任.md` | NVIDIA driver、kernel module、device node 与宿主责任 | 区分 NVIDIA 驱动、内核模块、设备节点与宿主操作系统的责任 | `hardware` | `18.05` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.07` | `18.07-nvidia-smi设备进程利用率拓扑与证据边界.md` | nvidia-smi 设备、进程、利用率、拓扑与证据边界 | 使用 nvidia-smi 的观测范围判断设备与驱动证据及其不能证明的内容 | `tool` | `18.06` | 60–90 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.08` | `18.08-CUDA-driver-runtime-toolkit-library与编译运行职责.md` | CUDA driver、runtime、toolkit、library 与编译运行职责 | 区分 CUDA driver API、runtime、toolkit 和 library 的编译与运行职责 | `principle` | `18.06` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.09` | `18.09-compute-capability-binary-minor-forward兼容边界.md` | compute capability、binary、minor/forward 兼容边界 | 根据 GPU 架构和 CUDA 兼容模型建立双方支持范围交集 | `principle` | `18.08` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.10` | `18.10-Python-wheel-native-ABI环境隔离与可复现性.md` | Python、wheel、native ABI、环境隔离与可复现性 | 界定 Python 包、native wheel、ABI 和隔离环境的兼容与复现责任 | `methodology` | `18.09` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.11` | `18.11-PyTorch-tensor-device-dtype与推理设备可用性.md` | PyTorch tensor、device、dtype 与推理设备可用性 | 区分 tensor、device、dtype、autograd 和 inference 并判断设备实际可用性 | `tool` | `18.07`, `18.10` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.12` | `18.12-模型工件来源许可证校验与remote-code边界.md` | 模型工件、来源、许可证、校验与 remote code 边界 | 界定 tokenizer、config、weights、格式、来源、许可证、校验和 remote code 的供应链责任 | `methodology` | `18.01` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.13` | `18.13-weights-KV-cache-activation-workspace与显存估算.md` | weights、KV cache、activation、workspace 与显存估算 | 按显存构成建立不依赖具体模型参数的容量估算边界 | `methodology` | `18.11`, `18.12` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L4` |
| `18.14` | `18.14-latency-TTFT-TPOT-throughput-batch与concurrency.md` | latency、TTFT、TPOT、throughput、batch 与 concurrency | 区分推理性能指标及其在批量和并发条件下的测量语义 | `methodology` | `18.13` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L4` |
| `18.15` | `18.15-NVIDIA-Container-Toolkit-runtime-hook与CDI职责.md` | NVIDIA Container Toolkit、runtime、hook 与 CDI 职责 | 区分 Container Toolkit、runtime、hook、CDI 和底层组件的职责 | `tool` | `18.09` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.16` | `18.16-容器GPU可见设备能力权限隔离与证据.md` | 容器 GPU 可见、设备能力、权限、隔离与证据 | 判断容器内 GPU visibility、device、capability、权限与隔离的证据边界 | `principle` | `18.07`, `18.15` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.17` | `18.17-base-image-CUDA-runtime宿主驱动与镜像兼容交集.md` | base image、CUDA runtime、宿主驱动与镜像兼容交集 | 根据镜像来源和各层支持范围建立容器镜像兼容交集 | `methodology` | `18.10`, `18.16` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.18` | `18.18-vLLM-engine-scheduler-worker-cache与请求生命周期.md` | vLLM engine、scheduler、worker、cache 与请求生命周期 | 关联 vLLM engine、scheduler、worker 和 cache 的职责与请求生命周期 | `platform` | `18.11`, `18.17` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.19` | `18.19-OpenAI-compatible-API协议接口与行为边界.md` | OpenAI-compatible API、协议接口与行为边界 | 界定 OpenAI-compatible API 的协议兼容、服务接口和模型行为边界 | `service` | `18.18` | 60–90 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.20` | `18.20-continuous-batching-KV-cache与并行取舍.md` | continuous batching、KV cache 与并行取舍 | 比较 continuous batching、KV cache、tensor parallel 和 pipeline parallel 的资源取舍 | `principle` | `18.13`, `18.18` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L4` |
| `18.21` | `18.21-推理服务认证网络数据租户与审计边界.md` | 推理服务认证、网络、数据、租户与审计边界 | 界定认证、网络、输入输出、模型数据、租户隔离和审计责任 | `methodology` | `18.12`, `18.19` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L4` |
| `18.22` | `18.22-model-load-startup-health-readiness与优雅退出.md` | model load、startup、health、readiness 与优雅退出 | 组织模型加载、启动、健康、就绪、优雅退出和服务恢复的生命周期 | `methodology` | `18.21` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.23` | `18.23-GPU利用率显存功耗温度ECC-Xid硬件遥测.md` | GPU 利用率、显存、功耗、温度、ECC/Xid 硬件遥测 | 组织 GPU 利用率、显存、功耗、温度、ECC 和 Xid 的硬件证据 | `methodology` | `18.07` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.24` | `18.24-queue-latency-TTFT-TPOT-token-throughput与error.md` | queue、latency、TTFT、TPOT、token throughput 与 error | 关联服务队列、延迟、吞吐和错误指标形成推理服务证据 | `methodology` | `18.14`, `18.19`, `18.23` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.25` | `18.25-overload-OOM-backpressure-admission与降级.md` | overload、OOM、backpressure、admission 与降级 | 根据过载和 OOM 证据建立背压、准入、降级和容量边界 | `methodology` | `18.20`, `18.22`, `18.24` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L4` |
| `18.26` | `18.26-Kubernetes-device-plugin与extended-resource.md` | Kubernetes device plugin 与 extended resource | 解释 device plugin 如何向 Kubernetes 报告并分配扩展设备资源 | `platform` | `18.16` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.27` | `18.27-GPU-request-limit-label-taint-affinity与topology.md` | GPU request/limit、label、taint、affinity 与 topology | 关联 GPU 资源声明和节点约束形成可解释的调度边界 | `principle` | `18.26` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L3` |
| `18.28` | `18.28-MIG-time-slicing共享隔离计量与安全边界.md` | MIG、time-slicing、共享、隔离、计量与安全边界 | 比较 MIG 与 time-slicing 的共享、隔离、计量和安全边界 | `principle` | `18.27` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L4` |
| `18.29` | `18.29-GPU-Operator-device-plugin驱动与节点生命周期选择门.md` | GPU Operator、device plugin、驱动与节点生命周期选择门 | 建立 GPU Operator、device plugin、驱动和节点生命周期的组件选择门 | `methodology` | `18.28` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L4` |
| `18.30` | `18.30-推理交付缓存发布排空升级回滚成本与释放.md` | 推理交付、缓存、发布、排空、升级、回滚、成本与释放 | 组织镜像与模型缓存、发布、节点排空、升级、回滚、恢复、成本和资源释放责任 | `methodology` | `18.25`, `18.29` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L4` |
| `18.31` | `18.31-驱动CUDA容器框架vLLM-Kubernetes分层排障.md` | 驱动、CUDA、容器、框架、vLLM、Kubernetes 分层排障 | 沿 GPU 软件与服务栈组织分层故障假设和证据 | `methodology` | `18.30` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L4` |
| `18.32` | `18.32-AI-Infra需求兼容部署观测运维恢复与完整设计.md` | AI Infra 需求、兼容、部署、观测、运维、恢复与完整设计 | 汇合全部章节形成版本门中立的 AI Infra 完整设计与证据闭环 | `methodology` | `18.31` | 90–120 分钟 | 就业后补学 | `CP-18`, `LAB-L4` |

## 导航

- 上游：[知识库总览](../README.md)
- 前一阶段：[17 监控与可观测性](../17-监控与可观测性/README.md)
- 后续阶段：[19 AIOps 与 MLOps 入门](../19-AIOps与MLOps/README.md)
- 相关内容：[项目实战](../../项目实战/README.md)

## 边界

当前仅建立阶段骨架，不含正式正文、教学解释、操作步骤、代码、面试答案或故障案例。

- AI Infra 只负责 GPU、软件兼容、容器和 Kubernetes 运行、推理服务与运维；训练算法、微调、RAG 应用以及 AIOps/MLOps 的模型、数据和流水线治理不在本阶段。
- 兼容链按 GPU 架构与 compute capability、宿主驱动、CUDA driver/runtime/toolkit、Container Toolkit 与镜像、Python 与 native wheel、PyTorch、vLLM、目标模型和服务接口逐层核验。`nvidia-smi` 的 CUDA 字段不证明本机已安装对应 CUDA Toolkit，来源核验也不等于环境验证。
- NVIDIA 驱动、CUDA、Container Toolkit、Python、PyTorch、vLLM、模型和 Kubernetes GPU 组件的精确版本与组合继续保持阶段门。vLLM `latest` 入口可能是 developer preview，不能据此锁定生产版本。
- 模型在本阶段只作为需要核验来源、许可证、完整性和资源需求的运行工件，不选择模型、参数规模、量化、上下文、精度、并行方式或显存值；缓存不是模型工件备份。
- GPU 使用云上租用资源并优先阿里云 GPU ECS；实例族、GPU、显存、地域、库存、价格、计费方式和模型组合仍是实验进入 `ready` 前的非阻塞决策门。本阶段不创建云资源，也不承诺价格。
- GPU 可见不等于框架可用，服务存活不等于推理正确。共享不等于强隔离；认证、输入输出敏感数据、模型与镜像供应链、租户边界、容量、遥测、升级回退和资源释放都必须在后续实验门取得实际证据。
