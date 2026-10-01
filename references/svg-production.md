# SVG and PNG Production

Read this reference before creating or substantially revising a Source SVG.

## Canvas Profiles

Use a stable viewBox and export the PNG Preview directly from it.

| Profile | Recommended viewBox | 2× PNG |
| --- | --- | --- |
| 16:9 | `0 0 1600 900` | `3200×1800` |
| 4:3 | `0 0 1200 900` | `2400×1800` |
| 3:4 | `0 0 900 1200` | `1800×2400` |
| 1:1 | `0 0 1200 1200` | `2400×2400` |

Keep the SVG responsive with `width="100%"`, `height="auto"`, and `preserveAspectRatio="xMidYMid meet"` when it is embedded. Do not rasterize and reinsert the diagram into an SVG shell.

## Structure

The root SVG should include:

```xml
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 1600 900"
     role="img"
     aria-labelledby="diagram-title diagram-desc">
  <title id="diagram-title">...</title>
  <desc id="diagram-desc">...</desc>
  <defs>...</defs>
  <g id="diagram-background">...</g>
  <g id="diagram-groups">...</g>
  <g id="diagram-relations">...</g>
  <g id="diagram-nodes">...</g>
  <g id="diagram-labels">...</g>
</svg>
```

- Keep all IDs unique within an HTML document, including marker IDs.
- Prefix reusable IDs with the diagram name.
- Keep visible words as `<text>` and `<tspan>`; do not convert them to paths.
- Avoid `<foreignObject>` for final diagrams because layout and font rendering vary across viewers.
- Add `vector-effect="non-scaling-stroke"` to important strokes when the SVG will be resized.
- Put relations behind nodes unless a deliberate overlay is required.

## Typography

Use classes for script-aware type:

```css
.zh { font-family: "Songti SC", SimSun, STSong, serif; }
.en { font-family: "Times New Roman", Times, serif; }
.math { font-family: "STIX Two Math", "Cambria Math", serif; }
```

SVG does not perform reliable automatic word wrapping. Write each line explicitly with `<tspan x="..." dy="...">`. For each text block:

- define a maximum width in the layout notes;
- keep at least 20–28 units of horizontal padding at 1600×900;
- prefer 1.25–1.4 line height;
- align text from a stable anchor rather than eyeballing each line;
- inspect the actual installed-font rendering before approving.

If a node requires more than four lines, shorten the copy, enlarge the node, or split the diagram.

## Layout sequence

1. Mark outer safe area and title/legend zones.
2. Allocate group bounds and whitespace.
3. Place nodes on a grid with consistent alignment anchors.
4. Reserve connector corridors and loop-back lanes.
5. Route relations and place relation labels.
6. Add secondary notes last.
7. Remove temporary guides before delivery.

Use `data-boundary="x y width height"` on text-heavy groups when it helps review. Use `data-from`, `data-to`, and `data-relation` on connector paths so the validator can check references and reviewers can trace intent.

## Connector construction

- Markers and connector strokes use the same color.
- Use `markerUnits="strokeWidth"` or test marker scaling explicitly.
- Arrowheads touch the target boundary without entering the node's text area.
- Source paths begin at the source boundary, not at its center behind the fill.
- Orthogonal routes use deliberate bends; avoid 1–3 unit accidental gaps at segment joins.
- Give long loop-back paths a dedicated outer lane and a clear return point.
- If several relations converge, draw a semantic junction; otherwise route them separately.

The Source SVG must remain understandable in grayscale. Color supplements labels, shapes, and line styles.

## Default visual restrictions

Avoid gradients, filters, shadows, glow, texture, `foreignObject`, ornamental imagery, and animation. An explicitly requested Conceptual Diagram may depart from these restrictions only when the Project Style DNA supports it and readability improves.

Use external icons sparingly. Place the text label first, then decide whether an icon adds recognition. Do not use emoji as diagram icons.

## Formula Inset

Omit formulas by default. If explicitly requested and essential:

- use a small, clearly separated inset;
- use math fonts and real mathematical symbols;
- define every variable or use established domain notation;
- do not let the formula interrupt the primary reading path;
- keep it editable as text where possible.

## PNG rendering

Render with a standards-based browser from the final SVG:

```bash
node <skill-dir>/scripts/render_svg.mjs diagram.svg --scale 2
```

The default output is `diagram.preview.png`. Do not use Finder thumbnails, Quick Look captures, or screenshots that are later enlarged. Do not crop or stretch the PNG after rendering.

If the target viewer substitutes a font, either embed a permitted font, choose an installed fallback, or document the difference. Never hide a font substitution that changes wrapping.

## Required review

Run static validation first:

```bash
python3 <skill-dir>/scripts/validate_svg.py diagram.svg --strict
```

Then inspect the SVG and PNG side by side at the intended display size:

- title, group, node, and note hierarchy;
- text wrapping and baseline alignment;
- minimum padding and sibling gaps;
- clipping at every viewBox edge;
- each connector from source boundary to target boundary;
- marker position and size;
- consistent palette roles;
- whitespace balance and reading order;
- PNG dimensions and aspect ratio.

For an edited diagram embedded in HTML or documentation, also inspect the final page and its responsive or fixed target viewport. A valid isolated SVG can still overflow its container.

