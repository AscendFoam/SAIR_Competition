# Interim Prompt Corpus

本目录用于存放 prompt corpus 的标准化中间产物。

当前阶段只包含 scaffold：

- `prompt_corpus_manifest.json`: corpus seed 状态与后续目标的机器可读说明。

后续预期文件：

- `corpus_v1.jsonl`
- `prompt_features_v1.jsonl`
- 其他审计或归一化中间文件

注意：

- manifest 必须如实描述当前 corpus 是否为空或仅为 seed。
- 不得把尚未收集的 prompt 伪写成已入库。
