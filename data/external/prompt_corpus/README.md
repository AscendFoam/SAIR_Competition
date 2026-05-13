# External Prompt Corpus

本目录用于存放第三方或外部公开 prompt corpus 的原始索引与来源信息。

当前约定：

- `raw_index.example.jsonl` 只提供示例记录，不代表真实 corpus 已完成收集。
- 若来源允许，可在后续新增 `raw_prompts/` 存放本地镜像的公开 prompt 文本。
- 若来源不允许直接存储原文，则只保留 provenance、hash、结构标签和摘要说明。

边界：

- 不在这里混入未公开私有 prompt。
- 不把社交媒体截图直接当作主统计语料。
- 任何 released final evaluation subsets 相关分析，都必须在报告里标注为 `post-release analysis`。
