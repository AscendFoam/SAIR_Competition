# Research Configs

本目录存放 Stage1 后赛事实证科研用的机器可读配置模板。

当前只提供 seed / example 文件，不代表对应语料、taxonomy 或评测已经完成。

文件约定：

- `corpus_sources.example.json`: prompt corpus 来源登记模板。
- `prompt_feature_taxonomy.yaml`: prompt 结构特征 taxonomy v0 seed。
- `evaluation_matrix.example.json`: screening / recomputed benchmark / post-release analysis 评测矩阵模板。

使用原则：

- 所有后赛事实验必须显式标注 `post-release analysis`。
- 不把未公开 prompt、API raw outputs、私有数据或敏感配置写入公开复现模板。
- 任何新字段都应与 `docs/02_experiment_plan.md`、`docs/06_eval_protocol.md` 和 `docs/03_architecture.md` 保持一致。
