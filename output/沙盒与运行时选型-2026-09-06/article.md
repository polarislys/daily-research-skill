# Agent 运行时选型先问隔离级别，再问星数

日期：2026-09-06（Asia/Shanghai）  
问题点：OpenSandbox、Kubernetes SIG 的 agent-sandbox、以及 Hermes 那一串终端后端，到底哪一层叫 runtime、哪一层叫 sandbox？明天怎么选，才不会把「能跑」当成「能上客」。  
关键词：agent-runtime, sandbox, mcp, computer-use, observability

## 结论

2026 年 9 月，agent **runtime（运行时）** 和 **sandbox（沙盒）** 已经分成两层货。Runtime 管一次 agent 怎么活着：进程、会话、工具总线、审批回调。Sandbox 管不信任代码跑在哪：Docker 共享内核、gVisor/Kata 用户态或轻虚机、Firecracker 级隔离。阿里开源的 OpenSandbox 把自己写成「通用沙盒平台」：多语言 SDK、Docker / Kubernetes、面向 Coding / GUI / Eval / RL。它还在规格里写要对齐 `kubernetes-sigs/agent-sandbox`。Hermes 则把「七种终端后端」当成产品功能，说明运行时可以换，沙盒不能默认等于本机 shell。

对能跑、能评的岗位，下一步是 **跑**：给现网每条会执行代码的路径标隔离级别。不要先比 E2B / Daytona / OpenSandbox 谁星多。星数回答的是「社区热不热」，隔离级别回答的是「出事时爆破半径有多大」。

## 问题界定

只讨论运行时与沙盒怎么分层、怎么选。  
不讨论哪家 serverless 更便宜，也不把 MCP 协议本身当成沙盒——MCP 只描述工具怎么被调用，不保证工具跑在隔离里。

## 第一层：对象是什么

**agent runtime**：一次 agent 跑起来时的进程、状态和工具总线。它回答：会话存在哪、工具结果怎么回流、人怎么插进审批、任务中断后能否续跑。Codex 的 app-server、dsh 的 headless/sdk profile、Hermes 的 gateway 进程，都是 runtime。没有 runtime，模型只会「说要跑」，不会真的跑完一轮。

**sandbox**：执行层的隔离。它回答：这段模型生成的代码 / 这条 MCP 工具，碰不碰宿主机内核、出不出网、能不能读 `.ssh`。Docker 默认与宿主机共享内核，逃逸面在内核 CVE。gVisor（`runsc`）把系统调用拦在用户态。Kata / Firecracker 把每个沙盒推进轻虚机。OpenSandbox 文档写明 Kubernetes 侧可选 Kata 与 gVisor；这是隔离级别菜单，不是营销形容词。

**OpenSandbox**：阿里开源、Apache-2.0 的通用沙盒平台，仓库现指向 [alibaba/OpenSandbox](https://github.com/alibaba/OpenSandbox) / [opensandbox-group/OpenSandbox](https://github.com/opensandbox-group/OpenSandbox)。README 用例直接写 Coding Agents、GUI Agents、Agent Evaluation、代码执行、RL Training。控制面是生命周期服务 +（K8s 上）Operator；数据面是带 `execd` 的沙盒镜像。server v0.2.0 在 2026-06-15，v0.2.3 在 2026-08-26；本日不是「刚刚 0.2.0」，不要抄过期版本号。

**kubernetes-sigs/agent-sandbox**：SIG 在做的 K8s 原生沙盒 CR。OpenSandbox 的 OSEP-0002 要把自己的 SDK/API 接到这套 CRD 上，让「业务 → OpenSandbox SDK → K8s → agent-sandbox Pod」成为一条官方路径。含义：运行时厂商开始认集群原语，而不是每家自己发明 Pod 注解。

**observability（可观测性）**：没有轨迹，沙盒只是「偶发能拦住」。你们至少要能回答：这次 `exec` 用了哪张镜像、网络策略是什么、审批人是谁、工具返回有没有被截断。OpenSandbox 的 ingress / egress sidecar 把流量从「容器默认出网」改成「控制面声明的策略」；这是观测点，也是事故回放点。只记模型 token 日志的团队，出了逃逸也还原不了。

**computer-use / GUI agent**：要操作浏览器或桌面时，隔离对象从「一段 Python」变成「带显示和输入的会话」。OpenSandbox 把 GUI Agents 和 Coding Agents 并列写进 README，意思是同一套生命周期 API 要能挂不同镜像，而不是给 GUI 另起一个无法审计的本机窗口。本机弹一个真实 Chrome 让模型点，等于 L0 再加摄像头。

**MCP**：模型上下文协议，管工具发现和调用形状。它**不**自带沙盒。`npx` 拉一个 MCP server，默认信任作者、跑在你的用户权限里。审计仓库 [mcp-auditor](https://github.com/mkrtchian/mcp-auditor) 走的是动态对抗：连上真服务器、生成对抗输入、用 judge 打 PASS/FAIL。这是评测夹具，不是隔离本身。NSA/CISA 2026 年 6 月的 MCP 安全指引把「约束并沙盒化工具执行」写成部署方责任，协议层只给形状。

过去 24 小时没有新的「某云发布独家运行时」一手稿值得单独成篇；值得挖的是：沙盒平台已经按 **评测 / RL 批量** 和 **交互式单租户** 两条交付在长，而 MCP 安全仍停在「协议不管隔离」。K8s 侧还在长 Pool（预热）、BatchSandbox（一批 N 个）、Snapshot（暂停根文件系统以便稍后续跑）——这些名字一旦出现在你们的容量规划里，说明问题已经从「能不能跑起来」变成「空闲时怎么把资源还回去」。

## 第二层：机制与岗位含义

主线是工程接线，不是采购清单。

先画三格，再买东西：

1. **交互式编码 agent**（人在回路）：要快启动、可挂磁盘、审批能打断。Docker 或预热池往往够用；危险的是工作区 = 宿主机家目录。
2. **评测与回归**：要可复现镜像、TTL 回收、轨迹可回放。OpenSandbox 的 BatchSandbox / Pool 就是为高吞吐准备的；评测岗应要求「同一镜像哈希 + 同一网络策略」。
3. **Agentic RL**：要大批短寿命沙盒、任务模板、失败可丢。K8s batch + 安全容器运行时才是这条的默认，而不是笔记本 Docker Desktop。

隔离级别可以写成你们内部的枚举，避免口头「我们有沙箱」：

- L0：本机 shell（Hermes 的 local 后端就属于这档，只适合自己的机器）
- L1：容器，共享内核
- L2：gVisor / Kata
- L3：微虚机（Firecracker 一类）

选型时再加两问，避免被产品名带着走。第一问：**失败时状态还在不在？** 评测要「每次干净重建」；人工排查要「留盘可 ssh」。OpenSandbox 的 snapshot / pause 是后者；RL batch 是前者。混用会让回归集不可复现。第二问：**出网是默认允许还是默认拒绝？** 模型很会「为了装依赖而 curl」。egress sidecar 若只拦 80/443 以外的端口，包管理器仍然能把供应链拉进来。先写允许域名，再给沙盒。

Hermes 把 Daytona / Modal 写成可休眠后端，说明还有第四问：空闲是否计费。这对个人 agent 有意义，对要冻结评测镜像的团队反而危险——休眠后再唤醒，时钟、缓存、外部 ticket 状态都可能变。评测岗应禁止「可休眠」当默认。

**明天能做的一个动作**：把现网一条会 `exec` 或会调 MCP 的路径，对照上面 L0–L3 标出来，写进设计文档的一行表。若是 L0 且工具能写仓库外路径——当天就把工作区收进专用目录，网络改成默认拒绝。不要先迁移到 OpenSandbox；先禁止「模型生成的命令等于你的登录壳」。表里再加一列「出网策略」，空白就当默认允许，优先修这一列。

若已经要用开源控制面：读 [OSEP-0002](https://github.com/alibaba/OpenSandbox/blob/main/oseps/0002-kubernetes-sigs-agent-sandbox-support.md)，看你们集群是走 SDK→API server，还是要独立 ingress 直达 Pod。这两条的观测点不同：前者日志在控制面，后者流量可能绕过你们现有的 trace。选 ingress 直达时，必须同时把 trace id 从 SDK 打到 Pod 标签，否则事故只剩「有一个沙盒出过网」。

## 证据（24h）

- 仓库：
  - [alibaba/OpenSandbox](https://github.com/alibaba/OpenSandbox)（通用 agent 沙盒）
  - [opensandbox-group/OpenSandbox server v0.2.3](https://github.com/opensandbox-group/OpenSandbox/releases/tag/server%2Fv0.2.3)（2026-08-26）
  - [kubernetes-sigs/agent-sandbox 对接规格 OSEP-0002](https://github.com/alibaba/OpenSandbox/blob/main/oseps/0002-kubernetes-sigs-agent-sandbox-support.md)
  - [mkrtchian/mcp-auditor](https://github.com/mkrtchian/mcp-auditor)（对 MCP 做动态对抗，不是沙盒本身）
- 博客 / 文档：
  - [OpenSandbox 架构说明（Northflank，二手但可对照 README）](https://northflank.com/blog/alibaba-opensandbox-architecture-use-cases)
  - [Kubernetes Deployment](https://open-sandbox.ai/kubernetes/deployment)
  - [Hermes 多终端后端说明](https://github.com/NousResearch/hermes-agent)
- 视频：本日未见。
- 公司 / 产品 / 融资：本日未见新融资稿。E2B / Daytona / Runloop 等商业 runtime 仍在市场上，但本日没有必须引用的新一手发布。

## 未证实

- 第三方「2026 runtime 选型」长文把 Runloop / Blaxel / Daytona / E2B 并列，数字和定价无法在官方页逐条对上，本文不引用其结论。
- OpenSandbox 星数在抓取页和镜像站不一致，以仓库页为准，不写死营销数字。
- 「MCP 自带沙盒」是常见误读；协议文本和 NSA/CISA 的 MCP 安全指引都把隔离留给部署方。
