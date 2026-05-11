# Statistical Analysis Reports

本目录用于记录 prompt 结构特征与性能、鲁棒性之间的统计分析。

当前状态：

- 尚未生成描述统计或检验结果。

后续建议覆盖：

- prompt length vs performance
- module order vs parse stability
- counterexample strategy vs true or false recall tradeoff
- model transfer gap
- robustness gap from public split to released subsets

要求：

- 所有统计结论必须能回溯到 prompt hash、split、model/provider config 和指标定义。
- 没有证据支撑的结论只能写为假设或待验证观察。
