---
name: wp-plugin-introduction-writer
description: Plan, research, outline, draft, and self-check Japanese blog articles that introduce WordPress plugins. Use when Codex is asked to write or prepare a plugin introduction, comparison, hands-on review, setup guide, feature overview, or recommendation article for a WordPress plugin. Always pair this skill with $olein-writing-style for voice, tone, and final Japanese prose; this skill supplies plugin-specific research, structure, fact-checking, and article-quality guidance only.
---

# WP Plugin Introduction Writer

## Core Rule

Use `$olein-writing-style` together with this skill whenever drafting, rewriting, or polishing the final article. Let `$olein-writing-style` control voice, Japanese phrasing, warmth, ending tone, and authorial stance. Use this skill only for WordPress plugin introduction strategy, source handling, structure, and technical/product accuracy.

## Workflow

1. Confirm the article target:
   - plugin name and official URL when available
   - target medium, expected length, and publication intent
   - reader level: site owner, beginner, developer, maintainer, client, or comparison shopper
   - article type: introduction, hands-on review, setup guide, comparison, recommendation, update note, or migration note
2. Gather high-confidence source material:
   - prefer official plugin directory pages, plugin vendor docs, GitHub repositories, changelogs, readme files, screenshots, pricing pages, support docs, and WordPress.org forum threads
   - inspect local plugin code or a development environment when the request includes a repository or implementation notes
   - use current web research for version numbers, active installs, compatibility, pricing, license, support status, and recent changes
3. Read `references/article-checklist.md` before outlining or drafting a full article.
4. Build a facts-first brief before writing:
   - what the plugin does
   - who it is for and who it is not for
   - main value proposition in plain Japanese
   - setup path and required prerequisites
   - strongest features, limitations, risks, and maintenance signals
   - official references to cite near the relevant sections
5. Choose a structure that matches the reader's intent:
   - **Introduction**: problem, plugin summary, useful cases, setup outline, caveats, conclusion
   - **Hands-on review**: testing environment, installation, observed behavior, useful points, friction, verdict
   - **Setup guide**: prerequisites, install/activate, key settings, verification, troubleshooting
   - **Comparison**: selection criteria, plugin-by-plugin notes, decision table or bullets, recommendation by use case
   - **Update note**: what changed, who is affected, upgrade cautions, verification steps
6. Draft with `$olein-writing-style`.
7. Self-check for factual accuracy, reader fit, and unsupported claims. Revise once before returning.

## Source Handling

Treat current plugin metadata as unstable. Verify it before stating it as fact, especially:

- latest version
- WordPress and PHP compatibility
- active installations or download counts
- pricing and plan limits
- ownership, acquisition, or support status
- security advisories and recently closed vulnerabilities
- screenshots or UI flow descriptions

When using third-party information, identify it as third-party or community-reported unless confirmed by an official source. Avoid turning marketing claims into factual claims unless the article frames them as the vendor's claim.

## Article Brief Template

Use this compact brief internally before drafting:

```markdown
Plugin:
Official sources:
Article type:
Target reader:
Reader problem:
Short answer:
Best use cases:
Not ideal for:
Setup notes:
Important settings:
Verification steps:
Caveats:
Links to cite:
```

## Writing Boundaries

Do not duplicate `$olein-writing-style` guidance about tone, first-person stance, Japanese endings, or general article voice. Do not write generic affiliate-style praise. Introduce the plugin through concrete reader problems, verified behavior, and practical caveats.

If the user only provides a plugin name, research before drafting. If reliable sources cannot confirm important details, narrow the article, say what could not be confirmed, and avoid unsupported specifics.

## References

- Read `references/article-checklist.md` for plugin-specific research, outline, and self-check criteria.
