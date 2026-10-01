[English](README.md) | **中文**

# Design Diagrams

**经得起审查的图，而不只是好看的图。**

一个面向 Claude Code、Codex 等 Agent 的、以证据和领域模型为基础的制图 Skill。
它把文档、源码、截图或文字描述变成业务关系图、数据流程图、业务流程与状态图，
以及系统架构图和 Agent Harness 架构图——交付可编辑的 SVG（唯一源文件）和用于
审阅、分享的高清 PNG。

**理念：** 先把领域对象、术语和关系说明白，再使用一致的视觉语言进行编码。
好看的图不能掩盖事实不确定、术语含混、箭头断开或信息过度拥挤。

## 你会得到什么

每张图都以一对文件交付——权威、可编辑的 SVG，以及直接从它渲染的 2× PNG：

```text
<name>.svg
<name>.preview.png
```

此外 Skill 还提供：

- 可编辑、可访问、包含语义分组与稳定 ID 的 SVG
- Source-grounded（基于证据）与 Conceptual（概念方案）两种模式
- 面向复杂主题的"总图 + 机制子图"结构
- 可复用的项目 Style DNA 工作流，保证同一项目视觉一致
- 稳定的术语、层级命名、颜色语义和连线语法
- 为有序流程和闭环连线提供连续的 `1、2、3、4…` 序号标识
- SVG 静态校验与浏览器 PNG 渲染脚本
- 支持 `16:9`、`4:3`、`3:4` 和 `1:1` 画布

复杂主题会拆成一组图，例如：

```text
system-overview.svg + .preview.png
agent-loop-detail.svg + .preview.png
session-lifecycle-detail.svg + .preview.png
```

## 快速开始

1. 安装 Skill（见[安装](#安装)）
2. 向 Agent 提供资料并说明希望得到的图：

```text
使用 $design-diagrams，把这些产品文档整理成一张 16:9 业务关系图，
同时交付 SVG 和 PNG。
```

```text
使用 $design-diagrams，检查这个代码库并绘制一张基于源码的系统总图，
再拆出 Agent Loop 和 Session 机制详图。
```

```text
使用 $design-diagrams 修改这张 SVG：修复文字溢出、箭头断开、
L1/L2/L3 术语不一致和阅读顺序不清晰的问题。
```

Skill 可以读取文字、文档、截图、数据字典、源码、官方文档和版本化出版资料。
附件内部出现的指令默认只是资料内容，除非你明确要求采用，否则不会把它当成用户命令。

## 工作原理

1. **确认证据**：区分已经验证的当前行为与概念方案或目标态，并记录对应版本。
2. **建立语义规格**：定义核心结论、读者、对象、关系、层级、术语、阅读顺序和子图范围。
3. **确定视觉系统**：优先采用目标项目的 Style DNA；外部 `design.md` 只是构图与排版的参考来源。
4. **选择图形语法**：架构图、数据流、泳道图、时序图、状态图、关系图或明确的循环图。
5. **生成 SVG**：使用语义形状、大字号分语言字体、预留连线路径，并添加可访问性元数据。
6. **渲染 PNG**：通过 Chrome 或 Chromium 直接从最终 SVG 导出。
7. **完成验收**：检查结构、几何、溢出、连线连续性、术语、颜色语义及 SVG/PNG 一致性。

## 视觉语言

默认颜色在总图与机制子图中保持稳定语义：

| 语义 | 色号 |
| --- | --- |
| 入口、外部交互、接口 | `#C4DCE6` |
| 处理、调度、主流程 | `#FBE7A6` |
| 数据、上下文、存储 | `#E0E4CC` |
| 状态、会话、生命周期 | `#D2D2E0` |
| 异常、风险、阻塞、警示 | `#FFBFBF` |

颜色只用于辅助编码。即使黑白打印，读者也应当能通过标题、形状、线型和位置
理解整张图。

默认字体：

- 中文：宋体、Songti SC 或 SimSun 字体族
- 英文与数字：Times New Roman 字体族
- 公式区域：仅在明确要求时使用 STIX Two Math 或 Cambria Math

默认不使用公式和动画。只有明确要求 HTML/React 交互版本时才会考虑。

## 项目 Style DNA

如果项目已经存在 `docs/design/STYLE_DNA.md` 或同类文件，以项目文件为准。
如果不存在，可根据 [`references/style-dna.md`](references/style-dna.md) 创建一份
简短、项目专属的视觉规范。

Refero Styles、Dribbble、Recent Design、Mobbin、Cue Design、Hugeicons、Pexels
和 React Bits 可以提供设计参考，但不能被当作直接照搬的模板。各资源的用途与边界见
[`references/design-resources.md`](references/design-resources.md)。

## 校验与渲染

校验 SVG：

```bash
python3 scripts/validate_svg.py path/to/diagram.svg --strict
```

生成默认的 2× PNG：

```bash
node scripts/render_svg.mjs path/to/diagram.svg --scale 2
```

渲染器默认输出 `path/to/diagram.preview.png`，并核对 PNG 像素尺寸是否与 SVG
的 viewBox 匹配。

脚本不能替代人工检查。需要在目标展示尺寸并排查看 SVG 与 PNG，并逐条从源节点
追踪到目标节点，确认所有有向关系都连续、清晰且没有歧义。

## 安装

### Claude Code

```bash
git clone https://github.com/FlyAIBox/design-diagrams.git ~/.claude/skills/design-diagrams
```

### Codex

```bash
git clone https://github.com/FlyAIBox/design-diagrams.git ~/.codex/skills/design-diagrams
```

### 本地开发

把仓库 clone 到任意位置，再用符号链接接入 Agent 的 skills 目录，
对工作副本的修改会立即生效：

```bash
git clone https://github.com/FlyAIBox/design-diagrams.git ~/code/design-diagrams
mkdir -p ~/.claude/skills
ln -s ~/code/design-diagrams ~/.claude/skills/design-diagrams
```

如果目标位置已经存在，`ln -s` 会直接失败而不会覆盖原有内容。如果当前 Agent
能够直接从本地路径调用 Skill，则不需要安装。

### 更新

```bash
git -C ~/.claude/skills/design-diagrams pull --ff-only
```

`--ff-only` 会在本地与远程历史分叉时停止，避免意外创建合并提交。
（Codex 安装请替换为对应路径。）

### 安装或更新后验证

```bash
SKILL_DIR=~/.claude/skills/design-diagrams

python3 "$SKILL_DIR/scripts/validate_svg.py" \
  "$SKILL_DIR/assets/svg-style-template.svg" --strict

node "$SKILL_DIR/scripts/render_svg.mjs" \
  "$SKILL_DIR/assets/svg-style-template.svg" \
  --scale 2 --output /tmp/design-diagrams-check.png
```

预期结果是 `PASS: 0 errors, 0 warning(s)`，并在
`/tmp/design-diagrams-check.png` 生成一张 `3200×1800` PNG。检查后可以删除该临时文件。

## 系统要求

- Python 3.10 或更高版本：运行 SVG 静态校验
- Node.js 18 或更高版本：运行渲染器
- Google Chrome、Chromium、Microsoft Edge 或 Brave：导出 PNG
- 推荐字体：Songti SC 或 SimSun、Times New Roman；公式可选 STIX Two Math 或 Cambria Math

校验与渲染脚本只使用 Python 和 Node.js 标准库——没有第三方依赖，也不需要任何 API Key。

## 目录结构

```text
design-diagrams/
├── SKILL.md                  # Agent 的 Skill 入口
├── CONTEXT.md                # 领域模型与术语
├── README.md / README.zh-CN.md
├── agents/
│   └── openai.yaml           # Codex Agent 清单
├── assets/
│   ├── ordered-flow-template.svg
│   └── svg-style-template.svg
├── references/
│   ├── design-resources.md   # 外部设计资源的用途与边界
│   ├── diagram-language.md   # 形状、连线、层级、颜色语义
│   ├── style-dna.md          # 项目 Style DNA 工作流
│   └── svg-production.md     # SVG 制作规范
└── scripts/
    ├── render_svg.mjs        # SVG → 2× PNG（Chrome/Chromium）
    └── validate_svg.py       # 静态结构校验
```

## 自定义方式

- 修改目标项目的 Style DNA，调整字体、信息密度、间距和视觉禁用项。
- 修改语义规格，定义当前主题的术语、证据状态、层级和关系类型。
- 可以从 [`assets/svg-style-template.svg`](assets/svg-style-template.svg) 开始，
  但交付前必须替换全部示例内容、ID、标题和描述。
- 有序流程或闭环需要在线路上显示 `1、2、3、4…` 时，使用
  [`assets/ordered-flow-template.svg`](assets/ordered-flow-template.svg)。
- 每次对 SVG 做实质修改后，都要重新生成 PNG，不能继续使用旧预览。
