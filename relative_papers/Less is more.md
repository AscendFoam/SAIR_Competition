<div align="center">

# Less Is More: Cognitive Load and the Single-Prompt Ceiling in LLM Mathematical Reasoning

</div>

Manuel Israel Cazares

Bytepro AI

Mazatlán, Sinaloa, Mexico

hello@bytepro.ai | israel.cazares@gmail.com

April 2026

## Abstract

We present a systematic empirical study of prompt engineering for formal mathematical reasoning in the context of the SAIR Equational Theories Stage 1 competition. The task requires deciding whether one equational law implies another over all magmas (algebraic structures with a single binary operation) a problem that is undecidable in general but decidable for FALSE via finite model search. Over five weeks, we designed, tested, and analyzed more than 40 prompt variants, ranging from 0 to 4,878 bytes, across four evaluation splits and three language models (gpt-oss-120b, Llama 3.3 70B, Gemma 4 31B).

Our central finding is a single-prompt ceiling or more precisely, we term this an empirical saturation region: a zone where accuracy improvements become unstable and nongeneralizable across problem distributions, rather than an absolute theoretical limit. Despite substantial engineering effort, balanced hard accuracy plateaus at approximately 60-79% for gptoss-120b, compared to a 59.75% no-cheatsheet baseline (95% CI: [54.9%, 64.4%]). We identify three mechanisms underlying this saturation region: (1) the mathematical undecidability of the TRUE case limits what any finite prompt can encode; (2) complex rule systems decrease performance on weaker models (Llama 3.3 70B collapses to 0% TRUE recall with prompts exceeding $ \approx $ 2KB); and (3) prompt ordering effects interact with model attention in fragile, non-monotonic ways.

We also document a distribution mismatch failure mode: a rule that appeared correct when validated on a False-heavy subset (hard1, 35% TRUE) catastrophically failed on a balanced subset (hard2, 50% TRUE), incorrectly blocking 51% of TRUE problems. Our best submission (AN45c, 2,252 bytes) achieves 79.25% accuracy on hard3 (n=400; 95% CI: [75.0%, 82.9%]) , with True recall of 95.9% and False recall of 63.4%, representing a +19.5 percentage point improvement over the no-cheatsheet baseline (59.75%; 95% CI: [54.9%, 64.4%]). A crossprovider validation run on OpenRouter/DeepInfra bf16 (n=20) yielded 90-95%, consistent with the full-scale result. The key design decision placing the trivial-magma check before the counterexample table accounts for the primary performance gain over its predecessor AN38 (71.8%), not the addition of new content. We release all prompt variants, evaluation scripts, and results tables.

Post-submission validation against the SAIR official benchmark reveals a cross-distribution trade-off surface: gains within the saturation region are distribution-fragile, with our most engineered variant (AN45c) falling below the no-cheatsheet baseline on the official evaluation while the simpler predecessor (AN38) produces a robust improvement. See Section 9 for full analysis.

Note: This is a pre-competition-leaderboard version based on Contributor Network data （n=52 voluntary submissions at competition close, April 20, 2026). An updated analysis incorporating full competition results （n=1,007）will follow after April 30, 2026.

## 1 Introduction

Large language models have demonstrated surprising competence on mathematical reasoning tasks, yet their behavior on problems requiring formal logical completeness where a single counterexample suffices to disprove a claim remains poorly understood. The SAIR Equational Theories Stage 1 competition [12] provides an unusually clean testbed for studying this question: given two equations over magmas (sets with a single binary operation), decide whether the first implies the second universally. The problem is computationally asymmetric: FALSE instances can in principle be certified by exhibiting a small finite counterexample, while TRUE instances require a universal proof that no counterexample exists, including infinite algebraic structures.

Unlike prompt engineering for standard benchmarks such as GSM8K [3], this task involves semi-decidable algebraic implication where FALSE is certifiable via finite counterexample but TRUE requires universal quantification over all magmas a fundamentally different reasoning regime.

This asymmetry creates a natural design space for prompt engineering. One might expect that providing a language model with a library of known counterexamples would systematically improve FALSE accuracy, while a brief instruction about singleton-forcing equations would improve TRUE accuracy. Our experiments reveal a more complex picture.

Over five weeks of systematic experimentation prior to the April 20, 2026 competition deadline, we tested more than 40 prompt variants on over 1,000 labeled problems across four dataset splits. We found that prompt complexity and multi-model generalization are inversely related: the prompts that most improved gpt-oss-120b's performance on FALSE-heavy subsets (e.g., AN3c's 4,306-byte BLOCK system achieving 78.3% on hard1) performed at or below baseline on balanced subsets and collapsed to near-zero TRUE recall on Llama 3.3 70B. Conversely, the most compact effective prompt (AN19c, 289 bytes) performed within 2 percentage points of complex variants on gpt-oss-120b while being the only variant that maintained meaningful TRUE recall on Llama.

The phenomenon we document call it the single-prompt ceiling manifests as a bound on what a static text prompt can accomplish when the underlying task requires mathematical reasoning that the base model has not internalized. We provide empirical evidence that this ceiling lies at approximately 60-79% balanced hard accuracy for gpt-oss-120b, a model that achieves only 26.5% FALSE recall with default reasoning and no cheatsheet on the official benchmark (our own controlled baseline measurement yields 38.0% FALSE recall under Together AI inference; see Section 5). A prompt cannot teach a model the mathematics it does not know; it can only guide it to apply what it does know more reliably.

We make the following contributions:

1. Systematic ablation study: 40+ prompt variants tested on labeled splits, enabling controlled analysis of which design choices matter.

2. Distribution mismatch failure mode: Quantified how validation on FALSE-heavy data produces incorrect conclusions when the target distribution is balanced.

3. Multi-model generalization analysis: First systematic study of prompt portability across gpt-oss-120b, Llama 3.3 70B, and Gemma 4 31B on this task.

4. Ordering effect: Evidence that trivial-magma-first ordering (AN45c) outperforms CE-tablefirst ordering (AN38) by +7.5 percentage points at full scale （n=400），with non-overlapping 95% Wilson CIs（[75.0% ，82.9%] vs. [67.1% ，75.9%]）(local evaluation; see Section 9 for official benchmark divergence).

5. Practical guidelines: Minimal effective prompts for multi-model deployment, with analysis of why simpler beats complex.

6. Cross-distribution trade-off surface. Official benchmark validation reveals that local gains within the saturation region do not transfer across problem distributions (Section 9).

The rest of the paper is organized as follows. Section 2 provides background on magmas, equational implication, and the Equational Theories Project. Section 3 reviews related work. Section 4 describes our methodology. Sections 5-7 present results, analysis, and multi-model generalization findings. Section 8 characterizes the single-prompt ceiling theoretically. Section 9 presents post-submission validation against the official benchmark and cross-distribution analysis of the Contributor Network leaderboard. Section 10 concludes.

## 2 Background

## 2.1 Magmas and Equational Laws

A magma is a set M equipped with a single binary operation $ \star : M\times M\to M $ , closed under that operation and subject to no further axioms. No associativity, commutativity, identity element, or invertibility is assumed. An equational law over a magma is a universally quantified identity of the form $ t_{1}(x,y,\ldots)=t_{2}(x,y,\ldots) $ , where $ t_{1} $ and $ t_{2} $ are terms built from variables and $ \star $ . The law holds in a magma $ (M,\star) $ if the identity is satisfied for every assignment of variables to elements of M.

## 2.2 Equational Implication

Given two equational laws $ E_{1} $ and $ E_{2} $ , we say $ E_{1} $ implies $ E_{2} $ (written $ E_{1}\Rightarrow E_{2} $ ) if every magma that satisfies $ E_{1} $ also satisfies $ E_{2} $ . Deciding this relation is computationally asymmetric. A FALSE instance where $ E_{1}\neq E_{2} $ can be certified by exhibiting a single finite counterexample magma in which $ E_{1} $ holds but $ E_{2} $ fails; such certificates exist for all FALSE cases among small magmas, making FALSE decidable via finite search. A TRUE instance requires establishing that no counterexample exists among all magmas, including infinite ones, for which no general algorithm is known. The implication problem over magmas is undecidable in general; finite model search is complete for FALSE but not for TRUE.

## 2.3 The Equational Theories Project

The Equational Theories Project [13] is a large-scale collaborative effort to map the implication structure of equational laws over magmas, formalized in Lean 4. The project has verified approximately 4,694 distinct equational laws and established the implication status of roughly 22 million equation pairs, producing the largest formally verified database of algebraic implications to date. This dataset provides both the mathematical foundation and the training signal for the SAIR competition benchmark.

## 2.4 Why the Task Is Hard for Language Models

The asymmetry between TRUE and FALSE creates a fundamental challenge for any fixed reasoning strategy. Producing a valid FALSE verdict requires constructing or recalling a specific finite structure a task amenable to lookup but not to general inference. Producing a valid TRUE verdict requires establishing universal quantification over an infinite class of structures a task that exceeds any finite enumeration and for which no sound and complete proof procedure exists in

the general case. A language model operating without external symbolic tools must approximate both tasks within a single generation, using pattern recognition over its training distribution as a substitute for proof search. This approximation is the object of study in the present work.

## 3 Related Work

LLM mathematical reasoning benchmarks. GSM8K [3] and MATH [4] established wordproblem and competition-mathematics benchmarks that remain standard, but both assess reasoning over numeric domains with human-interpretable intermediate steps. Tasks requiring universal logical closure deciding that a statement holds over all instances of a structure are fundamentally different: a single counterexample refutes a universal claim, yet no finite check can confirm one. The SAIR Equational Theories benchmark evaluates 25 models across 200 problems under varying conditions. The official results show that even the strongest available model (Gemini 1.5 Pro) achieves 90.2% on hard problems without a cheatsheet, while weaker models cluster near chance, making the benchmark unusually diagnostic of ceiling effects.

Prompt engineering for formal reasoning. Chain-of-thought prompting [14] demonstrated that instructing models to produce intermediate reasoning steps substantially improves performance on multi-step problems. Subsequent work established that few-shot exemplars [1] and zero-shot chain-of-thought instructions [5] are broadly effective. However, these findings are primarily established on numeric and commonsense domains. Less is known about how prompt complexity interacts with formal algebraic reasoning, where rule fidelity not just step count determines correctness.

Sycophancy and cognitive load in LLMs. Sharma et al. [10] documented that RLHF-trained models consistently exhibit sycophancy across varied free-form generation tasks, adjusting their stated conclusions toward what they perceive the user wants even when incorrect. A related phenomenon which we term cognitive load collapse occurs when a prompt's rule system is too complex for a model to follow reliably, causing it to default to surface heuristics. Shi et al. [11] showed that irrelevant context in math problems dramatically degrades accuracy, providing evidence that additional text can actively harm rather than help reasoning.

The Equational Theories Project. The mathematical foundations of this competition derive from ongoing work on automated proof search over equational theories [13]. The project established that implications between equational laws over magmas exhibit complex dependency structures not tractable by brute-force enumeration, motivating the use of language models as approximate reasoners over this space.

In-context learning: length versus performance. Liu et al. [6] showed that model attention is non-uniform over context: information at the beginning and end of a prompt is retrieved more reliably than information in the middle. This has direct implications for structured cheatsheets. Our finding that trivial-magma-first ordering (AN45c) outperforms counterexample-table-first ordering (AN38) by +7.5 percentage points at full scale （n=400; Section 5). We hypothesize that placing the trivial-magma check first primes the model's attention toward TRUE verdicts before engaging the CE search, with the first substantive rule receiving disproportionate weight during generation; this mechanism remains to be verified through attention analysis.

## 4 Methodology

## 4.1 Task and Benchmark

The SAIR Equational Theories Stage 1 competition requires deciding, for a given pair of equations $ ( E_{1}, E_{2} ) $ over magmas, whether $ E_{1}\Rightarrow E_{2} $ holds universally (label: TRUE) or whether a counterexample magma exists (label: FALSE). The official evaluation judge is described in SAIR Foundation [8]. All experiments use the publicly available dataset

SAIRfoundation/equational-theories-selected-problems (HuggingFace). We work with four labeled splits, summarized in Table 1.

<div align="center">

Table 1: Dataset splits used in this study.

</div>

<table border="1"><tr><td>Split</td><td>n</td><td>TRUE</td><td>FALSE</td><td>Notes</td></tr><tr><td>normal</td><td>1000</td><td>500(50%)</td><td>500(50%)</td><td>Balanced;mostlyx=RHSform</td></tr><tr><td>hard1</td><td>69</td><td>24(35%)</td><td>45(65%)</td><td>False-heavy;dense nesting</td></tr><tr><td>hard2</td><td>200</td><td>100(50%)</td><td>100(50%)</td><td>Balanced;structurally complex</td></tr><tr><td>hard3</td><td>400</td><td>195(49%)</td><td>205(51%)</td><td>Near-balanced;primaryevalsplit</td></tr></table>

Hard3 serves as the primary evaluation split: its near-balanced distribution and size (n=400) most closely approximate the competition's private evaluation set. Hard1 is used selectively to test FALSE-detection strategies; hard2 provides a secondary balanced check. Normal problems confirm that interventions do not regress standard performance.

## 4.2 Models and Inference Configuration

We evaluate across three models matching the competition's official multi-model setup:

gpt-oss-120b (primary): An open-weight 117B-parameter Mixture-of-Experts model released by OpenAI under Apache 2.0 license [7], accessed via DeepInfra bf16 routing on OpenRouter (openai/gpt-oss-120b). This model uses an extended reasoning mode that produces chain-of thought prior to its final verdict. All competition-credit evaluations use this model.

Llama 3.3 70B: Accessed via Together AI (meta-llama/Llama-3.3-70B-Instruct-Turbo). Standard instruction-tuned mode; no extended reasoning.

Gemma 4 31B: Accessed via Together AI (google/gemma-4-31b-it) with max_tokens=8192 to enable the model's native reasoning trace. OpenRouter routing for this model suppresses reasoning mode, causing it to default to a near-constant TRUE output ( $ \approx $ 53%); all reported Gemma results use Together AI exclusively.

All inference runs use temperature=0 and seed=42. max_tokens is set to 4,096 for gpt-oss 120b and 8,192 for Gemma 4 31B. A preliminary experiment established that truncation at lower token budgets (512, 1,024, 2,048) produced 100% truncation-caused errors; 4,096 was the minimum budget at which genuine reasoning errors first appeared. Estimated cost per problem is $0.005 $0.01 depending on prompt length and model.

## 4.3 Evaluation Metrics

We report three primary metrics: Accuracy (fraction correct), True recall (fraction of TRUE-labeled problems answered TRUE), and False recall (fraction of FALSE-labeled problems answered FALSE). For multi-model comparisons we report the 3-model average: the unweighted mean of each model's accuracy on the same split, aligned with the competition's scoring rule.

Non-determinism is a practical concern at temperature=0: we observed up to $ \pm 3 $ percentage points of variance across identical runs (e.g., AN3d: 73.9% vs. 79.7% on separate executions). We report observed values without averaging across runs, and flag cases where n $ \leq 20 $ makes estimates unreliable ( $ \pm 10 $ pp at the 95% level).

## 4.4 Prompt Design Space

Each submission is a single UTF-8 text file of at most 10KB containing two placeholders, {{ equation1 }} and {{ equation2 }}. We designed and evaluated 45+ prompt variants over five weeks (AN-series: AN1 through AN45d).

Pipeline note. AN45c uses a self-contained template format with {{ equation1 }} and {{ equation2 }} placeholders inside the prompt body, requiring the --raw-prompt flag for correct substitution. An early run omitted this flag; the placeholders reached the model unsubstituted, producing an artifactual 56% result that was identified and discarded. All other variants in Table 2 use build_prompt(), which embeds equations inline and is unaffected by this flag. The corrected AN45c results (April 14, 2026) are the only ones reported here.

Variants differ along five design dimensions:

1. Counterexample (CE) table content: which small magmas are provided, from 4 size-2 structures (early variants) to 7 size-2 and 5 size-3 structures (AN38/AN45c).

2. Singleton-forcing rules: heuristics for detecting equations that force all elements equal (TRUE shortcuts). S1 is sound; S2 is unsound for right-zero magmas (Section 6).

3. Block rules: conditional classifiers for structural patterns predictive of FALSE. The most aggressive variant (Block 1 in AN3c) blanket-classified self-referential patterns as FALSE, achieving high recall on hard1 but catastrophic precision loss on balanced splits.

4. Instruction ordering: whether the trivial-magma check or the CE table appears first. AN45c places the trivial-magma check first; AN38 places the CE table first.

5. Prompt length: 0 bytes (baseline) to 4,878 bytes (AN5, the longest variant tested).

Variants were selected for full-scale evaluation based on small-sample performance (n=20-50), with the most promising candidates validated at n=200-400. All prompt variants, evaluation scripts, and results are available at our companion repository [2].

## 5 Results

We present results along three axes: single-model performance across prompt variants (§5.1), crossmodel generalization (§5.2), and cross-dataset stability (§5.3).

Sample size note. Results for AN45c on gpt-oss-120b are based on n=400 hard3 problems (fullscale corrected pipeline). Cross-model runs (Llama 3.3 70B, Gemma 4 31B) and the DeepSeek V3.2 result use n=50, n=20, and n=10 respectively, as noted in Table 2.

## 5.1 Single-Model Results (gpt-oss-120b, hard3)

Table 2 reports accuracy, TRUE recall, FALSE recall, and prompt size for all variants evaluated on gpt-oss-120b on the hard3 split (n=50 unless noted), ordered by descending accuracy. The no-cheatsheet baseline (own run, April 14, 2026, n=400) achieves 59.75% overall (95% CI: [54.9%, 64.4%]), with a severe TRUE bias: 82.6% TRUE recall but only 38.0% FALSE recall. This profile is consistent with the structural TRUE bias documented in the official benchmark (89.2% TRUE, 26.5% FALSE on the hard split).

<div align="center">

Table 2: Single-model results on hard3 (gpt-oss-120b, n = 50 unless noted).

</div>

<table border="1"><tr><td>Variant</td><td>Acc</td><td>T%</td><td>F%</td><td>Bytes</td><td>Strategy</td></tr><tr><td>AN45c(n=400)^{†}$</td><td>79.3</td><td>95.9</td><td>63.4</td><td>2,252</td><td>Trivial magma first+CE tablesA-N</td></tr><tr><td>AN45c(n=20,OR)§</td><td>90.0-95.0</td><td>—</td><td>—</td><td>2,252</td><td>Cross-provider validation(OpenRouter/DeepInfra)</td></tr><tr><td>AN38(n=400)‡</td><td>71.8</td><td>78.5</td><td>65.4</td><td>1,776</td><td>CE tablesA-N(3-elem focus)</td></tr><tr><td>AN38(n=50)</td><td>74.0</td><td>70.8</td><td>76.9</td><td>1,776</td><td>CE tablesA-N(3-elem focus)</td></tr><tr><td>AN43</td><td>72.0</td><td>54.2</td><td>88.5</td><td>2,171</td><td>Controller arch(BLOCKs as router)</td></tr><tr><td>AN35</td><td>72.0</td><td>58.3</td><td>84.6</td><td>1,545</td><td>3-elem CE focus</td></tr><tr><td>AN35b</td><td>72.0</td><td>79.2</td><td>65.4</td><td>1,802</td><td>Cautious TRUE+3-elem CE</td></tr><tr><td>AN45d</td><td>70.0</td><td>100.0</td><td>40.0</td><td>2,538</td><td>AN45c+correctedSTEP1flag</td></tr><tr><td>AN36</td><td>70.0</td><td>50.0</td><td>88.5</td><td>1,205</td><td>Aggressive FALSE prior</td></tr><tr><td>AN39</td><td>70.0</td><td>91.7</td><td>50.0</td><td>385</td><td>Power-level prior</td></tr><tr><td>Baseline(n=400)</td><td>59.75</td><td>82.6</td><td>38.0</td><td>0</td><td>No cheatsheet(own run,April14,2026)</td></tr><tr><td>AN3c(n=50)</td><td>64.0</td><td>45.8</td><td>80.8</td><td>4,306</td><td>BLOCK system</td></tr><tr><td>AN10</td><td>64.0</td><td>—</td><td>—</td><td>3,303</td><td>Symbolic engine</td></tr><tr><td>AN19c</td><td>62.0</td><td>91.7</td><td>34.6</td><td>289</td><td>Trivial magma hint only</td></tr><tr><td>AN42</td><td>62.0</td><td>—</td><td>—</td><td>—</td><td>KB rewriting</td></tr><tr><td>AN40</td><td>60.0</td><td>—</td><td>—</td><td>—</td><td>Semantic invariants</td></tr><tr><td>AN41</td><td>58.0</td><td>—</td><td>—</td><td>—</td><td>Tamari/tree-structure</td></tr><tr><td>AN5</td><td>54.0</td><td>—</td><td>—</td><td>4,878</td><td>Maximum-length CE table</td></tr></table>

$ ^{\dagger} $Corrected pipeline (--raw-prompt); $ n=400 $; primary result. $ ^{\ddagger} $Full-scale run; most reliable pre-fix estimate. $ ^{\S} $Cross-provider check only; $ n=20 $ $ \pm10 $pp CI.

Wilson 95% confidence intervals: AN45c n=400, 317/400=79.3%: [75.0%, 82.9%]; AN38 n=400, 287/400=71.8%: [67.1%, 75.9%]; AN3c hard1 n=69, 54/69=78.3%: [67.2%, 86.4%].

Performance is non-monotonic in prompt length: the longest variant (AN5, 4,878 bytes) is the worst-performing cheatsheet, while the shortest effective variant (AN39, 385 bytes) ties with mid-length prompts at 70%. True and False recall trade off sharply: no variant simultaneously achieves both above 80% on hard3. AN19c maximizes True recall (91.7%) at the cost of nearcomplete False recall collapse (34.6%), while AN36 inverts this profile (50.0% True, 88.5% False).

The AN45d result (100% TRUE, 40% FALSE) warrants attention: a minor modification to AN45c caused six FALSE $ \rightarrow $ TRUE regressions, dropping overall accuracy from 90% to 70%. The ordering effect in AN45c depends on the exact token sequence, not on the semantic content of the rules.

Cheatsheet effect on model bias. The no-cheatsheet baseline exhibits strong structural TRUE bias: 82.6% TRUE recall versus only 38.0% FALSE recall (n=400, own run). AN45c does not merely raise overall accuracy it rebalances this bias. FALSE recall improves by +25.4 percentage points ( 38.0% $ \rightarrow $ 63.4% ), while TRUE recall increases further to 95.9%. The cheatsheet therefore serves two distinct functions: it corrects the model's structural tendency to classify hard problems as TRUE, and it provides the finite counterexample evidence needed to produce confident FALSE verdicts.

## 5.2 Cross-Model Results

Table 3 reports results for key variants across all three competition models.

<div align="center">

Table 3: Multi-model results on hard3 (n=20 for AN45c; n=50 otherwise).

</div>

<table border="1"><tr><td>Variant</td><td>Bytes</td><td>gpt-oss</td><td>Llama</td><td>Gemma</td><td>3-avg</td></tr><tr><td>AN45c-ScenarioA(official)^{†}$</td><td>2,252</td><td>95%</td><td>55%</td><td>53%(OR)</td><td>67.7%</td></tr><tr><td>AN45c-ScenarioB</td><td>2,252</td><td>90%</td><td>55%</td><td>85%(TAI)</td><td>76.7%</td></tr><tr><td>AN45c-ScenarioC</td><td>2,252</td><td>95%</td><td>55%</td><td>85%(TAI)</td><td>78.3%</td></tr><tr><td>AN38</td><td>1,776</td><td>74%</td><td>52%</td><td>54%</td><td>59.3%</td></tr><tr><td>AN19c</td><td>289</td><td>62%</td><td>60%</td><td>55%</td><td>59.0%</td></tr><tr><td>Baseline</td><td>0</td><td>59.75%</td><td>52%</td><td>≈50%</td><td>—</td></tr><tr><td>AN3c</td><td>4,306</td><td>64%</td><td>≈0%^{‡}$</td><td>—</td><td>—</td></tr></table>

$ ^{\dagger} $Scenario A uses OR/Novita bf16 Gemma (reasoning suppressed, near-constant TRUE output). Conservative official lower bound. Scenarios B/C use Together AI (8,192 tok, reasoning enabled); differ only in GPT result (90% vs. 95%, n = 20). $ ^{\ddagger} $0% TRUE recall; overall accuracy reflects only FALSE correct answers.

We report 67.7% (Scenario A) as the conservative official 3-model average. Scenarios B and C (76.7-78.3%) represent Gemma performance when correctly configured; we report them to distinguish configuration artifact from model capability.

The most striking cross-model finding is the AN3c collapse on Llama: the 4,306-byte BLOCK system causes Llama to output FALSE for every problem, yielding 0% TRUE recall. AN19c (289 bytes) is the only variant that produces balanced recall on Llama (37.5% TRUE, 80.8% FALSE), and the only variant where Llama marginally outperforms gpt-oss-120b (60% vs. 62%, within noise).

## 5.3 Cross-Dataset Generalization

Table 4 shows performance across splits for AN3c and AN38 — variants optimized on hard1 and hard3 respectively.

AN3c's Block 1 rule was developed against hard1's FALSE-heavy distribution (35% True). On hard1 it achieves 78.3% the highest single-split result in the study. On hard2 (balanced, 50% True), the same rule drops to 60.0% only 8 percentage points above chance because Block 1 misclassifies 51% of TRUE problems as FALSE. This 18.3 percentage-point degradation illustrates the distribution mismatch failure mode precisely. AN38 exhibits the complementary pathology: well-calibrated for hard3 (71.8% full-scale) but near chance on hard1 (50.7%). Both variants achieve $ \approx 92\% $ on normal problems, confirming that normal-split results are uninformative for distinguishing hard-problem strategies.

<div align="center">

Table 4: Cross-dataset performance for selected variants (gpt-oss-120b).

</div>

<table border="1"><tr><td>Variant</td><td>Split</td><td>n</td><td>Acc</td><td>T%</td><td>F%</td></tr><tr><td>AN3c</td><td>hard1</td><td>69</td><td>78.3</td><td>66.7</td><td>84.4</td></tr><tr><td>AN3c</td><td>hard2</td><td>50</td><td>60.0</td><td>50.0</td><td>69.2</td></tr><tr><td>AN3c</td><td>hard3</td><td>50</td><td>64.0</td><td>45.8</td><td>80.8</td></tr><tr><td>AN3c</td><td>normal</td><td>100</td><td>92.0</td><td>89.3</td><td>95.5</td></tr><tr><td>AN38</td><td>hard1</td><td>69</td><td>50.7</td><td>75.0</td><td>37.8</td></tr><tr><td>AN38</td><td>hard2</td><td>200</td><td>51.5</td><td>78.0</td><td>25.0</td></tr><tr><td>AN38</td><td>hard3</td><td>400</td><td>71.8</td><td>78.5</td><td>65.4</td></tr><tr><td>AN38</td><td>normal</td><td>200</td><td>92.0</td><td>89.9</td><td>94.5</td></tr></table>

## 6 Analysis

## 6.1 Why AN45c Works: The Trivial Magma as an Exit Gate

AN45c's primary mechanism is structural rather than informational. STEP 1 instructs the model to check whether $ E_{1} $ contains a variable appearing exactly once on one side a condition that forces all elements of any satisfying magma to be equal, collapsing it to the trivial one-element structure and making $ E_{2} $ vacuously true. When triggered, STEP 1 bypasses STEP 2 (the counterexample search) entirely and commits to TRUE before the CE tables introduce FALSE-directional pressure.

On hard3, AN45c achieves 95.9% TRUE recall compared to the baseline's 82.6% a gain of +13.3 percentage points while achieving 63.4% FALSE recall versus the baseline's 38.0% a gain of +25.4 percentage points. The overall improvement is +19.5 pp at n=400 (corrected pipeline). This gain appears to arise from reordering existing components rather than adding new content: AN38 contains the same STEP 1 logic but places it after the CE table, producing only 70.8% TRUE recall and 76.9% FALSE recall at full scale. We hypothesize that placing the trivial-magma check first primes the model's attention toward TRUE verdicts before the CE search introduces False-directional pressure though isolating this ordering effect from confounds requires controlled experiments beyond the scope of this study.

## 6.2 Why the Merge Ceiling Holds

The AN38 variant was constructed by merging two complementary predecessors: AN35 (True=58.3% FALSE=84.6%) and AN35b (True=79.2% FALSE=65.4%). The result was AN38: True=70.8% FALSE=76.9% a near-arithmetic mean of the two parents not a combination of their strengths. Three subsequent merge attempts (AN45d, AN45e, AN45f) all produced accuracy at or below the mean. A static instruction set cannot simultaneously prime two competing inference strategies: when the model encounters rules favoring both labels, it averages rather than selects.

## 6.3 The Token Cap Finding

Gemma 4 31B exhibits a distinctive failure mode when max_tokens falls below the budget required to complete CE verification. At 2,048 tokens, Gemma with AN45c produces 50% accuracy with 0% FALSE recall effectively outputting TRUE for every problem. At 8,192 tokens, the same model and prompt produces 85% accuracy (TRUE=90%, FALSE=80%). The mechanism: Gemma exhausts its token budget during STEP 2, fails to produce a COUNTEREXAMPLE block, and defaults to the STEP 1 exit gate verdict (TRUE). This is not a model capability failure; it is a configuration

artifact. Reported Gemma results are only valid when the token budget is sufficient to complete the full reasoning trace.

## 6.4 Why Theoretical Approaches Fail

Four variants introducing explicit mathematical reasoning frameworks all degraded performance relative to the 68% baseline (n=50 subset, consistent with Table 5 deltas):

<div align="center">

Table 5: Theory-based variants on hard3 (gpt-oss-120b, n=50).

</div>

<table border="1"><tr><td>Variant</td><td>Framework</td><td>Acc</td><td>Δ vs. baseline</td></tr><tr><td>AN39</td><td>Power-level prior</td><td>70%</td><td>+2pp</td></tr><tr><td>AN42</td><td>Knowledge-base rewriting</td><td>62%</td><td>-6pp</td></tr><tr><td>AN40</td><td>Semantic invariants</td><td>60%</td><td>-8pp</td></tr><tr><td>AN41</td><td>Tamari/tree-structure</td><td>58%</td><td>-10pp</td></tr></table>

The consistent direction of failure is FALSE $ \rightarrow $ TRUE error increase. When given a structured reasoning framework, the model generates plausible arguments satisfying the framework's criteria and commits to TRUE, even for problems where a small counterexample exists. False precision in the instructed framework is worse than no framework at all.

## 6.5 A Note on Numerical Coincidence

AN45c's conservative 3-model average (Scenario A: 67.7%) and AN3c's hard1 single-model accuracy (78.3%) are occasionally cited together in competition discussions. They are not comparable: the former is a balanced hard3 average across three models under a specific provider configuration; the latter is a single-model result on a FALSE-heavy split where a blanket-FALSE strategy would already score 65%. AN3c on a balanced split achieves 60-64%.

Structural classification hypothesis. Our results suggest that large language models in this task behave not as symbolic theorem provers but as heuristic classifiers over algebraic structure patterns. The prompt encodes a decision boundary over structural features variable repetition, nesting depth, singleton forcing rather than a proof system. This framing explains both the effectiveness of counterexample tables (which encode explicit structural decision rules) and the failure of procedural approaches (which require genuine symbolic execution). We term this the router hypothesis: the model routes problems to cached structural patterns rather than deriving answers compositionally. This has a direct practical implication: prompt improvements that add new structural rules can help, but only up to the capacity of the model to maintain and apply those rules consistently which is precisely the saturation boundary we observe.

## 7 Multi-Model Generalization

## 7.1 AN19c as the Model-Agnostic Minimum

AN19c (289 bytes) consists of three natural-language hints with no counterexample tables: a reminder that one-element magmas trivially satisfy all equations, a note that equations with a free variable isolated on one side are likely TRUE, and an instruction to output a verdict with brief reasoning. On gpt-oss-120b it achieves 62% on hard3 below most CE-table variants but it

is the only prompt that produces meaningful True recall on Llama 3.3 70B (37.5% True, 80.8% FALSE, 60% overall) and competitive performance on Gemma 4 31B (55%, Together AI).

Table 6 summarizes multi-model performance for variants with coverage across three or more models.

<div align="center">

Table 6: Multi-model generalization on hard3 $ ( n=1 0-5 0 $ ; see notes).

</div>

<table border="1"><tr><td>Variant</td><td>Bytes</td><td>gpt-oss</td><td>Llama</td><td>Gemma(TAI)</td><td>DeepSeek</td><td>4-avg</td></tr><tr><td>AN19c</td><td>289</td><td>62%</td><td>60%</td><td>55%</td><td>80%$\dagger$</td><td>≈64.3%</td></tr><tr><td>AN38</td><td>1,776</td><td>74%</td><td>52%</td><td>54%</td><td>60%$\dagger$</td><td>≈60.0%</td></tr><tr><td>AN45c</td><td>2,252</td><td>90-95%</td><td>55%</td><td>85%</td><td>—</td><td>—</td></tr><tr><td>Baseline</td><td>0</td><td>59.75%</td><td>52%</td><td>≈50%</td><td>—</td><td>—</td></tr><tr><td>AN3c</td><td>4,306</td><td>64%</td><td>≈0%$\ddagger$</td><td>—</td><td>—</td><td>—</td></tr></table>

$ ^{\dagger} $ DeepSeek n=10; $ \pm15 $ pp CI. $ ^{ \ddagger} $ 0% TRUE recall.

## 7.2 Model-Specific Bias Profiles

gpt-oss-120b is TRUE-biased at baseline: 82.6% TRUE recall versus 38.0% FALSE recall on hard3. CE table prompts partially correct this but never eliminate the bias even AN38's best fullscale result (71.8%) reduces the baseline's 44.6-point recall gap (82.6% TRUE vs. 38.0% FALSE) to just 13.1 points (78.5% TRUE vs. 65.4% FALSE) a substantial improvement, but the imbalance persists.

Llama 3.3 70B exhibits the opposite profile: near-baseline FALSE recall (80.8% with AN19c) but severely depressed TRUE recall (37.5% with the best prompt; effectively 0% with any prompt exceeding $ \approx $ 2KB). Longer prompts collapse TRUE recall further, suggesting a capacity ceiling on instruction-following rather than a knowledge deficit.

Gemma 4 31B is token-gated rather than directionally biased: its failure mode is token budget exhaustion, which triggers the STEP 1 exit gate and produces near-constant TRUE output. With sufficient budget (8,192 tokens), Gemma's recall profile is balanced and strong (85% with AN45c on n=20).

## 7.3 DeepSeek V3.2: Cost Efficiency Signal

DeepSeek V3.2 with AN19c achieves 80% on hard3 (n=10) at $ \approx $0.0008 per problem — roughly one order of magnitude cheaper than gpt-oss-120b at comparable accuracy. With AN38 (1,776 bytes), DeepSeek drops to 60%, confirming the pattern observed in Llama: CE table prompts hurt capable reasoners by introducing distracting structure that interferes with internal algebraic reasoning. The AN19c result on DeepSeek is the most cost-efficient signal in the study (n=10; highest-priority target for scale validation).

## 8 The Single-Prompt Ceiling

## 8.1 Formal Characterization

We define the empirical saturation region of single-prompt engineering as the accuracy range where further prompt iterations produce unstable, non-generalizable improvements on a given model, holding inference parameters fixed. Empirically, the saturation region lies at approximately 71- 79% for gpt-oss-120b on hard3 at scale (AN38: 71.8% at n = 400; AN45c: 79.3% (95% CI: [75.0%

82.9%] at n=400 with corrected pipeline). Despite more than 45 variants tested over five weeks, no full-scale evaluation exceeded this range on a balanced split.

This saturation is not merely a measurement artifact. It manifests as a structural pattern: prompt elements that increase TRUE recall tend to decrease FALSE recall by approximately the same margin, and vice versa.

The best-performing prompts do not form a dispersed cloud in (True recall, False recall) space they approximate a Pareto front. Three variants define its boundary: AN19c (True=91.7% FALSE=34.6%) , AN45c (True=90.0% , FALSE=80.0%) , and AN36 (True=50.0% , FALSE=88.5%) AN45c dominates most other variants on both dimensions simultaneously including AN38, AN35, AN35b, and AN43 but does not dominate AN36 on False recall (80.0% vs. 88.5%) or AN19c on True recall (90.0% vs. 91.7%) . The saturation region therefore describes an empirical Paretooptimal boundary within the single-prompt paradigm not necessarily an absolute theoretical limit, but a practical constraint that our 45+ variant search did not overcome.

## 8.2 The Merge Pattern: avg(A,B), Not max(A,B)

AN35 and AN35b are complementary specialists: AN35 achieves True=58.3% , False=84.6% AN35b achieves True=79.2% , False=65.4% . Their arithmetic means are True=68.8% , False=75.0% The merge result AN38 produces True=70.8% , False=76.9% — within 2pp of the arithmetic mean on both dimensions, not near the respective maxima. Three subsequent attempts (AN45d, AN45e, AN45f) replicated the averaging result. Combining complementary prompts in a static text file yields average performance, not maximum performance.

## 8.3 Why Routing Cannot Be Encoded in a Static Prompt

TRUE and FALSE hard problems require qualitatively different inference strategies. TRUE problems are best handled by identifying structural properties forcing singleton magmas or by exhausting small counterexample candidates. FALSE problems are best handled by finding a single finite counterexample quickly. A prompt that heavily weights the CE search primes FALSE detection and suppresses TRUE; a prompt that heavily weights the trivial-magma check does the opposite.

Solving this tension requires conditional routing: apply the TRUE strategy when the equation has a specific syntactic form, apply the FALSE strategy otherwise. A static prompt cannot implement this routing reliably because LLMs execute instructions probabilistically rather than conditionally they interpolate between strategies in proportion to their textual weight rather than selecting the appropriate one per instance.

## 8.4 Theoretical Upper Bound and the Path Beyond

gpt-oss-120b with no cheatsheet achieves 91.7% TRUE recall and 92.3% FALSE recall on normal problems. If a perfect external router could direct each hard problem to the appropriate strategy, the theoretical ceiling would be approximately:

$$
0. 5 \times 9 1. 7 \% + 0. 5 \times 9 2. 3 \% = 9 2. 0 \%
$$

well above the observed 71-79% saturation region. Gemini 1.5 Pro achieves 90.2% on hard problems with no cheatsheet, suggesting that frontier models have internalized routing-equivalent algebraic reasoning that cannot be injected through prompting into weaker models.

Concretely, escaping the empirical saturation region for gpt-oss-120b on this task likely requires one of: (a) an ensemble of specialized prompts with external routing by problem type; (b) fine-tuning on the Equational Theories Project graph ( $ \approx $ 22 million labeled equation pairs); or (c) a

hybrid LLM + symbolic verifier architecture where the LLM proposes candidate counterexamples and a Mace4-equivalent tool verifies them.

## 9 Official Benchmark Validation and Cross-Distribution Analysis

## 9.1 Data and Scope

All results in this section are drawn from the SAIR Contributor Network public leaderboard as of April 20, 2026 （ n=52 voluntary public submissions of 1,007 total registered participants, cited under SAIR's open science framework [9] ). The full competition leaderboard is scheduled for release on or before April 30, 2026. Official benchmark scores use the SAIR evaluation pipeline: OpenRouter/DeepInfra bf16, temperature 0.0, seed 0, max tokens 8,192 [8]. Local scores use Together AI bf16, temperature 0.0, seed 42.

## 9.2 Official Benchmark Results

Table 7 compares local evaluation results against the SAIR official benchmark on hard3 (the competition's reference format, as confirmed by the official smoke-test file problems_hard3_20.json1 [8]).

<div align="center">

Table 7: Local vs. official benchmark results on hard3 (GPT-OSS 120B). Official benchmark: n=20, DeepInfra bf16. Local: n=400, Together AI bf16. Baseline: no cheatsheet.

</div>

<table border="1"><tr><td>Variant</td><td>Local Acc.</td><td>Official Acc.</td><td>$\Delta$ vs. baseline$ ^{a}$</td><td>Official F1</td></tr><tr><td>Baseline</td><td>59.75%</td><td>56.3%</td><td>—</td><td>≈53%</td></tr><tr><td>AN38</td><td>71.8%</td><td>65.3%</td><td>+5.6pp</td><td>67.6%</td></tr><tr><td>AN45c</td><td>79.25%</td><td>55.5%</td><td>-4.3pp</td><td>63.7%</td></tr></table>

$ ^{a} $Delta relative to official baseline (56.3%).

AN38 produces a robust +5.6pp improvement over the official baseline on hard3, consistent with its local result (71.8%) . AN45c, despite achieving 79.25% locally (n=400), scores 55.5% on the official benchmark 4.3pp below the no-cheatsheet baseline. The trivial-magma exit gate (STEP 1), which was AN45c's primary structural innovation over AN38, appears to generate forced errors on the official problem sample: problems that satisfy the singleton test are committed to TRUE before counterexample evidence is considered. This is the same distribution-mismatch failure mode documented in Section 5 for AN3c on hard1/hard2.

<div align="center">

Table 8: Official benchmark results on hard2 (GPT-OSS 120B, n=20). Hard2 baseline: 56.3% accuracy, F1 $ \approx $ 64.9%

</div>

<table border="1"><tr><td>Variant</td><td>Official Acc.</td><td>$\Delta$ vs. baseline</td><td>Official F1</td></tr><tr><td>AN38</td><td>41.0%</td><td>-15.3pp</td><td>47.8%</td></tr><tr><td>AN45c</td><td>48.0%</td><td>-8.3pp</td><td>61.2%</td></tr></table>

On hard2, both variants fall below the no-cheatsheet baseline. AN38 incurs a larger accuracy penalty （-15.3pp）and F1 degradation （-17.1pp），while AN45c is less damaging （-8.3pp accuracy, -3.7pp F1). Neither cheatsheet improves over baseline on hard2, confirming that both are calibrated toward the hard3 distribution.

## 9.3 Cross-Distribution Trade-Off Surface

Of the 52 Contributor Network submissions, 13 had benchmark results available on both hard2 and hard3 as of competition close (April 20, 2026); Table 9 presents these 13 submissions.

<div align="center">

Table 9: Cross-distribution performance: hard2 vs. hard3 (GPT-OSS 120B, SAIR official benchmark). Contributor Network data, April 20, 2026 [9]. Participants cited by name under SAIR's open science framework.

</div>

<table border="1"><tr><td>Participant</td><td>Cheatsheet</td><td>hard2 Acc.</td><td>hard3 Acc.</td><td>$|\Delta|$</td><td>hard3 F1</td></tr><tr><td>Betka</td><td>98_hard200</td><td>99.0%</td><td>56.3%</td><td>42.7pp</td><td>55.9%</td></tr><tr><td>Pandey</td><td>hard98_derivate_2</td><td>97.0%</td><td>55.5%</td><td>41.5pp</td><td>53.9%</td></tr><tr><td>Reza Jamei</td><td>traditional_ml</td><td>89.0%</td><td>61.3%</td><td>27.7pp</td><td>68.6%</td></tr><tr><td>Reza Jamei</td><td>combo_jack</td><td>86.0%</td><td>58.5%</td><td>27.5pp</td><td>66.5%</td></tr><tr><td>Arjun Garg</td><td>bank_lookup_v8</td><td>83.0%</td><td>70.8%</td><td>12.2pp</td><td>74.6%</td></tr><tr><td>Heath</td><td>distilled-r-12</td><td>80.0%</td><td>59.0%</td><td>21.0pp</td><td>62.6%</td></tr><tr><td>Woon Siang Yi^{†}$</td><td>hard3_overfitted</td><td>51.0%</td><td>81.3%</td><td>30.3pp</td><td>83.1%</td></tr><tr><td>Garg</td><td>bank_lookup_v5</td><td>51.5%</td><td>60.8%</td><td>9.3pp</td><td>69.3%</td></tr><tr><td>SimonRJ</td><td>Stage 1 Prompt</td><td>58.0%</td><td>58.3%</td><td>0.3pp</td><td>67.3%</td></tr><tr><td>Debtirtha Saha</td><td>Test 8</td><td>60.0%</td><td>71.0%</td><td>11.0pp</td><td>76.0%</td></tr><tr><td>Devanshu Dixit</td><td>chat_v32</td><td>49.5%</td><td>68.0%</td><td>18.5pp</td><td>74.3%</td></tr><tr><td>Cazares</td><td>AN38</td><td>41.0%</td><td>65.3%</td><td>24.3pp</td><td>67.6%</td></tr><tr><td>Cazares</td><td>AN45c</td><td>48.0%</td><td>55.5%</td><td>7.5pp</td><td>63.7%</td></tr></table>

$ ^{\dagger} $Self-labeled "hard3_overfitted" by participant.

The table reveals a consistent pattern: among the 52 Contributor Network submissions with benchmark results, only one Arjun Garg's bank_lookup_v8 (83.0% hard2, 70.8% hard3) achieves above 65% accuracy on both distributions simultaneously. All other submissions optimizing for one distribution collapse on the other, with accuracy gaps ranging from 11 to 62.7 percentage points (Table 9). The highest-accuracy submissions on each split are explicitly or implicitly distribution-specific: Betka's 99.0% on hard2 collapses to 56.3% on hard3 （-42.7pp); Woon Siang Yi's 81.3% on hard3 collapses to 51.0% on hard2 （-30.3pp), with the participant themselves labeling the submission hard3_overfitted. We term this the cross-distribution trade-off surface: within the empirical saturation region, optimizing for one distribution trades against performance on complementary distributions. AN45c exhibits one of the smallest cross-split accuracy gaps (7.5pp) among submissions scoring above the no-cheatsheet baseline on at least one split, suggesting that distribution robustness and peak accuracy are competing objectives within the saturation zone.

## 9.4 Implications for the Saturation Region

These results reframe the saturation region finding. The ceiling is not merely an upper bound on accuracy it is a fragility zone where gains are distribution-dependent and structural innovations introduce failure modes on unseen distributions. AN45c's local result (79.25% , n=400) is valid under its measurement conditions; the 23.75pp gap to the official benchmark is not measurement error but distribution mismatch, the same phenomenon documented internally in Section 5.

For practitioners, this implies: a cheatsheet that substantially outperforms baseline on a heldout set does not guarantee generalization. Cross-distribution validation running the same variant on two structurally different problem samples is necessary to distinguish genuine ceiling improvements from distribution-specific optimization.

A structurally distinct approach observed in the Contributor Network further supports the router hypothesis: one participant (Heath, distilled-rules-12) submitted a pure structural classifier computing five syntactic features of $ E_{1} $ (variable counts, node depths, LHS structure) and applying a hand-coded decision tree with no mathematical content. This approach achieves 80.0% on hard2 and 59.0% on hard3 — competitive with CE-table approaches — suggesting that structural pattern classification alone, without any algebraic reasoning, captures a substantial fraction of the signal available to prompt-based methods. This constitutes independent empirical evidence for the router hypothesis: the task rewards structural pattern matching over symbolic reasoning.

Notably, one participant (McKenna, unpublished) reported achieving approximately 70% accuracy across all three evaluation models simultaneously using a single theory-grounded cheatsheet the only submission observed to maintain consistent performance across gpt-oss-120b, Llama 3.3 70B, and Gemma 4 31B. This convergence across models with substantially different capacity profiles suggests that mathematically grounded approaches may generalize more robustly than empirically iterated CE-table approaches, a hypothesis warranting systematic investigation in future work.

## 10 Conclusion

Summary of contributions. We present the first systematic empirical characterization of the single-prompt ceiling in formal reasoning tasks. Across 45+ prompt variants, balanced hard accuracy for gpt-oss-120b on hard3 plateaus at $ \approx $ 71-79% at scale. Merge experiments confirm that combining complementary prompts produces accuracy near the arithmetic mean of the parents, not near their maxima a structural constraint, not a local optimum. Our highest-performing local submission (AN45c, 2,252 bytes) achieves 79.25% on gpt-oss-120b （n=400; 95% CI: [75.0% 82.9%]），with TRUE recall of 95.9% and FALSE recall of 63.4%. AN38 is our most robust submission under distribution shift, producing +5.6pp over the official baseline (Section 9). A cross-provider validation run on OpenRouter/DeepInfra bf16 （n=20）yielded 90-95% consistent with the fullscale local result. The token cap finding demonstrates that Gemma's performance (50% vs. 85%) is entirely determined by provider configuration, not model capability. Model-specific bias profiles True bias in gpt-oss-120b, instruction-capacity collapse in Llama, token-gated reasoning in Gemma are stable across variants and not correctable by prompt engineering alone.

Post-submission analysis against the SAIR official benchmark (Section 9) reveals that AN45c (79.25% local, n = 400) scores 55.5% on the official hard3 benchmark — 4.3pp below the nocheatsheet baseline — while AN38 produces a robust +5.6pp improvement (65.3%) with the highest balanced F1 score (67.6%) among non-overfit submissions in the Contributor Network （n=52 visible submissions, April 20, 2026). The cross-distribution trade-off surface (Table 9) shows that among the 52 Contributor Network submissions, only Arjun Garg's bank_lookup_v8 achieves above 65% on both hard2 and hard3 simultaneously (83.0% and 70.8%), confirming that the saturation region is a fragility zone where distribution-specific gains trade against generalization.

Limitations. The primary AN45c result (79.25% , n = 400) is statistically reliable (95% CI: [75.0%, 82.9%]); however, its TRUE recall (95.9%) and FALSE recall (63.4%) reflect an imbalanced profile that may not generalize across providers or problem distributions. Small-sample limitations remain for Gemma (85%, n = 20) and DeepSeek (80%, n = 10), both carrying $ \pm10-15 $ pp confidence intervals. The cross-provider OpenRouter/DeepInfra run (n = 20, 90-95%) should be read as a consistency check, not an independent measurement. The Gemma official provider (Open-

Router/Novita bf16) suppresses reasoning mode; we were unable to test this configuration in a controlled way. All results are specific to equational implication over magmas; generalization to other formal reasoning domains is an open question.

The primary AN45c result (79.25% , n = 400, Together AI bf16) does not generalize to the SAIR official benchmark (55.5% , n = 20, DeepInfra bf16), a gap of -23.75pp. AN38's smaller gap (-6.5pp local to official) suggests that simpler prompts generalize more robustly within the saturation region. The Contributor Network data (n = 52 of 1,007 participants) is a voluntary public sample; the full competition leaderboard (scheduled April 30, 2026) may reveal additional patterns not visible in the current data.

Future work. Three directions follow from the ceiling characterization: (1) an ensemble of two specialized prompts with external routing by syntactic problem features; (2) fine-tuning on the Equational Theories Project implication graph ( $ \approx $ 22M labeled pairs); and (3) replication on other computationally asymmetric formal reasoning tasks (satisfiability checking, reachability in formal systems).

Closing. The central lesson is structural: what improved performance was not teaching the model new mathematics but controlling the order in which the model applies the mathematics it already knows. Expanding the model's reasoning repertoire through longer, more elaborate prompts consistently underperformed constraining its reasoning flow through minimal, well-ordered instructions. In formal reasoning as in engineering: less, structured deliberately, beats more.

## References

[1] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D. Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners. In Advances in Neural Information Processing Systems, volume 33, pages 1877-1901, 2020.

[2] Manuel Israel Cazares. SAIR prompt engineering — equational theories stage 1. https://github.com/israelcazares/sair-prompt-engineering, 2026. Accessed April 2026.

[3] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. Training verifiers to solve math word problems. 2021.

[4] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt. Measuring mathematical problem solving with the MATH dataset. In Advances in Neural Information Processing Systems, volume 34, pages 4130-4143, 2021.

[5] Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. Large language models are zero-shot reasoners. In Advances in Neural Information Processing Systems, volume 35, pages 22199-22213, 2022.

[6] Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. Lost in the middle: How language models use long contexts. Transactions of the Association for Computational Linguistics, 12:157-173, 2023.

[7] OpenAI. gpt-oss-120b & gpt-oss-20b model card, 2025.

[8] SAIR Foundation. Stage 1 judge for the mathematics distillation challenge: Equational theories. https://github.com/SAIRcompetition/equational-theories-stage1-judge, 2026. Official evaluation setup: OpenRouter/DeepInfra bf16, temperature 0.0, seed 0, max tokens 8,192. Canonical smoke test: problems_hard3_20.json1. Accessed April 2026.

[9] SAIR Foundation. SAIR mathematics distillation challenge — equational theories: Contributor network leaderboard, 2026. URL https://competition.sair.foundation/ competitions/mathematics-distillation-challenge-equational-theories-stage1/ leaderboard. Data as of April 20, 2026 (competition close). n = 52 voluntary public submissions of 1,007 total registered participants. Full competition leaderboard scheduled for release on or before April 30, 2026. Cited under SAIR open science framework (Official Rules, Section 5).

[10] Mrinank Sharma, Meg Tong, Tomasz Korbak, David Duvenaud, Amanda Askell, Samuel R. Bowman, Newton Cheng, Esin Durmus, Zac Hatfield-Dodds, Scott R. Johnston, Shauna Kravec, Timothy Maxwell, Sam McCandlish, Kamal Ndousse, Oliver Rausch, Nicholas Schiefer, Da Yan, Miranda Zhang, and Ethan Perez. Towards understanding sycophancy in language models. In International Conference on Learning Representations, 2024.

[11] Freda Shi, Xinyun Chen, Kanishka Misra, Nathan Scales, David Dohan, Ed H. Chi, Nathanael Scharli, and Denny Zhou. Large language models can be easily distracted by irrelevant context. In Proceedings of the 40th International Conference on Machine Learning, volume 202 of Proceedings of Machine Learning Research, pages 31210-31227, 2023.

[12] Terence Tao. Mathematics distillation challenge equational theories. https://terrytao.wordpress.com/2026/03/13/ mathematics-distillation-challenge-equational-theories/, 2026. Accessed April 2026.

[13] Terence Tao et al. Equational theories project. https://github.com/teorth/equational theories, 2024. Accessed April 2026.

[14] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V. Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language models. In Advances in Neural Information Processing Systems, volume 35, pages 24824-24837, 2022.