**English** | [中文](README.zh-CN.md)

# Design Diagrams

**Diagrams you can audit, not just admire.**

An evidence-grounded diagram skill for Claude Code, Codex, and similar agents. It
turns documents, code, screenshots, or prose into business relationship diagrams,
data-flow diagrams, process and state diagrams, and system or Agent Harness
architecture diagrams — delivered as an editable SVG (the source of truth) plus a
high-resolution PNG for review and sharing.

**Philosophy:** Model the domain and relationships first, then encode them with a
coherent visual language. A polished diagram must never conceal uncertain facts,
ambiguous terminology, disconnected arrows, or overcrowded content.

## What You Get

Every diagram is delivered as a pair — an authoritative, editable SVG and a 2×
PNG rendered directly from it:

```text
<name>.svg
<name>.preview.png
```

Along the way the skill gives you:

- Editable, accessible SVG with semantic groups and stable IDs
- Source-grounded (verified from evidence) and conceptual (target-state) modes
- Overview diagrams plus focused mechanism diagrams for complex subjects
- A reusable Project Style DNA workflow for consistent visuals across a project
- Stable terminology, level names, color roles, and connector grammar
- Numbered `1, 2, 3, 4…` connector badges for ordered processes and loops
- Static SVG validation and browser-based PNG rendering scripts
- Support for `16:9`, `4:3`, `3:4`, and `1:1` canvases

For a complex subject, the skill creates a diagram set:

```text
system-overview.svg + .preview.png
agent-loop-detail.svg + .preview.png
session-lifecycle-detail.svg + .preview.png
```

## Quick Start

1. Install the skill (see [Installation](#installation))
2. Hand your agent some source material and describe the diagram you want:

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
an attachment are treated as source content, not as commands, unless you explicitly
adopt them.

## How It Works

1. **Establish evidence** — distinguish verified current behavior from a conceptual
   or target-state design and record the relevant version.
2. **Build the semantic brief** — define the claim, audience, objects, relations,
   levels, terminology, reading order, and required detail diagrams.
3. **Resolve the visual system** — use the target project's Style DNA. An external
   `design.md` is only a donor for selected composition and typography ideas.
4. **Choose the diagram grammar** — architecture, data flow, swimlane, sequence,
   state, relationship graph, or explicit loop.
5. **Create SVG** — semantic shapes, large script-aware typography, reserved
   connector corridors, and accessible title/description metadata.
6. **Render PNG** — export directly from the final SVG in Chrome or Chromium.
7. **Validate** — structure, geometry, overflow, connector continuity, terminology,
   palette consistency, and SVG/PNG fidelity.

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

Formulas and animation are disabled by default. An interactive HTML/React variant
is considered only when explicitly requested.

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

The renderer writes `path/to/diagram.preview.png` and checks the PNG dimensions
against the SVG viewBox.

The scripts do not replace visual review. Inspect both artifacts at the intended
display size and manually trace every directed relation from source to target.

## Installation

### Claude Code

```bash
git clone https://github.com/FlyAIBox/design-diagrams.git ~/.claude/skills/design-diagrams
```

### Codex

```bash
git clone https://github.com/FlyAIBox/design-diagrams.git ~/.codex/skills/design-diagrams
```

### Developing the skill locally

Clone it anywhere you like and symlink it into your agent's skills directory, so
edits to the working copy are picked up immediately:

```bash
git clone https://github.com/FlyAIBox/design-diagrams.git ~/code/design-diagrams
mkdir -p ~/.claude/skills
ln -s ~/code/design-diagrams ~/.claude/skills/design-diagrams
```

`ln -s` intentionally fails instead of overwriting when the destination already
exists. Skip installation entirely when your agent can invoke the skill directly
from its source path.

### Updating

```bash
git -C ~/.claude/skills/design-diagrams pull --ff-only
```

`--ff-only` stops instead of creating an unexpected merge commit when the local and
remote histories diverge. (Use the matching path for a Codex installation.)

### Verify after installation or update

```bash
SKILL_DIR=~/.claude/skills/design-diagrams

python3 "$SKILL_DIR/scripts/validate_svg.py" \
  "$SKILL_DIR/assets/svg-style-template.svg" --strict

node "$SKILL_DIR/scripts/render_svg.mjs" \
  "$SKILL_DIR/assets/svg-style-template.svg" \
  --scale 2 --output /tmp/design-diagrams-check.png
```

The expected result is `PASS: 0 errors, 0 warning(s)` and a `3200×1800` PNG at
`/tmp/design-diagrams-check.png`. Remove that temporary PNG after inspection.

## Requirements

- Python 3.10 or later for static SVG validation
- Node.js 18 or later for the renderer
- Google Chrome, Chromium, Microsoft Edge, or Brave for PNG export
- Recommended fonts: Songti SC or SimSun, Times New Roman, and optionally STIX Two
  Math or Cambria Math

The validation and rendering scripts use only standard Python and Node.js modules —
no third-party dependencies, no API keys.

## Repository Layout

```text
design-diagrams/
├── SKILL.md                  # Skill entry point for the agent
├── CONTEXT.md                # Domain model and terminology
├── README.md / README.zh-CN.md
├── agents/
│   └── openai.yaml           # Codex agent manifest
├── assets/
│   ├── ordered-flow-template.svg
│   └── svg-style-template.svg
├── references/
│   ├── design-resources.md   # External design sources: roles and limits
│   ├── diagram-language.md   # Shapes, connectors, levels, color roles
│   ├── style-dna.md          # Project Style DNA workflow
│   └── svg-production.md     # SVG authoring rules
└── scripts/
    ├── render_svg.mjs        # SVG → 2× PNG via Chrome/Chromium
    └── validate_svg.py       # Static structural validation
```

## Customization

- Edit the target project's Style DNA to change typography, density, spacing, or
  visual restrictions.
- Edit the semantic brief for subject-specific terminology, evidence status, level
  definitions, and relation types.
- Use [`assets/svg-style-template.svg`](assets/svg-style-template.svg) as a starting
  point, but replace all sample content, IDs, title, and description.
- Use [`assets/ordered-flow-template.svg`](assets/ordered-flow-template.svg) when a
  process or loop needs connector-level `1, 2, 3, 4…` ordering.
- Keep the source SVG editable and regenerate the PNG after every material change.
