# Project Style DNA Starter

Use this reference only when the target project has no established visual specification. Keep the resulting project file concise; remove any rule that does not change a design decision.

## One sentence

Editorial technical diagrams with generous whitespace, large serif typography, precise semantic color, and visibly traceable relationships.

## Design principles

- Accuracy before decoration.
- One primary claim per diagram.
- Hierarchy through position, scale, whitespace, and type before color.
- Color distinguishes semantic roles; it does not fill empty space.
- The composition should read as a diagram, not a dashboard or a collage of cards.
- An Overview Diagram and its Mechanism Diagrams are one family: same vocabulary, level system, palette, stroke hierarchy, and spacing rhythm.

## Canvas and grid

- Background: white `#FFFFFF`.
- Default internal grid: 8 units; prefer spacing steps of 16, 24, 32, 48, and 64.
- Outer safe margin at 1600×900: 64–88 units.
- Keep title, legend, and content in distinct zones.
- Reserve connector corridors before placing explanatory copy.
- Maintain visible whitespace between sibling groups; never rely on border color alone to separate them.

## Typography

- Chinese: `Songti SC, SimSun, STSong, serif`.
- Latin and numerals: `Times New Roman, Times, serif`.
- Formula Inset only: `STIX Two Math, Cambria Math, serif`.
- Suggested 1600×900 scale:
  - diagram title: 42–52
  - section or group title: 28–34
  - node title: 24–30
  - body: 22–26
  - secondary note: 18–20
- Use sentence case. Avoid all-caps labels except short protocol or product identifiers.
- Keep visible node copy to a title and at most three short lines. Move explanations to a Mechanism Diagram or adjacent prose.

## Semantic palette

| Role | Fill | Typical use |
| --- | --- | --- |
| Entry / interface | `#C4DCE6` | user input, external system, API boundary |
| Processing / orchestration | `#FBE7A6` | engine, workflow, decision, primary execution |
| Data / context | `#E0E4CC` | data product, context, storage, document |
| State / lifecycle | `#D2D2E0` | session, state machine, persistence, recovery |
| Exception / warning | `#FFBFBF` | error, risk, blocked path, exceptional control |

Use dark neutral text and strokes for contrast:

- primary text: `#242424`
- secondary text: `#555555`
- primary stroke: `#3F3F3F`
- quiet separator: `#B8B8B8`

Not every diagram needs all five fills. Once a role is assigned in a Diagram Set, do not reuse that color for another role.

## Shapes and strokes

- Use semantic shapes: containers for scope, rounded rectangles for components, cylinders only for real stores, diamonds only for decisions, and circles only for events or compact states.
- At 1600×900, use roughly 1.5 units for quiet boundaries, 2–2.5 for nodes, and 2.5–3 for primary relations. Keep strokes thin enough to avoid overwhelming small diagrams.
- Use moderate corner radii, normally 12–18 units. Avoid pill-shaped boxes unless the subject is literally a token, tag, or status chip.
- Use one arrowhead family per Diagram Set. Arrowheads must remain legible in the PNG Preview.
- For an Ordered Flow, use compact 30–36 unit Sequence Badges with high-contrast numerals. Keep badge geometry consistent, position it beside the relation rather than inside a node, and leave the arrowhead unobstructed.

## Anti-patterns

- gradients, glassmorphism, glow, heavy shadows, textures, noise, 3D, or decorative perspective;
- repeated identical cards when objects have different semantic roles;
- generic sparkles, robots, brains, clouds, or database icons added without meaning;
- large decorative headings that compete with the diagram;
- every node having a subtitle, badge, icon, border, and fill simultaneously;
- tiny text used to avoid splitting a dense diagram;
- decorative curves or arrows with no verb in the semantic brief;
- strings of parallel four-to-five-character slogans (「表现有证据 / 操作有边界 / 中断后能续」-style lists) that read like generated filler; write each line as natural language a person would actually say.

## Adapting a Donor Design

Extract only decisions that fit the content:

1. composition: grid, reading direction, group balance;
2. rhythm: spacing, density, section cadence;
3. typography: scale contrast and line length, not proprietary fonts;
4. emphasis: how one primary element is made dominant;
5. interaction: only for an explicitly requested Interactive Variant.

Rewrite those decisions using this project's vocabulary and tokens. Do not carry over brand colors, logos, product screenshots, unique illustrations, or ornamental effects merely because they appear in the donor.
