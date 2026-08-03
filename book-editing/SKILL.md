---
name: book-editing
description: Edit and structurally revise existing Markdown book chapters for purpose, reader level, explanation order, repetition, terminology, voice, and continuity with adjacent chapters. Use when Codex is asked to revise, polish, shorten, reorganize, or review an existing manuscript while preserving verified meaning. Pair with $olein-writing-style for the author's final Japanese prose; use $book-fact-check separately when claims require external verification.
---

# Book Editing

## Core Rules

- Preserve the author's intended meaning and all supported facts unless the user authorizes substantive changes.
- Treat repository specifications and the approved outline as authoritative.
- Use `$olein-writing-style` for Japanese voice and phrasing when it is available. Do not let stylistic polishing alter technical meaning.
- Do not silently repair questionable facts. Mark or report them for `$book-fact-check`.
- Keep editing comments, alternatives, and review notes outside publishable manuscript files unless the repository defines an annotation convention.
- Do not edit generated files under `build/` or equivalent output directories as source manuscripts.

## Choose the Editing Mode

- **Direct edit**: use when the user asks to revise or polish a manuscript file. Make scoped changes and verify them.
- **Review only**: use when the user asks for critique, diagnosis, or an editorial review. Do not modify files; report findings with locations and proposed changes.
- **Substantive restructure**: use when sections must be moved, merged, removed, or newly added. Confirm that the requested scope permits structural changes; preserve the approved chapter objective.

## Workflow

1. Read applicable `AGENTS.md` files and book guidance such as the book specification, reader profile, editorial policy, style guide, terminology, and structure documents when present.
2. Read the target manuscript, its outline and notes, and enough of adjacent chapters to detect continuity problems.
3. Establish the chapter contract:
   - intended reader outcome
   - assumed knowledge
   - required and excluded topics
   - facts and examples that must remain unchanged
4. Diagnose before rewriting. Use `references/editing-checklist.md` to identify the smallest set of changes that resolves the problems.
5. Edit in passes:
   - structure and explanation order
   - redundancy and scope
   - paragraph clarity and transitions
   - terminology and notation
   - voice with `$olein-writing-style`
6. Compare the revision with the original for lost qualifications, changed technical meaning, missing references, or accidental scope expansion.
7. Run repository-provided checks or previews when files were changed and suitable commands exist.

## Fact Boundaries

- Preserve citations and source associations when moving or rewriting claims.
- Flag unsupported, contradictory, ambiguous, or time-sensitive claims rather than normalizing them into confident prose.
- Use `$book-fact-check` when verification is part of the request. Editing alone is not evidence that a claim is correct.

## Deliverables

For a direct edit, return:

- changed file and the nature of the revision
- major structural or meaning-sensitive changes
- claims that still need fact-checking
- checks run and their results

For review only, group findings by priority and include precise file and section locations, rationale, and a concrete revision direction. Avoid line-by-line commentary when one structural finding explains several symptoms.

## References

- Read `references/editing-checklist.md` before revising or reviewing a chapter.
