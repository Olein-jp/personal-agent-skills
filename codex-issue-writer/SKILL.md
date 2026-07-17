---
name: codex-issue-writer
description: Create concise, high-signal GitHub Issues or PR work instructions for Codex. Use when the user wants to turn a feature request, bug report, refactor, review finding, or ChatGPT conversation into an Issue that helps Codex implement accurately while minimizing unnecessary token use, repo exploration, planning, subagents, tests, and verbose reporting.
---

# Codex Issue Writer

## Goal

Draft GitHub Issues that work as Codex task briefs: clear enough to implement and verify, narrow enough to avoid wasteful exploration. Prefer Japanese unless the user requests another language.

Use the referenced conversation as operating doctrine:

- Accuracy comes from purpose, scope, acceptance criteria, constraints, and verification.
- Token efficiency comes from limiting the first files to read, stopping conditions, related tests only, no unrelated refactors, no default subagents, and short completion reports.
- `AGENTS.md` should hold stable project rules; the Issue should hold task-specific goals and limits.

## Workflow

1. Identify task size:
   - **S**: text change, single-condition bug, CSS tweak, single function.
   - **M**: normal feature or behavior change touching a few related files.
   - **L**: design/data/auth/API changes, cross-cutting refactor, multiple packages, unclear impact.
2. Ask at most one concise clarification only when the task cannot be scoped safely. Otherwise, draft with explicit assumptions.
3. Extract only task-local facts:
   - desired outcome
   - user/problem context
   - first files or screens Codex should inspect
   - implementation requirements
   - acceptance criteria
   - constraints and non-goals
   - relevant verification commands
4. Add token-control instructions:
   - first inspect only the listed files/screens
   - expand only to directly referenced dependencies needed for implementation
   - avoid repo-wide investigation unless the listed entry points contradict the request
   - do not use subagents unless explicitly justified
   - avoid detailed planning for S tasks
   - run related tests first; run full suites only for shared/cross-cutting changes
   - keep final report to four items
5. For L tasks, split into two Issues or phases: investigation/plan first, implementation second after approval.
6. Read `references/issue-templates.md` when the user asks for a ready-to-use Issue body, template, or size-specific wording.

## Drafting Rules

- Start with the outcome, not implementation details.
- Keep acceptance criteria to 3-7 checkboxes unless the task truly needs more.
- Separate **must inspect** from **may inspect if needed**.
- Mark non-goals concretely: no unrelated refactors, no package updates, no doc rewrites, no broad formatting.
- Prefer "related tests only" by default. Name exact commands when the user or repo context provides them.
- Preserve Codex's ability to choose implementation details within the stated boundaries.
- Avoid duplicating stable repo rules already expected to live in `AGENTS.md`.

## Size Guidance

### S Tasks

Use a compact Issue. Include target file, current behavior, expected behavior, 1-3 acceptance criteria, one related verification command if known, and "do not change unrelated files." State that no plan or subagent is needed.

### M Tasks

Use the standard token-efficient Issue structure. Include entry files, requirements, acceptance criteria, constraints, non-goals, verification, and reporting format.

### L Tasks

Create an investigation Issue first:

- inspect only named entry points and directly related dependencies
- produce a 5-item-or-less implementation plan
- identify risks, files likely to change, and verification strategy
- do not implement yet

Then create a second implementation Issue once the plan is accepted.

## Output Shape

When drafting an Issue, return a polished GitHub Issue body in Markdown. Include a short note before it only if assumptions or missing information matter.

Default headings:

```markdown
# 目的
## 作業対象
## 実装要件
## 受け入れ条件
## 制約
## 対象外
## 検証
## 作業方法
## 完了報告
```

For S tasks, use fewer headings. For L tasks, replace implementation sections with investigation and planning sections.

## Self-Check

Before answering, verify:

- the Issue says where Codex should start reading
- the Issue says when Codex should stop investigating
- acceptance criteria are testable
- verification is scoped to the change
- unnecessary work is explicitly excluded
- the completion report is short
- the Issue does not paste long background conversation text
