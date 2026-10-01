[English](README.md) | **中文**

# Design Diagrams：专业结构图 Skill

一个以证据和领域模型为基础的制图 Skill，用于绘制业务关系图、数据流程图、
业务流程与状态图，以及系统架构图和 Agent Harness 架构图。

它将可编辑的 SVG 作为唯一源文件，同时输出高清 PNG，方便审阅、分享和用于
SVG 支持不稳定的工具。

**理念：** 先把领域对象、术语和关系说明白，再使用一致的视觉语言进行编码。
好看的图不能掩盖事实不确定、术语含混、箭头断开或信息过度拥挤。

## 你会得到什么

- 可编辑、可访问、包含语义分组与稳定 ID 的 SVG
- 与 SVG 比例一致、直接渲染的 2× 高清 PNG
- Source-grounded（基于证据）与 Conceptual（概念方案）两种模式
- 面向复杂主题的“总图 + 机制子图”结构
- 可复用的项目 Style DNA 工作流
- 稳定的术语、层级命名、颜色语义和连线语法
- SVG 静态校验与浏览器 PNG 渲染脚本
- 支持 `16:9`、`4:3`、`3:4` 和 `1:1` 画布

## 快速开始

提供资料并说明希望得到的图：

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

## 默认交付物

每张图都以一对文件交付：

```text
<name>.svg
<name>.preview.png
```

SVG 是权威、可编辑的源文件。PNG 必须直接从最终 SVG 以不低于目标展示尺寸
两倍的分辨率渲染，不能反过来把 PNG 当作编辑源。

复杂主题会拆成一组图，例如：

```text
system-overview.svg
system-overview.preview.png
agent-loop-detail.svg
agent-loop-detail.preview.png
session-lifecycle-detail.svg
session-lifecycle-detail.preview.png
```

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

默认不使用公式和动画。只有明确要求 HTML/React 交互版本时，才考虑 React Bits
等动效组件。

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

## 系统要求

- Python 3.10 或更高版本：运行 SVG 静态校验
- Node.js 18 或更高版本：运行渲染器
- Google Chrome、Chromium、Microsoft Edge 或 Brave：导出 PNG
- 推荐字体：Songti SC 或 SimSun、Times New Roman；公式可选 STIX Two Math 或 Cambria Math

校验与渲染脚本只使用 Python 和 Node.js 标准库。

## 安装

Skill 源目录当前位于：

```text
/Users/fly/code/design-diagrams
```

### Codex：本地符号链接（推荐）

符号链接可以让已安装 Skill 始终指向可编辑的源目录：

```bash
mkdir -p ~/.codex/skills
ln -s /Users/fly/code/design-diagrams ~/.codex/skills/design-diagrams
```

如果目标位置已经存在，这条命令会直接失败，不会覆盖原有内容。如果当前 Agent
能够直接从本地路径调用 Skill，则不需要安装。

### Claude Code：本地符号链接

如果 Claude Code 环境支持目录式 Skill：

```bash
mkdir -p ~/.claude/skills
ln -s /Users/fly/code/design-diagrams ~/.claude/skills/design-diagrams
```

### 复制安装

无法使用符号链接时，可以复制文件：

```bash
mkdir -p ~/.codex/skills/design-diagrams
rsync -a /Users/fly/code/design-diagrams/ ~/.codex/skills/design-diagrams/
```

复制安装会产生独立快照。以后修改源目录时，必须再次同步，已安装版本才会更新。

### 通过 Git 安装

当前本地源目录尚未关联 Git 仓库。Skill 发布后，将示例地址替换成实际仓库地址：

```bash
DIAGRAMS_REPOSITORY_URL="https://github.com/OWNER/design-diagrams.git"
git clone "$DIAGRAMS_REPOSITORY_URL" ~/.codex/skills/design-diagrams
```

## 更新

### 符号链接安装

不需要重新安装。只要修改或更新 `/Users/fly/code/design-diagrams`，Codex 通过符号
链接读取到的就是同一份文件。可以通过下面的命令确认链接目标：

```bash
readlink ~/.codex/skills/design-diagrams
```

### 复制安装

把最新源文件同步到已安装目录：

```bash
rsync -a /Users/fly/code/design-diagrams/ ~/.codex/skills/design-diagrams/
```

该命令会更新同名文件，但不会删除目标目录中的其他文件。

### Git 安装

如果已安装目录是一个 Git clone：

```bash
git -C ~/.codex/skills/design-diagrams pull --ff-only
```

`--ff-only` 会在本地与远程历史分叉时停止，避免意外创建合并提交。

### 安装或更新后验证

```bash
python3 ~/.codex/skills/design-diagrams/scripts/validate_svg.py \
  ~/.codex/skills/design-diagrams/assets/svg-style-template.svg --strict

node ~/.codex/skills/design-diagrams/scripts/render_svg.mjs \
  ~/.codex/skills/design-diagrams/assets/svg-style-template.svg \
  --scale 2 --output /tmp/design-diagrams-check.png
```

预期结果是 `PASS: 0 errors, 0 warning(s)`，并在
`/tmp/design-diagrams-check.png` 生成一张 `3200×1800` PNG。检查后可以删除该临时文件。

## 目录结构

```text
design-diagrams/
├── SKILL.md
├── CONTEXT.md
├── README.md
├── README.zh-CN.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── svg-style-template.svg
├── references/
│   ├── design-resources.md
│   ├── diagram-language.md
│   ├── style-dna.md
│   └── svg-production.md
└── scripts/
    ├── render_svg.mjs
    └── validate_svg.py
```

## 自定义方式

- 修改目标项目的 Style DNA，调整字体、信息密度、间距和视觉禁用项。
- 修改语义规格，定义当前主题的术语、证据状态、层级和关系类型。
- 可以从 [`assets/svg-style-template.svg`](assets/svg-style-template.svg) 开始，
  但交付前必须替换全部示例内容、ID、标题和描述。
- 每次对 SVG 做实质修改后，都要重新生成 PNG，不能继续使用旧预览。
