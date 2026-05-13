# Provenance Rules

状态：candidate-register hygiene v0，非 completed corpus policy。

## Source Type Definitions

- `local`: 本仓库内已经存在、可本地读取的 prompt 文件。
- `official`: 官方公开资源或官方正式发布的 prompt-related 材料。
- `github`: 公开 GitHub 仓库、gist 或其他可追溯代码托管来源。
- `paper`: 论文、报告、附录或文章中的 prompt 描述。
- `contributor_network`: 官方 Contributor Network 可见材料或与其等价的公开贡献页面。
- `social`: 社交媒体、截图、自述结果；只作为补充线索，不作为主统计来源。

## Storage Eligibility

- `local_text_available`: 仓库内已有本地文件，可登记 path、hash 和 byte size。
- `metadata_only`: 只登记来源、许可、归因、计划用途；不存原文。
- `structure_only`: 只登记结构标签、摘要、可见模块或 feature summary；不存原文。
- `excluded`: 当前不进入 candidate register 主体，只保留拒绝原因。

## Direct Recompute Eligibility

- `direct_recompute`: 本地文本已存在，或外部来源已经核验到可允许后续本地导入且无需再做 license 阻塞审查；但如果外部文本尚未导入，本轮仍可暂时保持 metadata-only。
- `needs_license_review`: 候选看起来有研究价值，但仍需完成 license、ToS 或 file-level provenance 审查后才能导入或重算。
- `structure_only`: 只允许做结构编码、taxonomy、归因或 related-work 对照，不进入直接重算。
- `exclude`: 当前不进入重算、结构分析或公开语料主体。

## Metadata-Only Conditions

满足任一条件时应使用 `metadata_only`：

- 原文可见，但当前没有明确许可支持本地镜像。
- 来源能定位，但 commit、作者、license 或发布边界仍未核验。
- 研究上值得保留来源线索，但不宜在仓库存储 prompt 原文。

## Structure-Only Conditions

满足任一条件时应使用 `structure_only`：

- 只能合法记录结构模块、prompt feature summary 或短摘录。
- 原文不可稳定追溯、不可合法镜像，或只在 contributor summary 中可见。
- 候选适合作为 taxonomy、motivation 或 reviewer objection 对照，但不适合作为直接重算对象。

## Public and Private Asset Boundary

- 不把未公开私有 prompt 混入 corpus。
- 不把 API raw outputs、`.env`、私有数据或 release-only 资产写入公开复现包。
- 本地已有 prompt 也必须保留 provenance、hash、路径和 release boundary 说明。
- 社交媒体或截图来源默认不进入主统计语料。

## Attribution Policy

- 每个 public candidate 至少保留 source ref、author or team、timestamp、license or ToS note。
- contributor-network 候选在任何结构复述前都要保留 attribution note。
- 若只做 structure-only 记录，也必须说明不存原文的原因。

## Post-Release Rules

- `released final evaluation subsets` 只能用于 `post-release analysis`。
- 它们不能用于 prompt selection reward，也不能作为赛时未知盲测叙事。
- `post_release_relation` 应明确区分 `pre_release_design`、`post_release_analysis_only` 和 `unknown`。

## Candidate Register v0 Scope

- candidate register v0 不是 completed corpus。
- 当前只登记第一批 `8-12` 个候选及其 provenance hygiene。
- 正式 corpus 清洗、去重、license audit 和外部来源核验留给 T04-T06。

## Git Tracking Strategy

- 当前采用 `.gitignore` 窄 allowlist，允许跟踪 `data/external/prompt_corpus/*.md`、`*.jsonl` 与 `data/interim/prompt_corpus/*.md`、`*.json`、`*.jsonl`。
- 该 allowlist 只覆盖 prompt corpus governance files，不放开 `data/raw/`、一般 `data/interim/` 产物或未来可能出现的 `raw_prompts/`。
- 如果后续新增外部原文镜像目录，应继续默认忽略，除非另开任务并明确许可边界。
