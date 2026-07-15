# P1-02-03G VMware 版本门独立审查报告

## 1. 角色、对象与建议

- 审查任务：P1-02-03G-R VMware 版本门独立审查
- 审查日期：2026-07-15
- 审查角色：未参与 P1-02-03G 产品或执行报告生产的独立审查会话
- 工作目录与分支：`C:\Workspace\Projects\cloud-ops-roadmap`，`main`
- 当前 HEAD：`313a8c095c04d55c7cf68378134e7f42dded22fb`
- 固定产品提交：`df6104ecbc0ed33c9b4232320b090ea56e60a4a9`
- 固定执行报告提交：`c51b808e2d00a07371c2b4a2fb76b5d6e2d4042c`
- 产品父对象：`f0a145470c007dd557901be07dac182fe2d255a9`
- 建议状态：`accepted`

本建议只表示固定版本门成果在来源、治理、提交范围和证据边界上达到审查要求，不是主会话的最终验收裁决，也不表示 VMware、Rocky Linux 或具体宿主组合已经取得环境验证。本审查未启动 P1-02-03。

## 2. 启动门禁与固定范围

| 门禁 | 独立证据 | 结果 |
|---|---|---|
| 分支与远程 | `main`；`origin=https://github.com/beiyue1988/cloud-ops-roadmap.git` | 通过 |
| 写前工作区 | `git status --short` 无输出；仅出现用户级 Git ignore 权限警告 | 通过 |
| 固定对象 | 产品、报告、父对象均存在且是当前 HEAD 的祖先 | 通过 |
| 审查任务包 | Git 查询得到提交 `313a8c095c04d55c7cf68378134e7f42dded22fb`，在当前历史 | 通过 |
| 看板状态 | P1-02-03G 为 `submitted`；P1-02-03G-R 为 `ready` | 通过 |
| 审查报告初始状态 | 写前不存在 | 通过 |
| Python | 隔离解释器为 CPython 3.11.15 | 通过 |
| 仓库机械门禁 | 133/133；默认与 partial 均退出 0 | 通过 |

### 2.1 提交范围

| 对象 | 提交信息 | 实际文件范围 | 结论 |
|---|---|---|---|
| 产品提交 | `docs: lock VMware Workstation Pro 26H1 baseline` | ADR-0006、ADR 索引、软件版本基线、更新日志，共 4 个文件 | 与任务包一致 |
| 报告提交 | `docs: report P1-02-03G VMware gate` | 仅 `项目管理/执行报告/P1-02-03G-执行报告.md` | 与任务包一致 |

`git show --check` 对两个固定提交均退出 0；`git diff --check f0a145470c007dd557901be07dac182fe2d255a9..c51b808e2d00a07371c2b4a2fb76b5d6e2d4042c` 退出 0。产品提交未修改 ADR-0001 至 ADR-0005，未触及学习内容、校验器、PRD、任务包、看板或项目记忆。

## 3. 官方来源独立核验

所有动态事实均于 2026-07-15 重新核验。搜索只用于发现官方入口；下表结论来自 VMware/Broadcom 或 Rocky Linux 的直接页面。未使用搜索摘要补写不可读取的 Release Notes 内容。

| 官方入口 | 独立核验结果 | 不能证明的内容 |
|---|---|---|
| [Workstation/Fusion 26H1 公告](https://blogs.vmware.com/cloud-foundation/2026/05/14/announcing-vmware-workstation-and-fusion-26h1/) | 明确宣布 26H1 于 2026-05-14 GA；Windows Workstation Pro 转为 64 位应用；当日可经 Broadcom Support Portal 获取；个人、教育和商业用途免费 | 不证明具体 build、账户、下载、安装或目标宿主成功 |
| [Workstation Pro 26H1 TechDocs](https://techdocs.broadcom.com/us/en/vmware-cis/desktop-hypervisors/workstation-pro/26H1.html) | 本审查的只读 GET 返回 HTTP 200、正文长度 57751；固定产品准确记录原执行时自动访问返回 403，且没有据此补写正文内容 | 当前可达不能追溯否定原执行时 403，也不证明 Release Notes 中的环境行为已验证 |
| [宿主支持矩阵 Article 315653](https://knowledge.broadcom.com/external/article?legacyId=80807) | Workstation 12+ 只支持 64 位宿主；26H1 列出 Windows 10 20H1+、Windows 11；Linux 以发行版和内核版本逐行列示 | 不证明任一学习者的处理器、宿主版本或安全功能组合成功 |
| [安装与下载 Article 387947](https://knowledge.broadcom.com/external/article/387947/installing-vmware-workstation-pro.html) | 下载需登录 Broadcom Support Portal；安装前应核对最新 Release Notes、处理器和宿主要求；首次启动需接受 EULA | 本审查未登录、下载或安装 |
| [虚拟硬件版本 Article 315655](https://knowledge.broadcom.com/external/article?legacyId=1003746) | Workstation Pro 26H1 与 25H2 均映射到虚拟硬件版本 22；页面说明硬件版本会影响跨产品兼容 | 不证明已有 VM 必须升级，也不证明升级后客体兼容 |
| [VMware Tools 与客体 Article 313371](https://knowledge.broadcom.com/external/article/313371/vmware-tools-compatibility-with-guest-op.html) | Linux 推荐 `open-vm-tools`；Rocky Linux 8 及以上由发行版提供该工具路径 | 不证明 Rocky Linux 9.8 已作为 Workstation 客体安装，也不证明工具已运行 |
| [下载与许可 Article 368667](https://knowledge.broadcom.com/external/article/368667/download-and-license-vmware-desktop-hype.html) | 商业、教育和个人用途免费；免费版本无需许可证密钥；下载需要门户账户、资料与条款确认 | 不证明账户合规审核通过或具体 26H1 build 可得 |
| [Desktop Hypervisor FAQ](https://www.vmware.com/docs/desktop-hypervisor-faqs) | Workstation 面向 Windows/Linux 的 64 位 Intel/AMD 主机；合同结束后不再提供直接 Broadcom 工单等企业支持能力，转用社区、知识库和在线文档 | 不替代具体版本 Release Notes、宿主矩阵或支持合同文本 |
| [2024 免费公告](https://blogs.vmware.com/cloud-foundation/2024/11/11/vmware-fusion-and-workstation-are-now-free-for-all-users/) | 产品自 2024-11-11 起对商业、教育和个人用户免费；存量合同在合同期内保留约定支持 | 免费不等于自动获得新的企业支持合同 |
| [Rocky Linux 9.8 GA](https://rockylinux.org/news/rocky-linux-9-8-ga-release) | 明确宣布 Rocky Linux 9.8 GA，并提供安装、容器和云镜像入口 | 不证明镜像已下载或在 VMware 中安装成功 |
| [Rocky Linux 版本指南](https://wiki.rockylinux.org/rocky/version/) | 详细 minor 表列出 9.8、`Supported=Yes`，预计由 2026-11 的下一 minor 取代 | 页面顶部总览仍显示 9.7，属于页面局部更新时间不一致；不证明 Workstation 客体兼容 |

官方 Desktop Hypervisor 归档在审查日的最新 Workstation/Fusion 发布文章仍为 26H1，官方宿主矩阵的最高日历发布列也是 26H1；未发现已 GA 的更晚 Workstation 发布线。该结论是执行日官方入口检索结果，不是永久声明；新发布线仍按 ADR 触发复审。

Rocky Linux Wiki 的顶部总览与详细 minor 表存在局部更新时间差异，但 9.8 GA 新闻和同页详细表的 `Supported=Yes` 能够解释并闭合 9.8 已 GA、当前受支持的结论。该差异不构成将平台实装或环境兼容外推为已验证的依据。

## 4. A/B/C 审查矩阵

### A. 提交与治理

| # | 审查问题 | 独立结论 | 证据 |
|---:|---|---|---|
| A1 | 产品/报告是否精确为 4/1 文件 | 通过 | 固定提交 `git show --name-status` |
| A2 | ADR `accepted` 是否来自主会话授权 | 通过 | ADR 元数据明确为“主会话；执行会话按已批准决定记录”；任务包逐字授权该状态，没有执行会话自批语义 |
| A3 | 26H1/25H2 是否为两个真实选项 | 通过 | 官方宿主矩阵同时列出两线，虚拟硬件表均映射 vHW 22；采用理由基于当前 GA 与再验证成本 |
| A4 | `locked=8`、`phase-gated=11`、`reference-only=1` | 通过 | 按三个数据区段机械计数为 8/11/1 |
| A5 | 2026-07-15 是否仅为局部更新 | 通过 | 初始基线日期保留 2026-07-12；新增“最近局部更新”边界；非目标行的值和原核验日期未漂移 |

### B. 外部事实

| # | 审查问题 | 独立结论 | 证据 |
|---:|---|---|---|
| B1 | 26H1 GA 与当前性 | 通过 | 2026-05-14 官方 GA 公告；官方归档和矩阵未出现更晚已 GA 线 |
| B2 | Windows 64 位与 Linux 矩阵 | 通过 | Article 315653 的 64 位总边界、Windows 10 20H1+/Windows 11 行和 Linux 发行版/内核行 |
| B3 | 26H1/25H2 均为 vHW 22 | 通过 | Article 315655 |
| B4 | Rocky 8+ `open-vm-tools` 边界 | 通过 | Article 313371；ADR 明确不证明 Rocky 9.8 已实装 |
| B5 | 免费许可、门户与支持模式 | 通过 | 26H1/2024 公告、Article 368667、FAQ 和 Article 387947；没有外推为企业支持 |
| B6 | Rocky 9.8 GA 与支持状态 | 通过 | Rocky 9.8 GA 新闻、版本指南详细表；已记录 Wiki 局部更新时间差异 |

### C. 证据与安全边界

| # | 审查问题 | 独立结论 | 证据 |
|---:|---|---|---|
| C1 | build、处理器、安全组合和客体实装是否留在环境门 | 通过 | ADR、基线和更新日志均把这些项目留到阶段 03 首个安装实验 |
| C2 | 是否把页面、矩阵、许可或校验器外推为环境成功 | 通过 | 全部文件保持 `source-verified`，逐项否定下载、安装、运行与组合成功 |
| C3 | 是否降低 Hyper-V/VBS/内存完整性等安全控制 | 通过 | 只登记验证点，明确不授权关闭任何安全控制；回退条件要求不降低安全基线 |
| C4 | 是否强制升级 vHW 22 | 通过 | 明确“不因可升级就强制升级”，仅在功能/安全需求和兼容评估后升级 |
| C5 | TechDocs 受限是否诚实披露 | 通过 | 固定成果记录原执行时 403 且未补写内容；本审查记录现时 HTTP 200，不反写历史事实 |

## 5. 问题分级与负向边界

| 级别 | 数量 | 结论 |
|---|---:|---|
| Critical | 0 | 未发现会导致版本门决定失效、安全控制被降低、来源伪造或范围越权的问题 |
| Important | 0 | 未发现需要返工后才能解除 P1-02-03 ready 前置门的问题 |
| Minor | 0 | 未发现产品文件中的局部准确性、结构或措辞缺陷 |

已验证的负向边界：

- 没有锁死动态下载 build；
- 没有声称已登录门户、下载、安装、启动或测试 VMware；
- 没有把 Rocky Linux 8+ 的工具路径写成 Rocky Linux 9.8 平台实装证据；
- 没有把免费许可写成企业支持合同；
- 没有把 vHW 22 写成已有 VM 的强制升级要求；
- 没有把 Windows 主路径扩展为 macOS/Fusion，也没有把 Linux 宿主写成未经逐次核验的默认路径；
- 没有授权关闭 Hyper-V、VBS、内存完整性或其他安全控制；
- 没有把 2026-07-15 的局部核验伪装成全表复核；
- 没有修改非目标 ADR、版本值或正式学习内容。

TechDocs 可达性变化和 Rocky Wiki 局部更新时间差异属于外部证据限制，均已通过时点、支持范围和不能证明的内容进行隔离，不是当前产品缺陷。

## 6. 计数、命令与退出码

隔离解释器：

```text
C:\Users\beiyue\AppData\Local\Temp\cloud-ops-roadmap-uv-0.11.28\python\cpython-3.11.15-windows-x86_64-none\python.exe
```

| 检查 | 退出码 | 关键结果 |
|---|---:|---|
| `python --version` | 0 | Python 3.11.15 |
| `python -B -m unittest discover -s '脚本资源/项目校验/tests' -p 'test_*.py' -v` | 0 | 133/133，失败 0、错误 0 |
| `python -B '脚本资源/项目校验/validate_repository.py' .` | 0 | 报告写入后 Markdown 174、知识章节 0、本地链接 425、错误 0 |
| `python -B '脚本资源/项目校验/validate_repository.py' . --outline-gate partial` | 0 | 阶段清单 3、章节 50、依赖 63、视图引用 0、锚点 0、错误 0 |
| `git show --check df6104ecbc0ed33c9b4232320b090ea56e60a4a9` | 0 | 无空白错误 |
| `git show --check c51b808e2d00a07371c2b4a2fb76b5d6e2d4042c` | 0 | 无空白错误 |
| `git diff --check f0a145470c007dd557901be07dac182fe2d255a9..c51b808e2d00a07371c2b4a2fb76b5d6e2d4042c` | 0 | 无空白错误 |
| 基线三个数据区段机械计数 | 0 | `locked=8`、`phase-gated=11`、`reference-only=1` |
| 九类正式内容目录非 `README.md` Markdown 统计 | 0 | 0 |
| 产品提交非目标 ADR 差异 | 0 | ADR-0001 至 ADR-0005 修改数 0 |
| `git status --short` | 0 | 写前无输出；写后仅出现本报告 |

报告写入后已重新运行默认、partial 与 `git diff --check`，均退出 0；工作区唯一差异为本报告。报告提交完成后还须复核提交范围和最终工作区状态，结果在执行回复中提供，不预测报告提交自身哈希。

## 7. 风险、未决、权限与远程边界

- 证据等级：版本、发布线、宿主矩阵、工具和许可结论最高为 `source-verified`；仓库机械门禁是本地环境运行证据，但不能证明虚拟化环境。
- 风险：具体 26H1 build、处理器、Windows 宿主与 Hyper-V/VBS/内存完整性组合、Rocky Linux 9.8 客体、`open-vm-tools`、快照/克隆和回退仍未运行。它们必须在首个安装实验前取得明确环境证据。
- 未决问题：首个安装实验需记录执行时 build 和适用条款，并验证目标宿主/客体组合；若使用 Linux 宿主，需按当时发行版和内核矩阵重新核验。以上不阻塞来源级版本门。
- 动态触发：新日历发布线、许可/支持或宿主矩阵变化、下载不可用、关键安全问题，或无法在不降低安全控制的前提下复现，都必须触发复审；改变发布线必须使用替代 ADR。
- 权限：仅为复核 TechDocs 实际访问状态，对受限沙箱失败的完全相同只读 GET 合规提升一次；未下载软件、未写凭据、未关闭安全控制。
- 远程操作：未 push、未创建 Pull Request、未发布网站/制品、未修改 GitHub 设置、未创建云资源或进行其他远程写。

## 8. 建议状态与后续门禁

- 建议 P1-02-03G：`accepted`。
- 建议 P1-02-03G-R：独立审查交付完成后由主会话裁决。
- 解锁边界：本报告只支持主会话解除 P1-02-03 的 ready 前置版本门；不替代 P1-02-03 自身任务包，也不授权任何安装、实验、正文、脚本、配置、图表或安全控制变更。
- 最终责任：主会话依据固定产品、执行报告、本独立审查与新鲜复验作最终验收；本审查会话不得宣布最终 `accepted`。
