# T11 Run Screening on Selected Prompt Candidates — Review Explanation

## 一、这个任务在做什么（通俗版）

继续用 T10 的医学临床试验比喻：

T10 写好了初筛方案（protocol），T11 就是**实际执行初筛实验**。具体来说：

1. 把 T10 确定的 9 种候选药物（9 条 prompt）全部交给一个便宜的检测系统（deepseek-chat 模型）。
2. 每种药物用同一批 64 道标准测试题（smoke split）测一遍。
3. 记录每道题的结果：模型回答了什么（TRUE 还是 FALSE）、回答对了吗、回答能被解析吗。
4. 把所有原始数据存好，方便后续分析。
5. 对照 T10 定下的淘汰标准（E1-E4），检查哪些候选通过了初筛、哪些被淘汰。

**结果令人意外：所有 9 个候选都被淘汰了。**

- 唯一的宽松格式 prompt（P0）因为输出格式太乱，只有 26.6% 的回答能被解析——淘汰（E1: parse collapse）。
- 其余 8 个严格格式 prompt，模型几乎全部输出 FALSE——无论题目答案是 TRUE 还是 FALSE。这意味着模型没有真正在做推理，而是在"全选 FALSE"——淘汰（E3: all-false collapse）。

打个比方：你用某种检测仪器测了 9 种药物，结果发现这台仪器对 8 种药物只报告"无效"，对第 9 种药物的报告格式读不懂。问题不在药物——而是这台仪器本身不适合做这类检测。

所以 T11 的核心发现是：**deepseek-chat 这个模型不适合用来做 equational-theories 任务的 screening。** 它有系统性的全 FALSE 偏向，无法区分不同 prompt 的实际效果。T11 worker 正确地把这个问题上报给 Captain，让 Captain 决定下一步怎么办。

## 二、任务实现的详细解释

### 2.1 任务目标

T11 的核心目标是**执行** T10 冻结的 Stage A screening，而非设计新的 protocol。具体包括：

1. 用 9 条 text-ready local prompts 在 smoke split (64 problems) 上跑一遍 API eval。
2. 每条 run 产出 4 个必需 artifact：run_config.json、summary.json、predictions.jsonl、prompt_hash_manifest.json。
3. 所有 artifact 存放在 `artifacts/research_runs/screening/<prompt_id>/` 目录下。
4. 写一份 execution manifest 记录所有 run 的状态和指标。
5. 更新 handoff 文件，记录执行事实和 screening failure。
6. 不写 T12 shortlist 结论，不修改任何 frozen config。

### 2.2 任务流程

**Step 1：编写执行脚本 `_run_screening.py`**

Worker 编写了一个临时执行脚本（~165 行），核心逻辑是：

1. 从 `corpus_v1.jsonl` 加载 9 条 prompt 的 SHA256 哈希值。
2. 遍历 9 条 prompt，对每条调用项目已有的 `run_complete_prompt_eval()` 函数。
3. `run_complete_prompt_eval()` 内部调用 DeepSeek API，逐题发送 prompt + problem，收集模型响应，解析 verdict，计算 metrics，写出 `summary.json` 和 `predictions.jsonl`。
4. Worker 额外写出 `run_config.json`（记录 frozen 参数）和 `prompt_hash_manifest.json`（校验 prompt 文件完整性）。
5. 最后把所有 run 的结果汇总到 `screening_results.json`。

脚本严格使用 frozen 参数：temperature=0, max_tokens=256, provider=deepseek, model=deepseek-chat, repeats=1。

**Step 2：执行 9 条 screening run**

9 条 run 全部成功完成，没有 API 错误或重试。总耗时约 540 秒（~9 分钟）。

每条 run 的 raw output 都是真实 API 响应：
- 严格格式 prompt 的模型输出几乎全是单字 "false"（0.5-1 秒/题）。
- P0 宽松格式 prompt 的模型输出是多段推理文本（3-4 秒/题），因为模型试图构造 magma 反例。

**Step 3：写 execution manifest**

`screening_execution_manifest_v1.md`（~149 行）记录了：
- Execution config（provider、model、frozen 参数）
- Run directory layout
- Per-run results 表格（9 行 × 11 列：prompt_id, completed, problems, parsed, parse rate, accuracy, true recall, false recall, SHA256 match, elapsed）
- Artifact verification 检查结果
- E1-E4 elimination rules 的逐条应用
- Screening failure flag

**Step 4：更新 handoff 和 screening README**

- `docs/07_handoff.md`：添加 T11 执行结果、screening failure 说明、Captain 决策选项。
- `reports/research/screening/README.md`：更新为"screening execution 已完成"状态，标注 screening failure。

### 2.3 关键数据/配置变化

| 文件 | 变化 |
|---|---|
| `artifacts/research_runs/screening/<9 dirs>/` | 新增。每个目录含 4 个 artifact（run_config.json, summary.json, predictions.jsonl, prompt_hash_manifest.json） |
| `artifacts/research_runs/screening/screening_results.json` | 新增。9 条 run 的汇总结果 |
| `artifacts/research_runs/screening/_run_screening.py` | 新增。临时执行脚本（标记为 temporary） |
| `reports/research/screening/screening_execution_manifest_v1.md` | 新增。完整 execution manifest |
| `reports/research/screening/README.md` | 更新。状态改为"screening execution 完成"，标注 failure |
| `docs/07_handoff.md` | 更新。添加 T11 执行事实和 screening failure escalation |

### 2.4 Screening 结果详解

**P0 (宽松格式 baseline):**
- parse_success_rate = 0.266（17/64）
- 模型产出的 47/64 道题的回答是长段落推理文本，无法解析为 TRUE/FALSE
- 原因：P0 的 verdict_contract 是 `relaxed`，不要求单字输出，deepseek-chat 因此展开了推理
- 被淘汰：E1 (parse_success_rate < 0.95)

**8 个严格格式 prompt:**
- parse_success_rate 全部为 1.000（64/64）
- 模型输出几乎全部是单字 "false"
- true_recall: 0.000-0.032（31 道 true 题中最多答对 1 道）
- false_recall: 0.970-1.000（33 道 false 题中答对 32-33 道）
- 被淘汰：E3 (false_recall >= 0.95 AND true_recall <= 0.10)

**关键发现：**
1. deepseek-chat 对 equational-theories 任务有系统性全 FALSE 偏向
2. 这个偏向不随 prompt 结构变化：balanced、CE-first、trivial-first、saturated rules、fast filters 结果几乎一样
3. 唯一差异：P1.2.2 有 1 道 false 题答错（false_recall=0.970），其余全为 1.000
4. P1.2.3 和 P2.0.0 各有 1 道 true 题答对（true_recall=0.032），可能是偶然

### 2.5 对后续开发的意义

1. **Captain 决策点**：screening failure 需要 Captain 裁决后才能继续 T12。最可能的方向是换一个不同的 screening model。

2. **T12 (Screening Summary)**：T12 应该在 Captain 解决 model 问题后再写。如果换 model 重跑，T12 需要覆盖两次 screening 的结果比较。

3. **论文贡献潜力**：deepseek-chat 的全 FALSE 偏向本身是一个有价值的发现——如果多个模型都表现出类似的保守偏向，这可能成为论文中关于"LLM equational reasoning 的 default bias"的实证贡献（对应 RQ3: model-specific bias）。

4. **P0 parse failure 确认了 taxonomy 预测**：T07 taxonomy 中 P0 的 `verdict_contract = relaxed` 和 `parse_risk = high` 编码是正确的。P0 在 strict parser 下的 0.266 parse rate 验证了这个分类。

5. **Milestone 3 进度**：T11 执行完成，但 screening failure 意味着 Milestone 3 的退出条件（"shortlist 包含 3-5 个 prompt"）暂时无法满足。需要 Captain 干预后才能推进。

## 三、为什么给出 PASS 的 review 结果

### 核心检查维度

| 检查维度 | 结果 | 说明 |
|---|---|---|
| 任务目标是否完成 | 是 | 9 条 run 全部执行，4 个 artifact 全部产出，execution manifest 已写 |
| Allowed files 合规 | 是 | 修改的文件全部在 allowed list 内（artifacts/screening/, screening manifest, README, handoff） |
| Forbidden scope 合规 | 是 | 未修改 src/, tests/, prompts/, configs/, task board, data/ |
| 是否有伪实现/mock | 否 | 所有 predictions.jsonl 包含真实 API 响应（P0 的长段落推理、strict prompts 的单字 false） |
| Frozen config 是否遵守 | 是 | temperature=0, max_tokens=256, repeats=1, 9 条 prompt, smoke split — 全部匹配 T10 matrix |
| SHA256 是否验证 | 是 | 所有 9 条 prompt 的 hash 匹配 corpus_v1.jsonl |
| E1-E4 是否正确应用 | 是 | 独立 Python 脚本交叉验证，elimination 判定全部正确 |
| Screening failure 是否正确上报 | 是 | 0 candidates survive，正确按 shortlist rules Section 4 Step 3 escalation |
| 是否偷跑 T12 结论 | 否 | 没有 shortlist 判定、没有 ranking、没有 screening model 推荐 |
| 是否破坏已有功能 | 否 | 未修改任何代码文件，extractor tests 不受影响 |
| 验证是否充分 | 是 | validate-layout pass + artifact 完整性 + row count + SHA256 + metrics 存在性 |
| 延迟数据是否合理 | 是 | strict prompts 40-65s，P0 263s（长文本输出），符合 API 行为 |

### 发现的非阻塞问题

1. **N1-N3: metric naming inconsistency**：summary.json 使用 `true_accuracy`/`false_accuracy`，screening_results.json 和 manifest 使用 `true_recall`/`false_recall`。数值正确但命名不一致。来源是 `run_complete_prompt_eval` 的输出格式，不是 worker 的错误。

2. **N4: .claude/settings.json noise**：与 T08-T10 review 中相同的问题，IDE 自动积累的工具权限记录。

3. **N5: P0 异常延迟**：263 秒 vs 其他 40-65 秒。这是合理的——P0 的宽松格式导致模型输出长段落推理文本，token 数远多于单字 "false"。

### 总体判断

T11 worker 完成了一次干净、诚实的 screening 执行。9 条 run 全部成功完成，所有 artifact 齐全且经过验证，frozen config 未被修改。Screening failure（所有候选被淘汰）是一个真实的实验结果，不是执行错误——worker 正确识别并上报了这个 failure，没有试图掩盖或修改淘汰标准。执行脚本 `_run_screening.py` 是一个有用的临时工具，清晰地记录了执行逻辑。唯一的小瑕疵是 metric naming 的不一致（`true_accuracy` vs `true_recall`），这是底层 runner 的输出格式问题，不影响数据正确性。PASS。
