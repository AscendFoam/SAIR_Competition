# sair_competition — SAIR 代数推理竞赛工程化实验框架

本包是 SAIR（Semantics Algebraic Implication Reasoning）数学蒸馏挑战赛（Stage 1）的核心工具库。竞赛任务为判断一个方程是否蕴含另一个方程，本框架将这一任务视为"知识压缩与提示词协议设计"的工程问题，提供从数据准备到实验分析的全流程工具链。

## 包结构

```
sair_competition/
├── __init__.py        # 包初始化，导出 REPO_ROOT
├── cli.py             # 命令行入口（20+ 个子命令）
├── paths.py           # 仓库路径常量
├── config/            # 环境变量与 API 配置管理
├── data/              # 数据模式、JSONL I/O、数据集准备与拆分
├── parse/             # 方程解析与变量规范化
├── features/          # 结构特征提取与家族标签系统
├── eval/              # 评估指标、基线预测器、输出解析、评估运行器
├── analysis/          # 错误分析、实验对比、离线规则资产管理
└── prompting/         # 提示词模板加载、渲染与方程注入
```

## 架构概览

```
                          ┌──────────────┐
                          │   cli.py     │
                          │  命令行入口   │
                          └──────┬───────┘
                                 │ 调度
         ┌───────────┬───────────┼───────────┬────────────┐
         ▼           ▼           ▼           ▼            ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐
    │  data   │ │  parse  │ │features │ │  eval   │ │prompting │
    │数据管理  │ │方程解析  │ │特征标签  │ │评估管线  │ │提示词组装 │
    └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └─────┬────┘
         │           │           │            │            │
         │           └─────┬─────┘            │            │
         │                 │ 被依赖            │            │
         └────────┬────────┘                  │            │
                  │                           │            │
                  ▼                           ▼            │
            ┌──────────────────────────────────┘            │
            │                                                │
            ▼                                                ▼
    ┌──────────────┐                                  ┌──────────┐
    │   analysis   │◄─────────────────────────────────│  config  │
    │ 错误分析/报告 │    (通过 eval 使用 config)         │ API 配置  │
    └──────────────┘                                  └──────────┘
```

## 路径常量 (`paths.py`)

| 常量 | 值 | 说明 |
| --- | --- | --- |
| `PACKAGE_ROOT` | `src/sair_competition/` | 包根目录 |
| `SRC_ROOT` | `src/` | 源码根目录 |
| `REPO_ROOT` | 项目根目录 | 仓库根目录（通过 `__init__.py` 导出） |

## CLI 命令一览 (`cli.py`)

通过 `python -m sair_competition.cli <command>` 调用。

### 基础工具

| 命令 | 说明 |
| --- | --- |
| `validate-layout` | 验证仓库目录结构完整性 |
| `show-error-taxonomy` | 显示 8 种错误分类定义 |
| `show-family-tag-taxonomy` | 显示 45 个家族标签定义 |
| `demo-metrics` | 打印示例指标对象（工具链健康检查） |
| `parse-output <text>` | 解析模型输出文本为布尔值 |

### 数据准备

| 命令 | 说明 |
| --- | --- |
| `prepare-public-data` | 标准化官方公开数据文件 |
| `make-splits` | 创建确定性分层拆分（smoke/dev/holdout/audit） |
| `tag-problem-families` | 为数据集标注家族标签 |

### 评估

| 命令 | 说明 |
| --- | --- |
| `run-baseline-eval` | 运行基线预测器评估 |
| `run-complete-prompt-eval` | 通过 API 运行完整 prompt 评估 |
| `build-complete-prompt` | 渲染完整 prompt 文件 |

### 分析

| 命令 | 说明 |
| --- | --- |
| `analyze-errors` | 分析预测错误并生成报告 |
| `compare-candidates` | 对比多个实验候选运行 |

### 家族标签与离线规则

| 命令 | 说明 |
| --- | --- |
| `attach-family-tags-to-predictions` | 将家族标签回填到预测文件 |
| `build-offline-rule-assets` | 从标注数据构建离线规则资产 |
| `attach-offline-rule-assets` | 将规则资产 ID 附加到数据行 |
| `audit-offline-rule-assets` | 审计规则资产在预测上的表现 |
| `consolidate-offline-rule-axes` | 合并重叠资产为规范轴 |
| `build-offline-rule-review-set` | 生成去重审查集和标注清单 |

## 典型工作流

```bash
# 1. 验证仓库结构
python -m sair_competition.cli validate-layout

# 2. 准备数据
python -m sair_competition.cli prepare-public-data

# 3. 创建拆分
python -m sair_competition.cli make-splits

# 4. 标注家族标签
python -m sair_competition.cli tag-problem-families --output-path data/interim/public_tagged.jsonl

# 5. 运行基线评估
python -m sair_competition.cli run-baseline-eval

# 6. 运行 prompt 评估
python -m sair_competition.cli run-complete-prompt-eval --prompt-path prompts/complete/P1.md

# 7. 分析错误
python -m sair_competition.cli analyze-errors --predictions-path artifacts/candidates/xxx/predictions.jsonl --output-dir artifacts/candidates/xxx_analysis

# 8. 对比候选
python -m sair_competition.cli compare-candidates --candidate-dir artifacts/candidates/A --candidate-dir artifacts/candidates/B --output-dir artifacts/comparisons/cmp1
```

## 各子模块详细文档

| 模块 | 文档 | 说明 |
| --- | --- | --- |
| `config/` | [config/README.md](config/README.md) | 环境变量与 API 配置 |
| `data/` | [data/README.md](data/README.md) | 数据模式与 I/O |
| `parse/` | [parse/README.md](parse/README.md) | 方程解析工具 |
| `features/` | [features/README.md](features/README.md) | 特征提取与家族标签 |
| `eval/` | [eval/README.md](eval/README.md) | 评估管线 |
| `analysis/` | [analysis/README.md](analysis/README.md) | 错误分析与离线规则 |
| `prompting/` | [prompting/README.md](prompting/README.md) | 提示词组装 |
