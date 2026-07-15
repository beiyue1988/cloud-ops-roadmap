# P1-02-03G-R VMware 版本门独立审查任务包

## 新会话启动指令

```text
请执行 cloud-ops-roadmap 的 P1-02-03G-R“VMware 版本门独立审查”任务。

你是新的独立审查会话，不是原执行者、项目领导者、规格制定者、产品修复者、学习正文作者或最终验收者。工作目录固定为 C:\Workspace\Projects\cloud-ops-roadmap，分支固定为 main。只审查固定产品提交 df6104ecbc0ed33c9b4232320b090ea56e60a4a9 与执行报告提交 c51b808e2d00a07371c2b4a2fb76b5d6e2d4042c，不得委派或扩大范围。

写前完整阅读：AGENTS.md、CODEX-PRD.md、AI-CODEX-RULES.md、本审查任务包、P1-02-03G 任务包、版本记录/README.md、软件版本基线.md、更新日志.md、决策记录 README、ADR-0001 至 ADR-0006、P1-02-03G 执行报告、来源优先级、校验器 README 和模板/执行报告模板.md。

唯一目标：独立判断固定 VMware 26H1 版本门成果是否事实准确、证据诚实、治理闭合且足以解除 P1-02-03 的 ready 前置门。

产品文件一律只读。唯一允许创建/修改：C:\Workspace\Projects\cloud-ops-roadmap\项目管理\验收记录\P1-02-03G-VMware版本门独立审查报告.md。禁止修改 ADR、基线、更新日志、执行报告、任务包、看板、PRD、学习内容、校验器或项目记忆；禁止安装/下载 VMware/Rocky，禁止关闭安全控制；不得自动调用 superpowers-zh；不得进行远程写。

启动门禁：main、origin 精确、写前工作区干净；固定产品/报告提交和本审查任务包提交在当前历史；看板 P1-02-03G 为 submitted、P1-02-03G-R 为 ready；CPython 3.11.15 下 133/133、默认与 partial 退出 0；审查报告尚不存在。任一不符立即停止。

必须重新打开官方来源，不得只引用执行报告。至少核对：26H1 GA/当前性与 Windows 64 位、宿主支持矩阵、安装/下载边界、vHW 22、Rocky 8+ open-vm-tools、免费许可/自助支持、Rocky 9.8 GA/支持状态。TechDocs Release Notes 403 或登录门须记录实际限制；不得用搜索摘要补写无法看到的 Release Notes 内容。

必须审查：两个固定提交范围；ADR 两个真实选项和 accepted 授权来源；8/11/1 计数；VMware 从 phase-gated/not-yet-verified 到 locked/source-verified 的语义；动态 build 与首个安装实验环境门；Windows x86-64、Linux 逐次核验、macOS/Fusion 非范围；Rocky 工具证据不得外推为平台实装；免费许可不得外推为企业支持；vHW 22 不得外推为必须升级；禁止降低安全控制；2026-07-15 局部核验不得冒充全表复核；非目标基线不得漂移；正式正文仍为 0。

发现问题按 Critical / Important / Minor 分级，逐项给出文件、证据、影响与建议；没有问题也必须列出已验证的负向边界。只可建议 accepted、rework 或 blocked，最终裁决归主会话。

审查报告提交只含唯一报告文件，提交信息固定为 docs: review P1-02-03G VMware gate。禁止 amend/rebase/reset/push/PR。完成回复提供报告提交完整哈希、问题分级、来源核验、自动/人工证据、风险、未决和建议状态；不得启动 P1-02-03。
```

## 门禁 1：固定审查对象

| 对象 | 固定提交 | 预期范围 |
|---|---|---|
| P1-02-03G 产品 | `df6104ecbc0ed33c9b4232320b090ea56e60a4a9` | ADR-0006、ADR README、软件版本基线、更新日志，共 4 文件 |
| P1-02-03G 报告 | `c51b808e2d00a07371c2b4a2fb76b5d6e2d4042c` | 仅 P1-02-03G 执行报告 |
| 产品父对象 | `f0a145470c007dd557901be07dac182fe2d255a9` | 用于核对非目标差异 |

禁止审查浮动工作区代替固定提交；报告中同时记录固定哈希和当前 HEAD。

## 门禁 2：唯一写入白名单

```text
项目管理/验收记录/P1-02-03G-VMware版本门独立审查报告.md
```

产品缺陷只能在报告中提出，不得顺手修复。

## 门禁 3：审查问题

### A. 提交与治理

1. 产品/报告提交是否各自精确落在 4/1 文件边界？
2. ADR-0006 的 `accepted` 是否明确来自主会话已批准决定，而非执行会话自批？
3. 26H1 与 25H2 是否为两个真实选项，选择理由是否依赖一手证据？
4. `locked=8`、`phase-gated=11`、`reference-only=1` 是否在对应数据区段成立？
5. 2026-07-15 是否仅标记局部更新，旧来源日期和非目标值是否保持？

### B. 外部事实

1. 2026-07-15 是否已有 26H1 GA，且未发现更晚已 GA 的 Workstation 发布线？
2. 官方是否支持 26H1 的 Windows 10 20H1+/Windows 11 64 位宿主，并对 Linux 给出发行版/内核矩阵？
3. 26H1 与 25H2 是否同为虚拟硬件版本 22？
4. Broadcom 是否仅支持“Rocky Linux 8+ 使用发行版 open-vm-tools”这一工具结论，而非证明 Rocky 9.8 已实装？
5. 免费许可、下载门户和免费用户支持边界是否表达准确？
6. Rocky Linux 9.8 GA/支持状态是否仍成立？

### C. 证据与安全边界

1. 具体 build、处理器、宿主安全功能组合和客体实装是否仍留在 `environment-verified` 门？
2. 是否存在把网页可访问、兼容矩阵、免费许可或仓库校验器外推成环境成功的文字？
3. 是否有明示或暗示关闭 Hyper-V、VBS、内存完整性等安全控制？
4. vHW 22 是否被误写为强制升级？
5. TechDocs 403 是否被诚实披露且未由二手摘要填补？

## 门禁 4：官方来源

- <https://blogs.vmware.com/cloud-foundation/2026/05/14/announcing-vmware-workstation-and-fusion-26h1/>
- <https://techdocs.broadcom.com/us/en/vmware-cis/desktop-hypervisors/workstation-pro/26H1.html>
- <https://knowledge.broadcom.com/external/article?legacyId=80807>
- <https://knowledge.broadcom.com/external/article/387947/installing-vmware-workstation-pro.html>
- <https://knowledge.broadcom.com/external/article?legacyId=1003746>
- <https://knowledge.broadcom.com/external/article/313371/vmware-tools-compatibility-with-guest-op.html>
- <https://knowledge.broadcom.com/external/article/368667/download-and-license-vmware-desktop-hype.html>
- <https://www.vmware.com/docs/desktop-hypervisor-faqs>
- <https://blogs.vmware.com/cloud-foundation/2024/11/11/vmware-fusion-and-workstation-are-now-free-for-all-users/>
- <https://rockylinux.org/news/rocky-linux-9-8-ga-release>
- <https://wiki.rockylinux.org/rocky/version/>

搜索摘要只可发现入口，不可作为关键事实唯一证据。

## 门禁 5：验证与报告

至少实际运行：

```powershell
python --version
python -B -m unittest discover -s '脚本资源/项目校验/tests' -p 'test_*.py' -v
python -B '脚本资源/项目校验/validate_repository.py' .
python -B '脚本资源/项目校验/validate_repository.py' . --outline-gate partial
git show --check df6104ecbc0ed33c9b4232320b090ea56e60a4a9
git show --check c51b808e2d00a07371c2b4a2fb76b5d6e2d4042c
git diff --check f0a145470c007dd557901be07dac182fe2d255a9..c51b808e2d00a07371c2b4a2fb76b5d6e2d4042c
git status --short
```

报告必须包含：角色/独立性、固定对象、来源逐项结果、A/B/C 审查矩阵、问题分级、8/11/1 与内容计数、命令/退出码、证据限制、风险、未决、远程操作和建议状态。

## 门禁 6：停止与提交

固定提交缺失或不在历史、工作区非干净、来源产生无法消解冲突、需写产品文件或验证失败根因超出报告范围时停止。仅提交审查报告：

```text
docs: review P1-02-03G VMware gate
```

不得宣布最终验收，不得更新看板，不得启动 P1-02-03，不得进行任何远程写。
