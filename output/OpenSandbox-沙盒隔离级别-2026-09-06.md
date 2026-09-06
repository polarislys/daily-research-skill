---
形态: 产品剖析
主题: OpenSandbox
日期: 2026-09-06
---

# OpenSandbox 的分级隔离：沙盒管「在哪跑」，harness 管「怎么跑」

这篇只抠 OpenSandbox 的**隔离层级**怎么选，以及它和 agent harness、MCP 各管哪一段链路。值得看，是因为 2026 年的 agent 栈常把「接了 MCP」误写成「已经沙盒化」——协议是能力通道，不是安全边界；不信任代码跑在哪、隔离到哪一级，才是 sandbox 要回答的问题。

## 痛点：不信任代码需要分级，而不是一刀切

Coding agent 要跑模型生成的 shell、Python、浏览器自动化；GUI agent 还要 VNC、Playwright、code-server。全上 Firecracker microVM，冷启动与调度成本在评测、RL 批量任务里会爆；全用 Docker 默认 runc，多租户或 prompt injection 场景又心里发虚——尤其当同一个 server 上要混跑「用户 A 的 Claude Code」和「用户 B 的数据清洗脚本」时，进程级隔离的边界感很弱。

更麻烦的是 **harness 与 sandbox 职责纠缠**：Claude Code、Codex CLI、LangGraph、Google ADK 已经管 tool loop、上下文、审批——若每个 SDK 各自嵌一套 `docker run` 与网络策略，换 runtime、换云、换隔离级别，集成代码就要重写。MCP 让宿主「看见」沙盒工具，但 MCP 规范本身不定义 cgroup、不定义 VM——把 MCP 当 sandbox 是类别错误。

OpenSandbox（阿里开源，Apache 2.0）的定位是**通用沙盒平台**：统一 lifecycle API、多语言 SDK（Python/Java/TS/Go/C#）、Docker 与 Kubernetes runtime，覆盖 Coding Agent、GUI Agent、Agent Evaluation、AI Code Execution、RL Training。它回答「工作负载跑在哪个隔离级别、谁管生命周期」，不回答「模型下一步调用哪个 tool」——那是 harness 的事。

平台内部还可拆成几块各司其职：`opensandbox-server` 管 create/kill/timeout；`execd` 在实例内执行命令与文件 IO；`ingress`/`egress` 组件管网络；`Credential Vault` 管出站凭证注入。SDK 与 MCP 都对着同一套 OpenAPI——避免「CLI 能 gVisor、SDK 只能 runc」的分裂。

## 机制：隔离级别与平台组件

**分级隔离（secure runtime）。** 管理员在 `~/.sandbox.toml` 的 `[secure_runtime]` **服务器级**配置一次，该 server 上所有 sandbox 透明继承；SDK 与 API 调用方**零代码改动**。Server 启动时会校验 runtime 是否可用——配了 runsc 但主机没装 gVisor，直接拒绝启动，避免「以为上了硬隔离其实还在 runc」的 silent fallback。

选型时要同时看 **启动延迟、内存 footprint、syscall 兼容**。gVisor 拦截 syscall，少数深度依赖 host kernel 特性的工具可能行为异常；Kata/Firecracker 兼容性更好但调度更重。OpenSandbox 文档把 runc 标为 trusted workload 与 local dev——不是「不安全就不能用」，而是**威胁模型**不同：你信任的是代码还是信任的是用户？Coding agent 默认应假设代码不可信。

| 级别 | 机制 | 典型开销 | 适用 |
|------|------|----------|------|
| runc（默认） | 进程 cgroup | ~0ms | 本地开发、可信代码 |
| gVisor | 用户态内核拦截 syscall | +10–50ms，~50MB | 不可信代码、要密度 |
| Kata/QEMU | 完整 VM | ~500ms | 最强兼容与隔离 |
| Kata/Firecracker | microVM | ~125ms，~5MB | 高密度不可信 workload |

设计意图很明确：OpenSandbox 面向 **AI 生成的不信任代码**——容器逃逸防护、内核级隔离、多租户安全、合规场景。选型不是「越硬越好」，而是按任务时长、租户模型、启动频率在延迟与隔离之间取点。

**与 harness 的关系：正交分层。** Harness 决定 agent loop、模型路由、tool schema、人审卡点；OpenSandbox 保证 `Sandbox.create` 之后的 `commands.run`、`files.write`、Code Interpreter 在指定边界内执行。一次典型 Coding Agent 集成是：harness 在宿主机或自有 orchestrator 里跑 model loop，需要执行不可信代码时通过 SDK 或 MCP 调 OpenSandbox 创建实例；harness 崩溃不会自动销毁 sandbox——lifecycle 由 OpenSandbox server 的 timeout/kill 语义管，这与 Temporal outer harness 里「Code Mode 的 Python 也要 durable」可以叠：外层 workflow 记到哪一步，内层 sandbox 按 policy 重建。

官方 examples 把 Claude Code、Gemini CLI、Codex CLI、OpenCode、LangGraph、Google ADK 等**整 CLI 装进 sandbox 镜像**——此时 harness 逻辑在容器里，但**镜像选型、资源上限、网络 egress** 仍由平台配置。Harbor 评测：一 trial 一 sandbox，失败 trial 不影响邻居。Kubernetes 路径对接 **kubernetes-sigs/agent-sandbox** CR，OpenSandbox 做 runtime 而非重复造 CR 语义。

**MCP：暴露能力，不替代隔离。** `opensandbox-mcp` 向 Claude Code、Cursor 等宿主提供「创建 sandbox、执行命令、读写文本文件」等 tool。宿主仍决定**何时**调用、传什么镜像与 timeout；MCP stdio 配置只是把 `opensandbox-mcp --domain ...` 注册进 `mcpServers`。执行发生在 OpenSandbox 管理的 runtime——若 server 配的是 gVisor，MCP 路径与 Python SDK 路径隔离级别一致。记硬边界：**MCP 传意图，sandbox 划牢笼**；**Credential Vault 管 secret 怎么进请求，不管 model 怎么选 tool**——后者仍在 harness。

桌面与浏览器场景把隔离需求再抬高一档：Chrome、Playwright、VNC desktop 示例说明 OpenSandbox 不只服务「跑一段 Python」，而是**任意 OCI 镜像**的生命周期平台；GUI agent 的 harness 负责截图理解与动作规划，OpenSandbox 负责 Playwright 进程别逃出 designated 网络。

**配套能力补全信任链。** Credential Vault：出站 HTTP 注入凭证，workload 不见明文 secret——agent 在 sandbox 里 `curl` 外部 API 时，vault 替它签名，harness 不必把 key 写进 prompt。Ingress/Egress 网关：按 sandbox 控入站路由与出站策略，防止生成的代码扫描内网。`execd` 守护进程处理容器内命令与文件；OpenAPI spec 定义 lifecycle 与 execution API，可扩展自定义 runtime——OSEP 流程说明项目如何用公开 RFC 演进协议，而不是 silently 改 SDK。

Volume 示例（Docker PVC、K8s PVC、OSSFS）表明 sandbox 不只是 ephemeral shell：Coding agent 需要在实例里持久化 `node_modules` 或共享数据集时，平台层也要管挂载策略——这又是 harness 不该硬编码的细节。

OpenSandbox 还强调 **多入口同一控制面**：`osb` CLI、Python SDK、MCP server 都对着同一 lifecycle API——避免 Cursor 用一套集成、Harbor 评测用另一套。specs 里的 OpenAPI 让第三方 runtime 可插拔；OSEP 公开讨论 agent-sandbox CR 支持，说明它在对接 K8s 生态而不是 reinvent orchestrator。RL 与 batch eval 场景更在意启动 QPS：dev cluster 可 runc，untrusted pool 可 firecracker， researcher SDK 不变——隔离策略跟着 server 走，跟着 harness 版本走。

## 工程师实操：从 runc 升级到 gVisor 要动什么

好消息是 **SDK 不用改**：同一台 OpenSandbox server 上，管理员把安全运行时从 runc 换成 gVisor，新创建的 sandbox 自动继承；坏消息是 **镜像与系统调用要回归**：有些 agent 镜像里的 Chrome、老版本基础库在 gVisor 下行为会变，批量评测要在两种 runtime 各跑一轮基线。建议路径：本地开发用 runc 保速度；预发集群开 gVisor；只有多租户不可信代码池上 microVM。

与 harness 集成时，把「创建 sandbox」当成普通 tool：harness 只传镜像名、超时、资源上限；别在 prompt 里写「请在 Docker 里跑」——那会把隔离策略绑死在自然语言里。多轮命令应尽量 **复用同一 sandbox**，否则每句 bash 都冷启动，成本和延迟都会爆。

国内部署常卡在 **镜像拉取与签名**：官方 registry 带 Cosign，生产应 pin digest，而不是 `:latest`。与阿里云 ACK 集成时，agent-sandbox 相关 CR 在演进，要盯 OSEP 而不是只读 README 一页。

## 对照、误区与边界

对比 E2B、Modal 等托管沙盒 SaaS，OpenSandbox 偏**可自建、可 K8s 规模化**的平台层，镜像在三处官方 registry 发布并带 Cosign 签名——生产应用 digest pin。对比 Hermes 内置的 terminal backend（Docker、Modal 等），Hermes 选「agent 住哪」，OpenSandbox 选「不可信片段在哪跑」——个人 agent 可能两者都用：Hermes gateway 在 VPS，重命令丢给 OpenSandbox cluster。

常见误区一：「agent 在 sandbox 里」等于 prompt injection 无害——harness 若把 vault 挂载进容器，或 MCP 宿主泄露 API key，隔离救不了。误区二：Firecracker 永远最优——短任务 gVisor 常更划算。误区三：OpenSandbox 当 harness——无 model loop。误区四：以为接 MCP 就自动有 egress 策略——egress 要单独配组件，默认不能假设「沙盒无网」。

可带走的一句判断：**sandbox 选的是隔离级别与生命周期平台；harness 选的是 agent 怎么思考与调度；MCP 只是让宿主能远程按按钮——三者必须分开设计，才能在不改 agent 代码的情况下把 runc 换成 gVisor。** 下一步你若搭 agent 栈，应先画一张表：每一列写 harness、MCP 宿主、OpenSandbox server、secure runtime、Vault——问「这一列挂了，攻击者能触达什么」。表画不清，就不该上生产流量。

Harbor 评测场景把分级隔离说透：一 trial 一 sandbox，trial A 的 Agent 跑恶意 `rm -rf /` 只毁本实例，邻居 trial B 的 reward 曲线不受影响。管理员在 `~/.sandbox.toml` 把 `[secure_runtime]` 从 runc 切 gVisor，**SDK 零改动**——新 trial 自动继承；但 Chrome-heavy 镜像要在两种 runtime 各跑基线，因 gVisor syscall 拦截可能导致 headless 行为差异。与 Claude Managed Agents 叠用：Managed 的 `execute` 背后创建 OpenSandbox 实例，hand 在 gVisor 里，brain 无凭证调 MCP；Temporal outer harness 再包「等审批三天」——sandbox 只管 **单步执行边界**，不管 durable turn。Credential Vault 则补最后一环：Agent 在 sandbox 内 `curl api.internal`，vault 注入签名，prompt 里不出现 key——**MCP 传意图、Vault 管 secret、OpenSandbox 管隔离**，缺任一环「接了 MCP 就安全」都是错觉。

多轮命令应 **复用同一 sandbox**：每句 bash 都 `Sandbox.create` 会冷启动爆炸——harness 传 timeout 与资源上限即可，别把隔离策略写进 prompt。K8s 路径对接 agent-sandbox CR 时，OpenSandbox 做 runtime 而非重复 CR 语义；RL batch 可在 dev cluster 用 runc、untrusted pool 用 firecracker，researcher SDK 不变。与 E2B/Modal 托管 SaaS 比，OpenSandbox 偏 **可自建、可审计 digest pin**——合规团队要 Cosign 与 egress 组件显式配置，不能假设默认无网。

GUI agent 把 Chrome/Playwright 装进 OCI 镜像时，隔离级别决定 **多租户密度 vs 逃逸面**：短任务评测池优先 gVisor，长驻 desktop 会话可能选 Kata。harness 负责截图理解与动作规划，OpenSandbox 负责 Playwright 进程别逃出 designated 网络——again，MCP 只传「创建 sandbox、跑命令」意图，不替代 `[secure_runtime]` 配置。

---
**参考**
- [OpenSandbox README](https://github.com/alibaba/OpenSandbox)
- [OpenSandbox Secure Container Runtime Guide](https://github.com/alibaba/OpenSandbox/blob/main/docs/guides/secure-container.md)
- [OpenSandbox MCP README](https://github.com/alibaba/OpenSandbox/tree/main/sdks/mcp/sandbox/python)
