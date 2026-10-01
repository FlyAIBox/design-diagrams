# Diagram Design

This context defines the shared language for producing precise, editable diagrams and their rendered previews.

## Language

**Source SVG**:
The authoritative, editable vector artifact. All later previews and exports derive from this file.
_Avoid_: SVG preview, vector screenshot

**PNG Preview**:
A high-resolution raster rendering generated directly from the final Source SVG at the intended aspect ratio. It is a compatibility and review artifact, never the editable source.
_Avoid_: Source image, editable PNG

**Diagram Deliverable**:
The paired Source SVG and PNG Preview representing the same content, geometry, typography, and color semantics.
_Avoid_: Image export

**Project Style DNA**:
The concise, project-owned visual rules that govern typography, color semantics, spacing, density, and prohibited treatments. It is authoritative when external references disagree.
_Avoid_: Theme prompt, inspiration board

**Donor Design**:
An external `design.md` or visual reference used to borrow selected composition, rhythm, or typography ideas before adapting them to the Project Style DNA.
_Avoid_: Template, final style, source of truth

## Evidence

**Evidence Source**:
A user-designated or authoritative document, codebase, interface contract, data dictionary, policy, research artifact, or versioned publication used to substantiate diagram content.
_Avoid_: Code source, background material

**Source-grounded Diagram**:
A diagram of an existing subject whose objects, relationships, terminology, and version claims are traceable to Evidence Sources; unresolved inferences remain visibly qualified.
_Avoid_: As-built diagram, code diagram

**Conceptual Diagram**:
A diagram of a proposed, explanatory, or target-state model that is explicitly distinguished from verified current behavior.
_Avoid_: Future diagram, imaginary architecture

## Presentation

**Formula Inset**:
An optional, compact mathematical annotation used only when a requested calculation is essential to the diagram's meaning. Diagrams omit it by default.
_Avoid_: Decorative formula, equation label

**Canvas Profile**:
The chosen aspect ratio and target rendering dimensions shared by a Source SVG and its PNG Preview. Supported profiles are 16:9, 4:3, 3:4, and 1:1.
_Avoid_: Page size, screenshot size

**High-resolution Preview**:
A PNG Preview rendered directly from the final Source SVG at no less than twice the intended display resolution, without later stretching or aspect-ratio changes.
_Avoid_: Upscaled image, enlarged screenshot

**Semantic Palette**:
The stable five-color role system shared by an overview and its detail diagrams: blue for entry or interface, yellow for processing or orchestration, green for data or context, purple for state or lifecycle, and red for exception or warning.
_Avoid_: Theme colors, decorative palette

**Script-aware Typography**:
Typography that assigns Songti-family fonts to Chinese, Times-family fonts to Latin text and numerals, and math fonts only to an explicitly requested Formula Inset.
_Avoid_: Global serif font, one-font layout

## Diagram Set

**Overview Diagram**:
The navigational diagram that shows the subject boundary, major modules, and primary relationships without explaining each mechanism internally.
_Avoid_: Full diagram, master flowchart

**Mechanism Diagram**:
A focused detail diagram that explains one process, lifecycle, state model, or collaboration while preserving the Overview Diagram's terminology, levels, and Semantic Palette.
_Avoid_: Subgraph, enlarged overview

**Relation Grammar**:
The fixed mapping from verified relationship types to connector forms: directed flow uses solid arrows, conditional or delayed flow uses labeled dashed arrows, synchronization uses bidirectional arrows, association uses unheaded lines, and containment uses nesting.
_Avoid_: Arrow style, connector theme

**Traceable Connector**:
A continuous relation path that visibly leaves its source boundary and reaches its target boundary without ambiguous shared segments, obstruction, or a detached marker.
_Avoid_: Near-connected line, implied arrow

**Diagram Glossary**:
The canonical vocabulary shared by every diagram in a Diagram Set; first use may pair a precise Chinese term with its canonical English term, while source identifiers remain unchanged.
_Avoid_: Label list, translation table

**Diagram Level**:
A named explanatory layer whose scope is defined once for a Diagram Set and then referenced consistently, usually as L0, L1, L2, or L3.
_Avoid_: Inner layer, outer layer, low layer, bottom layer

**Interactive Variant**:
An explicitly requested HTML or React presentation that adds motion to a completed diagram without replacing the Source SVG or PNG Preview.
_Avoid_: Animated SVG, default diagram

**Editorial Technical Style**:
A restrained diagram style built from whitespace, grid alignment, typographic hierarchy, semantic shapes, and clear stroke weights rather than ornamental UI effects.
_Avoid_: Dashboard style, AI aesthetic, card collage

**Rendered Validation**:
Inspection of the final Source SVG and its High-resolution Preview at the target Canvas Profile for overflow, overlap, clipping, connector continuity, hierarchy, and cross-format fidelity.
_Avoid_: SVG lint, code review
