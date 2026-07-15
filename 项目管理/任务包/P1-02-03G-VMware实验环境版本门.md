# P1-02-03G VMware 实验环境版本门任务包

## 新会话启动指令

```text
请执行 cloud-ops-roadmap 的 P1-02-03G“VMware 实验环境版本门”任务。

你是新的独立版本治理执行会话，不是项目领导者、规格制定者、独立审查者、学习正文作者或最终验收者。工作目录固定为 C:\Workspace\Projects\cloud-ops-roadmap，分支固定为 main。只执行本任务，不得委派、扩大范围或与其他写任务并行。

写前完整阅读：AGENTS.md、CODEX-PRD.md、本任务包、AI-CODEX-RULES.md、版本记录/README.md、版本记录/软件版本基线.md、版本记录/更新日志.md、参考资料/来源优先级.md、项目管理/决策记录/README.md、ADR-0001 至 ADR-0005、模板/决策记录模板.md、模板/执行报告模板.md、知识库/03-实验环境/README.md、P1-02-02 执行报告。

主会话已批准的唯一决定：选择 VMware Workstation Pro 26H1 发布线作为阶段 03 本地实验环境基线；Windows 10 20H1+ 或 Windows 11 的 64 位宿主为主教学路径；Linux 宿主只作为按执行时官方发行版/内核矩阵核验的兼容路径；macOS/Fusion 不在本决定中。锁定产品、日历发布线和主宿主边界，不锁死下载 build。Rocky Linux 9.8 x86_64 客体继续沿用既有锁定线，Linux 客体工具使用发行版提供的 open-vm-tools 路径。当前只允许记录 source-verified，不得声称已安装或 environment-verified。

唯一写入白名单：
- C:\Workspace\Projects\cloud-ops-roadmap\项目管理\决策记录\ADR-0006-VMware-Workstation-Pro-26H1实验基线.md；
- C:\Workspace\Projects\cloud-ops-roadmap\项目管理\决策记录\README.md；
- C:\Workspace\Projects\cloud-ops-roadmap\版本记录\软件版本基线.md；
- C:\Workspace\Projects\cloud-ops-roadmap\版本记录\更新日志.md；
- C:\Workspace\Projects\cloud-ops-roadmap\项目管理\执行报告\P1-02-03G-执行报告.md。

禁止修改既有 ADR、PRD、许可证、学习内容、任务包、看板、校验器或项目记忆；禁止安装/下载 VMware 或 Rocky Linux，禁止写命令、配置、实验步骤，禁止关闭 Hyper-V、VBS、内存完整性或其他安全控制；不得把官方页面可访问、免费许可或兼容矩阵写成环境验证；不得选择 Fusion、VirtualBox、Hyper-V 或其他替代主线；不得自动调用 superpowers-zh；不得进行远程写。

启动门禁：main、origin 精确、工作区干净；P1-02-02 产品 e9dab91ca6605fccb951ac0599fc44c041b39126、报告 7199ecd1110bf505ea315565cda941a0956fe37b、验收 9eb3bed8b529d0b591b47f0d3d4fc5c3f41c6ac6 在当前历史；看板 P1-02-02 为 accepted、P1-02-03G 为 ready；本任务包提交可由 Git 查询且在历史；ADR-0006 和执行报告尚不存在；CPython 3.11.15 下 133/133、默认校验和 partial 均退出 0。默认 python 不符时使用 C:\Users\beiyue\AppData\Local\Temp\cloud-ops-roadmap-uv-0.11.28\python\cpython-3.11.15-windows-x86_64-none\python.exe；该路径不可用则停止，不安装运行时。

交付 ADR-0006、ADR 索引、软件版本基线更新、追加式更新日志和独立执行报告。第一提交只含前四个治理文件，信息为 docs: lock VMware Workstation Pro 26H1 baseline；第二提交只含执行报告，信息为 docs: report P1-02-03G VMware gate。禁止 amend/rebase。

必须验证：Python 3.11.15、133/133、默认校验、--outline-gate partial、git diff --check、ADR 结构、锁定/阶段门计数、相对链接、两个提交范围和九类正式内容目录非 README Markdown 0；全部退出 0。来源冲突、产品当前性不成立、许可或宿主支持无法由一手资料确认、需要改变已批准决定、需要白名单外写入或验证无法在范围内修复时立即停止。

完成回复列出两个完整提交、五个文件、来源核验、ADR 选项与状态、基线计数变化、证据状态、自动/人工验证、异常、风险、未决和远程操作；只能建议 submitted、rework 或 blocked，不得宣布 accepted，也不得启动 P1-02-03。
```

## 门禁 1：任务信息

- **编号/名称：** P1-02-03G / VMware 实验环境版本门
- **所属阶段：** Phase 1，P1-02-03 前置治理门
- **状态/方式：** `ready`，串行
- **制定与批准者：** Phase 1 主会话

## 门禁 2：目标与价值

- **唯一目标：** 关闭阶段 03 的 VMware 产品、版本和宿主兼容性阶段门。
- **学习者价值：** 后续清单与实验使用同一可追溯桌面虚拟化线，同时区分官方来源支持和真实环境验证。

## 门禁 3：批准决定与边界

### 必须记录

1. 选择 VMware Workstation Pro 26H1，不选择浮动 latest、25H2 或 17.x 作为主线。
2. 锁定粒度为产品、26H1 日历发布线和 Windows x86-64 主宿主边界；具体 build 在首个安装实验前重新核验并记录。
3. 官方支持边界：Workstation Pro 26H1 为 64 位应用；Windows 10 20H1+、Windows 11 为支持宿主；Linux 宿主必须按官方发行版/内核表逐次核验。
4. Rocky Linux 9.8 x86_64 继续作为主客体；Rocky Linux 8+ 的工具路径为 `open-vm-tools`，但当前不证明 9.8 已在本项目安装成功。
5. 26H1 与 25H2 均对应虚拟硬件版本 22；不因可升级就强制升级已有虚拟机兼容级别。
6. Workstation/Fusion 对个人、教育和商业用途免费，但新免费用户主要依赖文档、知识库和社区资源；执行时仍需接受适用 EULA。
7. Hyper-V/VBS/内存完整性与 Workstation 的组合只登记为首个实验前验证点，不授权关闭安全控制。

### ADR 真实选项

- **选项 1（采用）：** Workstation Pro 26H1 当前发布线；当前、宿主矩阵明确、Windows 架构已转为 64 位。
- **选项 2：** Workstation Pro 25H2 上一发布线；仍支持 Windows 10/11 且与 26H1 同为虚拟硬件版本 22，但不是执行日当前线。
- 不得把“什么都不选”或未核验替代工具当作唯一备选。

### 非范围

- 不安装、下载、运行、截图或配置任何软件；不创建正式学习 Markdown。
- 不决定 VM 资源规格、实验拓扑、IP、终端工具、云实例或计费组合。
- 不修改 Rocky Linux、Kubernetes、GPU、VitePress、RuoYi 或其他既有基线。
- 不为 macOS 选择 Fusion，也不改变 PRD 的 VMware 方向。

## 门禁 4：唯一写入白名单

```text
项目管理/决策记录/ADR-0006-VMware-Workstation-Pro-26H1实验基线.md
项目管理/决策记录/README.md
版本记录/软件版本基线.md
版本记录/更新日志.md
项目管理/执行报告/P1-02-03G-执行报告.md
```

第一提交只含前四项，第二提交只含执行报告。

## 门禁 5：一手来源

核验日期为实际执行日。所有来源必须记录“支持什么”和“不能证明什么”。

| 范围 | 官方入口 | 最低支持结论 |
|---|---|---|
| 26H1 GA、64 位架构、可用性 | <https://blogs.vmware.com/cloud-foundation/2026/05/14/announcing-vmware-workstation-and-fusion-26h1/> | 26H1 于 2026-05-14 GA，Windows Workstation Pro 转为 64 位，当前可下载 |
| 26H1 Release Notes | <https://techdocs.broadcom.com/us/en/vmware-cis/desktop-hypervisors/workstation-pro/26H1.html> | 当前发布线与已知问题入口；访问受限时保留限制，不以搜索摘要替代 |
| 宿主支持矩阵 | <https://knowledge.broadcom.com/external/article?legacyId=80807> | Article 315653 列出 26H1 的 Windows 10/11 与 Linux 发行版/内核支持 |
| 安装与下载边界 | <https://knowledge.broadcom.com/external/article/387947/installing-vmware-workstation-pro.html> | 下载需 Broadcom Support Portal，安装前需核对发布说明、处理器与宿主要求 |
| 虚拟硬件版本 | <https://knowledge.broadcom.com/external/article?legacyId=1003746> | Article 315655：26H1/25H2 对应 vHW 22，升级存在兼容影响 |
| Linux 客体工具 | <https://knowledge.broadcom.com/external/article/313371/vmware-tools-compatibility-with-guest-op.html> | Rocky Linux 8+ 使用 `open-vm-tools`；平台、工具和客体支持仍需分别核对 |
| 许可与支持模式 | <https://blogs.vmware.com/cloud-foundation/2024/11/11/vmware-fusion-and-workstation-are-now-free-for-all-users/> | 个人、教育和商业用途免费；新免费用户支持以文档/知识库/社区为主 |
| Rocky Linux 9.8 | <https://rockylinux.org/news/rocky-linux-9-8-ga-release>；<https://wiki.rockylinux.org/rocky/version/> | 9.8 已 GA 且处于 Rocky 9 支持线；不证明本项目 VMware 安装成功 |

搜索摘要、聚合站、论坛和培训博客不得作为关键结论的唯一证据。TechDocs 403 或登录门只作为可访问性限制，不自动阻塞其他一手证据已闭合的结论。

## 门禁 6：交付要求

1. ADR-0006 使用模板完整结构，状态按主会话批准决定记录为 `accepted`；至少两个真实选项，包含正负/中性后果、迁移、回退、复审触发和证据限制。
2. ADR README 只增加 ADR-0006 索引，不复制决定正文。
3. 软件版本基线把 VMware 从 `phase-gated` 移入 `locked`；锁定条目 7→8、阶段门组件组 12→11；保留其他条目和值不变。
4. VMware 行写明 26H1、Windows x86-64 主路径、source-verified、首个安装实验前 environment 验证、动态 build 和复审触发。
5. 执行日来源表追加 VMware/Rocky 直接来源，不改写旧记录；版本基线日期语义不得伪装为全表重新核验。
6. 更新日志只追加 2026-07-15 条目，完整记录旧值、新值、minor/日历发布线决定、ADR、验证状态、影响与回退。
7. 执行报告记录产品提交完整哈希，不预测自身提交哈希。

## 门禁 7：验收与验证

```powershell
python --version
python -B -m unittest discover -s '脚本资源/项目校验/tests' -p 'test_*.py' -v
python -B '脚本资源/项目校验/validate_repository.py' .
python -B '脚本资源/项目校验/validate_repository.py' . --outline-gate partial
git diff --check
git status --short
```

另须人工确认：ADR 两个真实选项；既有 ADR 未修改；locked/phase-gated/reference-only 与证据状态语义正确；基线其他值逐项未漂移；相对链接有效；九类正式内容目录非 README Markdown 为 0；两个提交范围精确；无远程写。

## 门禁 8：提交、停止与回复

| 顺序 | 范围 | 固定提交信息 |
|---:|---|---|
| 1 | ADR-0006、ADR README、软件版本基线、更新日志 | `docs: lock VMware Workstation Pro 26H1 baseline` |
| 2 | 仅 P1-02-03G 执行报告 | `docs: report P1-02-03G VMware gate` |

分支、origin、工作区、前置提交、任务状态、Python、来源、许可或宿主兼容性不符，或需要改变已批准决定/白名单外写入时立即停止。禁止 amend、rebase、reset、push、PR、发布或启动 P1-02-03。

完成回复：建议状态；两个提交；五文件；来源成功数与限制；ADR 选项；locked/phase-gated 计数；source/environment 状态；133/133、默认、partial、正式内容和 Git 证据；异常、风险、未决、远程操作。不得宣布 `accepted`。
