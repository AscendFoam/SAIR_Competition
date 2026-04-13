# prompting — 提示词模板加载、渲染与组装

本模块负责将提示词模板文件和 cheatsheet 知识库文本组装为完整的 prompt，并将方程对注入到 prompt 中供模型评估使用。

## 文件清单

| 文件 | 职责 |
| --- | --- |
| `__init__.py` | 包初始化 |
| `compose.py` | 模板加载与变量替换 |
| `render.py` | 方程注入到完整 prompt |

## 核心 API

### `compose.py` — 模板组合

| 函数签名 | 说明 |
| --- | --- |
| `load_text(path: str \| Path) -> str` | 读取文本文件内容（UTF-8 编码） |
| `render_template(template_text: str, variables: dict[str, Any]) -> str` | 将模板中的 `{{ key }}` 或 `{{key}}` 占位符替换为对应值 |
| `build_complete_prompt(template_path, cheatsheet_path, variables) -> str` | 加载模板和 cheatsheet，将 cheatsheet 内容作为 `{{ cheatsheet }}` 变量注入模板，返回完整 prompt |

#### 模板占位符格式

```text
{{ cheatsheet }}    →  cheatsheet 文件内容
{{ equation1 }}     →  方程 1（由 render.py 注入）
{{ equation2 }}     →  方程 2（由 render.py 注入）
```

### `render.py` — 方程注入

| 函数签名 | 说明 |
| --- | --- |
| `render_complete_prompt_for_problem(complete_prompt_text, equation1, equation2) -> str` | 将方程对注入到已渲染的完整 prompt 中 |

#### 支持的占位符格式

为兼容多种模板风格，以下 8 种写法均会被替换：

```text
{{ equation1 }}   {{equation1}}   { equation1 }   {equation1}
{{ equation2 }}   {{equation2}}   { equation2 }   {equation2}
```

## 数据流

```
模板文件 (template.md)
    ↓  load_text
模板文本
    ↓  render_template (注入 cheatsheet)
完整 prompt 文本
    ↓  render_complete_prompt_for_problem (注入 equation1, equation2)
最终 prompt → 发送给模型
```

## 依赖关系

- **被依赖方**: `eval.local_runner`
- **无项目内依赖**，仅使用标准库 `pathlib`
