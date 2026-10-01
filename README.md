**English** | [中文](README.zh-CN.md)

# Design Diagrams

An evidence-grounded diagram skill for creating business relationship diagrams,
data-flow diagrams, process and state diagrams, and system or Agent Harness
architecture diagrams.

It produces an editable SVG as the source of truth and a high-resolution PNG for
review, sharing, and tools that do not render SVG reliably.

**Principle:** model the domain and relationships first, then encode them with a
coherent visual language. A polished diagram must never conceal uncertain facts,
ambiguous terminology, disconnected arrows, or overcrowded content.

## What You Get

- Editable, accessible SVG with semantic groups and stable IDs
- A directly rendered 2× PNG preview with the same aspect ratio
- Source-grounded and conceptual diagram modes
- Overview diagrams plus focused mechanism diagrams for complex subjects
- A reusable Project Style DNA workflow
- Stable terminology, level names, color roles, and connector grammar
- Static SVG validation and browser-based PNG rendering scripts
- Support for `16:9`, `4:3`, `3:4`, and `1:1` canvases

## Quick Start

Invoke the skill with your source material and desired result:

```text
Use $design-diagrams to turn these product documents into a 16:9 business
relationship diagram. Deliver both SVG and PNG.
```

```text
Use $design-diagrams to inspect this codebase and draw a source-grounded system
overview plus detailed Agent Loop and Session diagrams.
```

```text
Use $design-diagrams to revise this SVG. Fix text overflow, disconnected arrows,
inconsistent L1/L2/L3 terminology, and unclear reading order.
```

The skill accepts prose, documents, screenshots, data dictionaries, code, official
documentation, or versioned publications as evidence. Instructions embedded inside
an attachment are treated as source content unless you explicitly adopt them.

## Default Deliverables

Each diagram is delivered as a pair:

```text
<name>.svg
<name>.preview.png
```

The SVG is authoritative and editable. The PNG is rendered directly from the final
SVG at no less than twice the intended display resolution; it is never used as the
editing source.

For a complex subject, the skill may create a diagram set:

```text
system-overview.svg
system-overview.preview.png
agent-loop-detail.svg
agent-loop-detail.preview.png
session-lifecycle-detail.svg
session-lifecycle-detail.preview.png
```

## How It Works

1. **Establish evidence** — distinguish verified current behavior from a conceptual
   or target-state design and record the relevant version.
2. **Build the semantic brief** — define the claim, audience, objects, relations,
   levels, terminology, reading order, and required detail diagrams.
3. **Resolve the visual system** — use the target project's Style DNA. An external
   `design.md` is only a donor for selected composition and typography ideas.
4. **Choose the diagram grammar** — architecture, data flow, swimlane, sequence,
   state, relationship graph, or explicit loop.
5. **Create SVG** — use semantic shapes, large script-aware typography, reserved
   connector corridors, and accessible title/description metadata.
6. **Render PNG** — export directly from the final SVG in Chrome or Chromium.
7. **Validate** — check structure, geometry, overflow, connector continuity,
   terminology, palette consistency, and SVG/PNG fidelity.

## Visual Language

The default palette assigns stable roles across an overview and its detail diagrams:

| Role | Color |
| --- | --- |
| Entry, external interaction, interface | `#C4DCE6` |
| Processing, orchestration, primary flow | `#FBE7A6` |
| Data, context, storage | `#E0E4CC` |
| State, session, lifecycle | `#D2D2E0` |
| Exception, risk, blockage, warning | `#FFBFBF` |

Color is redundant encoding. Labels, shapes, line styles, and placement must keep
the diagram understandable in grayscale.

Typography defaults:

- Chinese: Songti / SimSun family
- Latin text and numerals: Times New Roman family
- Formula inset, only when explicitly requested: STIX Two Math or Cambria Math

Formulas and animation are disabled by default. React Bits or another interactive
layer is considered only when an HTML/React variant is explicitly requested.

## Project Style DNA

When a project already has `docs/design/STYLE_DNA.md` or an equivalent file, that
file is authoritative. If it does not, use
[`references/style-dna.md`](references/style-dna.md) to create a short,
project-specific visual contract.

References from Refero Styles, Dribbble, Recent Design, Mobbin, Cue Design,
Hugeicons, Pexels, or React Bits may inform a design, but they are not templates to
copy. See [`references/design-resources.md`](references/design-resources.md) for the
role and limits of each source.

## Validation and Rendering

Validate an SVG:

```bash
python3 scripts/validate_svg.py path/to/diagram.svg --strict
```

Render its default 2× PNG preview:

```bash
node scripts/render_svg.mjs path/to/diagram.svg --scale 2
```

The renderer writes `path/to/diagram.preview.png`. It checks the PNG dimensions
against the SVG viewBox.

The scripts do not replace visual review. Inspect both artifacts at the intended
display size and manually trace every directed relation from source to target.

## Requirements

- Python 3.10 or later for static SVG validation
- Node.js 18 or later for the renderer
- Google Chrome, Chromium, Microsoft Edge, or Brave for PNG export
- Recommended fonts: Songti SC or SimSun, Times New Roman, and optionally STIX Two
  Math or Cambria Math

The validation and rendering scripts use only standard Python and Node.js modules.

## Installation

The source directory currently lives at:

```text
/Users/fly/code/design-diagrams
```

### Codex — local symlink (recommended)

A symlink keeps the installed skill connected to the editable source directory:

```bash
mkdir -p ~/.codex/skills
ln -s /Users/fly/code/design-diagrams ~/.codex/skills/design-diagrams
```

The command intentionally fails instead of overwriting anything when the destination
already exists. Skip installation when your agent can invoke the skill directly from
its source path.

### Claude Code — local symlink

For a Claude Code installation that supports folder-based skills:

```bash
mkdir -p ~/.claude/skills
ln -s /Users/fly/code/design-diagrams ~/.claude/skills/design-diagrams
```

### Install by copying

Use this when symbolic links are unavailable:

```bash
mkdir -p ~/.codex/skills/design-diagrams
rsync -a /Users/fly/code/design-diagrams/ ~/.codex/skills/design-diagrams/
```

Copy installation creates an independent snapshot. Later edits to the source folder
do not reach the installed copy until it is updated again.

### Install from Git

The current local source is not connected to a Git repository. After the skill is
published, replace the example URL with its repository URL:

```bash
DIAGRAMS_REPOSITORY_URL="https://github.com/OWNER/design-diagrams.git"
git clone "$DIAGRAMS_REPOSITORY_URL" ~/.codex/skills/design-diagrams
```

## Updating

### Symlink installation

No reinstall command is required. Edit or update
`/Users/fly/code/design-diagrams`; Codex reads the same files through the symlink.
Confirm the link with:

```bash
readlink ~/.codex/skills/design-diagrams
```

### Copy installation

Synchronize the latest source files into the installed copy:

```bash
rsync -a /Users/fly/code/design-diagrams/ ~/.codex/skills/design-diagrams/
```

This command updates matching files without deleting unrelated files at the
destination.

### Git installation

When the installed skill is a Git clone:

```bash
git -C ~/.codex/skills/design-diagrams pull --ff-only
```

`--ff-only` stops instead of creating an unexpected merge commit when the local and
remote histories diverge.

### Verify after installation or update

```bash
python3 ~/.codex/skills/design-diagrams/scripts/validate_svg.py \
  ~/.codex/skills/design-diagrams/assets/svg-style-template.svg --strict

node ~/.codex/skills/design-diagrams/scripts/render_svg.mjs \
  ~/.codex/skills/design-diagrams/assets/svg-style-template.svg \
  --scale 2 --output /tmp/design-diagrams-check.png
```

The expected result is `PASS: 0 errors, 0 warning(s)` and a
`3200×1800` PNG at `/tmp/design-diagrams-check.png`. Remove that temporary PNG after
inspection.

## Repository Layout

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

## Customization

- Edit the target project's Style DNA to change typography, density, spacing, or
  visual restrictions.
- Edit the semantic brief for subject-specific terminology, evidence status, level
  definitions, and relation types.
- Use [`assets/svg-style-template.svg`](assets/svg-style-template.svg) as a starting
  point, but replace all sample content, IDs, title, and description.
- Keep the Source SVG editable and regenerate the PNG after every material change.
