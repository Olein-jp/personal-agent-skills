---
name: book-drafting
description: Draft new Markdown chapters for a book from the repository's outline, chapter notes, sources, reader profile, editorial rules, terminology, and adjacent chapters. Use when Codex is asked to write, expand, or complete a new book chapter or section. Pair with $olein-writing-style when writing the author's final Japanese prose; this skill controls book-specific structure, evidence boundaries, inputs, and deliverables.
---

# Book Drafting

## Core Rules

- Treat the book repository as the source of truth for scope, audience, structure, notation, and terminology.
- Use `$olein-writing-style` for the author's Japanese voice when it is available. Let repository-specific editorial and notation rules take precedence where they conflict.
- Draft only the requested chapter or section. Do not change the book-wide structure without explicit approval.
- Do not invent facts, examples presented as real, version details, URLs, quotations, statistics, or source support.
- Keep research notes and drafting commentary out of the publishable manuscript.
- Preserve semantic Markdown intended for Pandoc. Do not introduce raw HTML, layout-only markup, or unsupported custom styles unless the repository permits them.

## Workflow

1. Locate repository guidance before drafting:
   - read applicable `AGENTS.md` files
   - inspect book-level specifications such as `docs/BOOK_SPEC.md`, `docs/READER_PROFILE.md`, `docs/EDITORIAL_POLICY.md`, `docs/STYLE_GUIDE.md`, `docs/TERMINOLOGY.md`, and `docs/STRUCTURE.md` when present
   - inspect the target chapter's `outline.md`, `notes.md`, `sources.md`, and existing `index.md` when present
   - read the preceding and following chapter outlines or manuscripts when needed for continuity
2. Identify the drafting contract:
   - chapter purpose and reader outcome
   - assumed reader knowledge
   - required topics, examples, figures, and exclusions
   - target length or level of detail
   - allowed Markdown and Pandoc conventions
3. Build a short internal evidence map that ties factual claims to the supplied sources. Separate:
   - supported facts
   - authorial explanation or interpretation
   - missing evidence or unresolved decisions
4. Draft in the order that best supports reader understanding. Use `references/chapter-template.md` only when the repository does not define a stronger chapter pattern.
5. Apply `$olein-writing-style` to final prose, then normalize terminology and notation against repository rules.
6. Read `references/drafting-checklist.md`, check the requested length, and revise once. Meet an approximate length without padding unsupported details; report a material shortfall when evidence or scope is insufficient.
7. Run repository-provided checks or previews when the task includes editing files and suitable commands exist.

## Handling Missing Information

- Continue with supported material when missing information does not change the chapter's direction.
- Mark an unresolved manuscript statement with `[要確認]` only when repository policy allows editorial markers.
- If a missing choice would materially change the chapter, stop before making that choice and report it.
- Never convert a plausible inference into an unqualified fact.

## Deliverables

When editing the repository, write the publishable draft to the designated chapter file, normally `index.md`. Keep notes and sources in their designated files.

Return a concise summary with:

- drafted or changed file
- chapter purpose and covered scope
- unresolved items
- suggested additional research
- material deviation from the requested length or scope
- checks run and their results

If the user requested text only, return the draft followed by unresolved items and research suggestions outside the manuscript text.

## References

- Read `references/chapter-template.md` only when no repository-specific chapter template exists.
- Read `references/drafting-checklist.md` before finalizing a draft.
