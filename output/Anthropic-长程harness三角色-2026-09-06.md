---
形态: 产品剖析
主题: Anthropic-Harness
日期: 2026-09-06
---

# 长程 Agent 的真正杠杆，是把「做」和「判」拆成两个上下文

这篇只回答一个问题：Anthropic 在 2026 年把长程 coding harness 从「初始化 + 编码」演进成 planner / generator / evaluator 三角色，到底多解决了什么、又付出了什么代价。如果你已经在用 Claude Agent SDK 或类似多 session 方案，值得对照自己的环是不是还在让同一个模型既写代码又给自己打分。

## 以前为什么不行

2025 年 11 月那篇《Effective harnesses for long-running agents》已经把痛点说透了：context 窗口有限，复杂项目不可能一次跑完；compaction 能续命，但挡不住两类崩法——一是 agent 总想 one-shot 整个应用，做到一半 context 耗尽，下一 session 对着半拉子工程猜历史；二是做到一定程度就宣布「完成了」，人类一眼还能用的功能它自己觉得够了。

Anthropic 当时的解法是 initializer + coding agent：首轮写 `init.sh`、JSON feature list（每项带 steps 与 `passes: false`）、`claude-progress.txt` 和 git 基线；后续每 session 只做一个 feature，Puppeteer 测完再 commit。社区很快收敛到类似思路——任务清单、进度文件、结构化 handoff。机制上是对的：把「状态」写进仓库和 JSON，而不是赌模型记得住。Initializer 还强调 **只允许改 passes 字段**，防止 agent 删测试糊弄过关。

但复杂任务跑久了，还有两个洞没填。一是 **context anxiety**：窗口还没满，模型就开始收尾；compaction 保留连续性，却给不了干净 slate，焦虑还在。Labs 在 Sonnet 4.5 上测过，单靠 compaction 撑不起数小时任务，必须 **hard reset + handoff artefact**。二是 **self-evaluation bias**：让写代码的同一个实例评自己的活，它几乎总会偏乐观——设计好不好、测试过没过，它都倾向于给自己过关。这在主观任务（前端审美）和可验证任务（端到端功能）里都一样要命：solo run 的 retro game maker 二十分钟九美元，界面像那么回事，play mode 输入无响应——代码里 entity 与 runtime  wiring 断了，自评却没拦住。

## 三角色怎么转

2026 年 3 月 Prithvi Rajasekaran 的《Harness design for long-running application development》把 GAN 的「生成器—判别器」结构借进 harness，落成 **planner / generator / evaluator**，并叠在更早的「分块 + 文件 handoff」之上。

**Planner** 接 1～4 句用户 prompt，扩成完整产品 spec：功能列表、优先级、高层技术方向，但刻意不写死实现细节——怕 spec 里一个错字 cascade 到后面。它还负责把 AI 能力织进产品故事，并可读 frontend design skill 定视觉语言。同一句话「2D retro game maker」，solo agent 只做编辑器壳子；planner 扩成 16 feature、10 sprint，含动画、行为模板、音效、AI 辅助 sprite、可分享 export。输出是结构化 artefact，不是聊天记忆。

**Generator** 继承旧 harness「一次一个 feature / sprint」的纪律，用 React + Vite + FastAPI + SQLite/PostgreSQL 增量实现，git 管版本。关键变化：它不再独自承担终局 QA， sprint 结束只做自检，然后交给 evaluator。早期还 **self-evaluate before QA**，但终局裁决权外移。

**Evaluator** 是这次架构的杠杆。它拿 Playwright MCP 像真人一样点页面、打 API、查库，再按 rubric 打分——产品深度、功能、视觉、代码质量，每项有硬阈值，任一不及格整 sprint 失败，反馈必须可执行。Sprint 3 的 level editor 合同有 27 条可测标准；evaluator 能报「矩形填充只改起终点、Delete 键条件写错、FastAPI 路由顺序导致 reorder 被当成 id」这类 **可直接改代码** 的 bug。早期版本还有 **sprint contract**：写代码前 generator 和 evaluator 先谈「什么叫 done、怎么测」，把高层 user story 桥接到可测行为。Rajasekaran 指出，spec 故意保持高层，就是为了避免 planner 过早锁死实现；contract 是 **运行时** 把故事翻译成测试的桥——这和 BDD 里 scenario workshop 类似，只是双方都是 agent。

前端 harness 是同一哲学的先导实验：四条 rubric（design quality、originality、craft、functionality）把「美不美」拆成可打分项；evaluator 用 Playwright **动态导航** 而非静态截图，5～15 轮迭代，荷兰艺术博物馆站从第九轮安全 landing 跳到第十轮 **CSS 透视 3D 展厅**——说明 **外部 critique 能驱动生成器做审美风险**，而非模板收敛。Full-stack 只是把 rubric 从四设计准则换成产品深度/功能/视觉/代码质量，并把 **可玩性** 变成 hard gate。

三者通信用 **文件** 而非共享长 context：A 写 spec/contract/QA 报告，B 读文件再动代码。这样 evaluator 可以开 **fresh context**，看不到 generator 的推理链，减轻「自己给自己放水」。前端实验里，generator 与 evaluator 循环 5～15 轮，单次最长约四小时；evaluator 会自己导航、截图、再打分。Full-stack 对比里，三角色 harness 六小时约两百美元，但 playable test mode 真的能动——physics 虽糙，核心闭环成立。

环是这样的：Planner 一次（或极少次）→ Generator 按 sprint 增量交付 → Evaluator 独立验收 → 失败则带 findings 回到 Generator，**不带 evaluator 全文 reasoning**。这和 Actor-Critic、code review 是同构的：**分离 generation 与 evaluation**，比调一个模型「更苛刻地批评自己」可行得多——evaluator 仍是 LLM，仍可能偏宽，但单独调 prompt、few-shot 校准比改 generator 容易。Rajasekaran 描述 tuning loop：读 evaluator log，找与人类判断分叉的案例，改 QA prompt，几轮后才稳定；出厂 Claude **并不天然是好 QA**。早期 evaluator 会把 legitimate bug **自我说服为可接受**，或只测 happy path——这和人类 junior QA 的成长曲线一样，说明 **evaluator prompt 是产品资产**，不是默认能力。

SDK 层实现上，三角色 **共享 tool 集与 system prompt 骨架**，差异主要在 **首轮 user prompt**——2025 文 footnote 也说过 initializer 与 coding agent 仅是 prompt 不同。2026 版则是 planner / generator / evaluator 三套 session prompt，外加文件协议。对你意味着：harness 的边际成本在 **编排与 artefact schema**，不在再训一个模型。Compaction 在 Opus 4.6 长 session 里仍运行，但 **hard reset between roles** 在前端实验里是标配——全栈版因模型变强可连续跑，说明 **reset 是模型属性函数**，不是道德准则。

## 对照、边界与 harness 减法

三角色不是推翻 2025 方案，而是 **spec 自动化 + 外部 QA** 的升级。Feature list、progress log、init.sh、git 纪律仍在 generator 侧；新增的是 planner 替人写 spec，evaluator 替人做 E2E。Opus 4.6 后 context anxiety 减轻，**整段 context reset 拿掉**，改靠 SDK 自动 compaction；sprint contract 在 ablation 里也可删；evaluator 从「每 sprint 评」退成「跑完再评一次」——任务落在模型能力圈内时 evaluator 变 overhead，在边界外仍有明显 lift。这验证 Anthropic 常提的原则：**harness 每个组件都在赌模型做不到 X；模型变强，组件会过期**。

边界要诚实：evaluator 仍可能 superficial test、漏 layout 直觉问题；成本可以是 solo 的二十倍；museum-quality 之类 rubric 措辞会意外收敛视觉风格；**生产级多 repo** 泛化公开一手仍偏 demo。Agent Patterns Catalog 把同一模式抽象成 driver + 固定 rubric，禁止 evaluator 看 generator CoT——与工程文一致。

若你在自建 harness，可操作的拆法是：**Planner 输出 machine-readable spec（JSON feature list 的成人版）**；**Generator  session 只读 spec + git + progress，写代码**；**Evaluator session 只读 diff + rubric + 运行态，写 findings JSON**。Driver 负责在失败时把 findings 喂回 Generator，但 **截断 evaluator 推理链**，避免 context 污染。文件通信还带来 crash recovery——进程挂了，磁盘上的 contract 和 QA 报告还在，这比把状态押在长 chat 里更接近工程实践。

和 OpenAI「harness engineering」、Codex platform 叙事对照：行业 2026 共识是 **模型是 brain，harness 是手与流程**；Anthropic 三角色进一步说 **brain 也不该兼任终审法官**。你换更强模型时，应预期 planner 变轻（用户 prompt 可更短）、evaluator 抽检频率可降，但 **spec 与 findings 的结构化** 不会消失——因为协作审查需要的是 artefact，不是更长的 CoT。

若只抄「三个 agent 名字」而不抄 **文件协议 + rubric + fresh context**，很容易得到三个互相污染的 chat role，bias 仍在，只是多了两次 handoff latency。最小可复刻集是：**(1) planner 产出带 acceptance 的 feature artefact；(2) generator 单任务 session；(3) evaluator 只看 artefact+运行态；(4) driver 循环**。Playwright MCP 可替换为任意 E2E runner，但 **分离上下文** 不可省。2025 initializer 的 JSON feature list 与 2026 planner spec 可视为同一 artefact 线的演进——差别在于 **谁写 spec、谁终检**；你若已有人类 PM 写 PRD，planner 可弱化，evaluator 仍值得保留。长程任务最终拼的是 **artefact 能否让 cold-start session 在十分钟内恢复世界状态**，三角色是把这条纪律推到 spec 与 QA 两端。

我的判断：**长程 harness 的核心不是更多 tool，而是可复查的分工与 artefact**——planner 产出 spec，generator 产出 diff，evaluator 产出结构化 findings；模型换代时，先问哪一环已被原生能力吃掉，再删复杂度。

举一个 sprint contract 如何救场的具体片段：Generator 交付 level editor 后，Evaluator 用 Playwright 点「画矩形填充」——发现只改起终点、中间格不变；再测 Delete 键，报「条件写错导致删错层」；又发现 FastAPI 把 `/reorder` 路由放在 `/{id}` 后面，reorder 请求被当成 id 解析。这三条 findings 写进 JSON，Generator 下一 session **只读 findings + diff**，不必重读 evaluator 全文推理——这就是 fresh context 的价值：credit 落在「哪条 contract 项失败」，而不是「模型觉得自己差不多」。若把 evaluator 和 generator 塞进同一长 chat，模型极易把「Delete 键有小问题但总体不错」自我说服；分离后，rubric 阈值是硬的，任一不及格整 sprint 失败。对你自建 harness 的启示：**evaluator 产出必须是可机器消费的 findings**，人类 reviewer 的「这里再改改」若不能结构化，就退化成 self-evaluation bias 的人类版。

---
**参考**
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
