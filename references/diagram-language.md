# Diagram Language

Read this reference when choosing a diagram form, encoding a relationship, splitting overview/detail figures, or standardizing terminology and levels.

## Choose the smallest truthful diagram

| Question | Preferred form |
| --- | --- |
| What are the major parts and boundaries? | architecture or containment diagram |
| How does information move and transform? | data-flow diagram |
| Who performs or owns each step? | swimlane or business process diagram |
| What happens over time between participants? | sequence diagram |
| Which states exist and what triggers transitions? | state diagram |
| What depends on, invokes, or publishes to what? | relationship graph |
| How does one loop execute repeatedly? | numbered cycle with explicit loop-back |

Do not combine diagram types unless the added grammar is essential. A flowchart inside every architecture component usually indicates that the content should be split.

## Overview and detail boundaries

An Overview Diagram contains system boundary, primary actors, major modules, and trunk relationships. A Mechanism Diagram explains exactly one process, lifecycle, state model, recovery path, or collaboration.

Split when any condition is true:

- more than three levels of containment;
- crossings cannot be removed without hiding direction;
- node copy exceeds four lines;
- a local loop competes with the global flow;
- multiple time scales appear in one figure;
- minimum text size would be violated;
- a reader must repeatedly jump between distant labels and lines.

The overview should link conceptually to each detail through stable names or level IDs, not through a dense web of extra arrows.

## Relation Grammar

| Meaning | Visual form | Required label |
| --- | --- | --- |
| certain flow, invocation, handoff, or control | solid one-way arrow | verb when not obvious |
| asynchronous, optional, delayed, or conditional path | dashed one-way arrow | condition or timing |
| real bidirectional synchronization | double-headed arrow | synchronization verb |
| undirected association | solid line without marker | relation name when ambiguous |
| containment or ownership | nesting | container title |
| state transition | one-way arrow | trigger or guard |
| unresolved inference | dashed boundary or qualified note | `推断` / `待核实` |

Never use an arrow merely to make the composition feel connected. A relation must have a source, target, verb, direction, and evidence status in the semantic brief.

## Ordered flows and sequence badges

When relations form a real process order or a closed execution loop, number the relations `1, 2, 3, 4…` in traversal order. The numbering belongs to the connector because it explains which directed transition happens next; a number placed only inside a node is not a substitute.

- Start at `1`; use positive integers with no gaps or duplicates.
- Place the Sequence Badge on or immediately beside the corresponding connector, normally near its first third or midpoint.
- Keep it clear of arrowheads, bends, relation labels, node boundaries, and text.
- Keep every arrowhead visible. Readers should understand direction from the arrowhead and order from the badge.
- In a cycle, number the return connector last so the loop closure is explicit.
- For a branch, share the last common number before the split, then label branches with the next independent step only when the domain defines their order. If branches are parallel, use branch labels rather than inventing a false numeric order.
- Do not number architecture dependencies, containment, association, or other unordered relations.

In SVG, mark the ordered group with `data-ordered-flow="true"`, each member connector with `data-sequence="N"`, and its visible badge group with `data-sequence-label="N"`. This lets static validation detect missing, duplicate, or non-contiguous numbering.

## Connector routing

- Leave and enter nodes from explicit ports or unambiguous boundary points.
- Keep at least one text-height of clearance from labels.
- Prefer short orthogonal paths for ordinary flows and smooth curves for long return paths.
- Do not let separate relations share a long segment unless a visible junction has semantic meaning.
- Crossings are acceptable only when no better layout exists; use a bridge or reroute so the paths cannot be mistaken for a junction.
- A loop-back arrow must visibly return to the correct step, not terminate in empty space near it.
- In an Ordered Flow, every Sequence Badge must be unambiguously attached to one connector and must not hide its arrowhead.

## Terminology

Create a Diagram Glossary before labeling a multi-diagram set.

- Use the source system's canonical term when it has a distinct meaning.
- On first use, pair a precise Chinese label with canonical English when helpful: `轮次（Turn）`.
- Preserve source identifiers such as `agentLoopContinue()` or `turn_end` exactly; explain them separately instead of translating the identifier.
- Do not use several Chinese translations for one English term.
- Do not collapse neighboring concepts merely to shorten labels.

For Agent Harness subjects, keep these distinctions when applicable:

- **Agent Run**: one low-level execution from start until its agent-level end event.
- **Turn**: one model-facing reasoning/tool cycle within a run.
- **Agent Loop**: the control loop coordinating model responses, tool execution, and subsequent turns.
- **Tool Call / Tool Result**: requested operation and the result returned into later context.
- **Steering**: input injected at the next supported boundary of an active run; not necessarily an interruption of a currently executing tool.
- **Follow-up**: queued input considered after a natural stopping point.
- **Session History**: persisted conversation/event history.
- **Model Context**: messages and tool definitions assembled for a specific model request.
- **Compaction**: replacement of older request context with a summary while preserving the underlying session record when the implementation does so.

When a product uses its own term, show it and add a short note. Do not substitute a more familiar term if that changes behavior.

## Levels

Levels describe explanatory scope, not importance. Define them once in the semantic brief. A common software-oriented scheme is:

- `L0` — system landscape or end-to-end overview
- `L1` — orchestration or control flow
- `L2` — execution mechanism or request/tool cycle
- `L3` — lifecycle, persistence, recovery, or integration wrapper

This scheme is optional. The subject may need different definitions, but once chosen, use the level ID or its canonical name consistently. Do not alternate among `外层`, `内层`, `底层`, and `低层` as substitutes.

## Text hierarchy

Within a node, prefer:

1. canonical title;
2. one short role statement;
3. at most two compact details.

Use connector labels for what moves or why the relationship exists. Use adjacent notes for caveats. Use the prose surrounding the diagram for explanations that do not affect visual structure.

## Natural wording

Node copy must read like something its author would say aloud, not like compressed slogans.

- Avoid runs of parallel clipped phrases of identical length (「表现有证据、操作有边界、变化可比较、问题能追溯、中断后能续」). Truncating a phrase to force parallelism (「中断后能续」) is worse than one extra character.
- Each line should contain a complete, specific statement: a subject or object plus a verb the reader can act on.
- When a list is genuinely parallel, let line lengths vary naturally; do not pad or clip for symmetry.
- Read every label aloud before delivery. If it sounds like machine-generated filler, rewrite it.
