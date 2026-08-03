---
name: book-fact-check
description: Fact-check technical claims, quotations, version details, dates, numbers, compatibility statements, and URLs in Markdown book manuscripts against primary and authoritative sources. Use when Codex is asked to verify a chapter, audit source support, check links, confirm time-sensitive product information, or prepare an evidence-backed correction report. This skill reports verification status and evidence; it does not rewrite the manuscript unless the user also asks for edits.
---

# Book Fact Check

## Core Rules

- Verify claims against the strongest available evidence; do not treat repeated secondary claims as independent confirmation.
- Prefer primary sources and record the exact page or local artifact that supports each conclusion.
- Distinguish what a source states from what can only be inferred.
- Record the verification date for time-sensitive claims.
- Do not rewrite manuscript files unless the user explicitly requests corrections.
- Preserve uncertainty. Absence of evidence is not evidence that a claim is false.

## Workflow

1. Read applicable repository instructions and `references/source-policy.md`.
2. Identify claim units rather than checking whole paragraphs as a single assertion. Prioritize:
   - technical behavior and procedures
   - versions, dates, prices, limits, compatibility, and support status
   - quotations and attributed opinions
   - statistics and numerical comparisons
   - legal, security, privacy, accessibility, or performance claims
   - URLs and labels that readers must follow
3. Inspect repository sources first:
   - chapter `sources.md` and notes
   - local code, fixtures, screenshots, test results, or archived documents
   - book-level research and terminology
4. Use current external research when the claim is time-sensitive, externally sourced, or not resolved locally. Prefer official documentation, specifications, release notes, source repositories, standards bodies, and original research.
5. Record for each claim:
   - manuscript location and normalized claim
   - status
   - evidence and source URL or local path
   - checked date when relevant
   - required correction or limitation
6. Test URLs for destination, relevance, redirects, and whether the cited page actually supports the nearby claim. A reachable URL is not automatically valid evidence.
7. Summarize corrections in priority order. Keep verified items compact; explain disputed or unresolved items enough for an editor to act.

## Status Vocabulary

Use exactly one primary status per claim:

- **確認済み**: strong evidence directly supports the material claim.
- **修正が必要**: reliable evidence contradicts the claim or shows a material omission.
- **一次情報が見つからない**: the claim may be plausible, but no suitable primary or authoritative evidence was located.
- **確認日が必要**: the claim is correct only as of a specific date or is likely to change.

Add a short qualifier when useful, such as `一部のみ確認済み`, without replacing the primary status.

## Deliverable

Return a fact-check report in this form:

```markdown
## Summary

- Claims checked:
- Confirmed:
- Corrections required:
- Primary source not found:
- Date-sensitive:

## Findings

### [Status] Short claim label

- Location:
- Claim:
- Assessment:
- Evidence:
- Checked: YYYY-MM-DD
- Recommended action:
```

When the user also asks for corrections, edit only claims with sufficient evidence, preserve citations, and list every changed claim in the final summary. Leave unresolved claims marked or reported according to repository policy.

## References

- Read `references/source-policy.md` before checking claims or selecting evidence.
