---
name: wp-plugin-review
description: Review WordPress plugins with a security-first, WPCS-aligned code review workflow. Use when Codex is asked to review, audit, harden, or prepare a WordPress plugin for release, WordPress.org Plugin Directory submission, public distribution, PR review, or security remediation. Covers PHP, JavaScript, blocks, REST API, Ajax, admin screens, settings, options, custom tables, cron, WP-CLI, assets, packaging, and readme/release readiness. Internationalization is required only when the plugin targets the official repository or broader public/global distribution; otherwise treat i18n as lower priority unless it creates user-facing defects.
---

# WP Plugin Review

## Goal

Review WordPress plugins as a senior WordPress security reviewer. Prioritize exploitable bugs, privilege boundary failures, data handling mistakes, WPCS violations that hide or create risk, and release blockers. Treat internationalization as conditional: required for WordPress.org or broad public/global distribution, low priority for private or narrowly scoped plugins unless the user asks otherwise.

## Core Workflow

1. Confirm the review target:
   - plugin root or main plugin file
   - intended distribution: private, client-only, commercial, WordPress.org, or global/public
   - target WordPress/PHP versions when visible
   - whether the user wants findings only or fixes as well
2. Triage the repository before judging code:
   - locate plugin headers, bootstrap files, `composer.json`, `package.json`, `phpcs.xml*`, PHPUnit config, block metadata, REST/Ajax registrations, uninstall logic, and release files
   - prefer `rg`/`rg --files` and existing project scripts
   - if available, run or recommend WPCS/PHPCS using the repo's own configuration before inventing one
3. Read `references/review-checklist.md` for the detailed review checklist.
4. Read `references/output-formats.md` before producing a user-facing review, especially when the user asks what report formats are possible.
5. Inspect high-risk flows first:
   - writes, deletes, imports, exports, uploads, redirects, remote requests, code execution, cron, background jobs, REST/Ajax handlers, shortcodes, blocks, settings saves, custom SQL, and uninstall
6. Verify each finding against actual code. Do not report generic best practices as findings unless the code creates a concrete risk.
7. Lead with findings ordered by severity. Include file/line references, exploit or failure scenario, and a specific fix direction.
8. Include enough remediation and PR-preparation detail that the user can turn the review into a pull request without re-investigating the same context.

## Review Priorities

Use this severity model:

- **Critical**: unauthenticated or low-privilege data loss, privilege escalation, remote code execution, arbitrary file write/delete/read, SQL injection, stored XSS reachable by lower roles, supply-chain execution, or dangerous automatic updates.
- **High**: missing capability checks on privileged actions, nonce-only authorization, CSRF with state change, unsafe uploads, REST/Ajax permission callback flaws, reflected/stored XSS in admin/public flows, unsafe redirects, SSRF, path traversal, weak uninstall deletion.
- **Medium**: incomplete sanitization/validation, late escaping gaps with limited reach, SQL prepare misuse with limited exploitability, privacy/consent issues, insecure defaults, multisite capability mistakes, cron idempotency or race risks.
- **Low**: WPCS/readability issues that do not materially change behavior, minor packaging/readme issues, conditional i18n gaps for private plugins.

Escalate i18n issues to release blockers when the plugin is intended for WordPress.org, translate.wordpress.org, or broad international distribution.

## WPCS And Tooling

Prefer existing project commands:

- `composer run lint`
- `composer run phpcs`
- `vendor/bin/phpcs`
- `vendor/bin/phpcs -ps . --standard=WordPress`
- `vendor/bin/phpcbf` only when the user asks for fixes and formatting-only changes are acceptable

If WPCS is absent, do not install dependencies without permission. Review manually against WPCS expectations and recommend adding project-local WPCS tooling when release quality matters.

When PHPCS reports many issues, separate mechanical style issues from security-relevant WPCS findings. Do not bury exploitable bugs under formatting noise.

## Security Baseline

Always check:

- capability checks with `current_user_can()` or equivalent before privileged actions
- nonces for CSRF protection, never as authorization
- validation/sanitization of request, REST, Ajax, shortcode, block, option, meta, uploaded, remote, and database-derived data
- context-appropriate escaping at output, as late as practical
- `$wpdb->prepare()` and safe allowlists for dynamic SQL identifiers/order clauses
- safe redirects, safe file paths, safe uploads, and no arbitrary include/require paths
- REST `permission_callback`, Ajax `wp_ajax_nopriv_*`, cron, WP-CLI, and uninstall behavior
- privacy, consent, licensing, third-party service calls, and WordPress.org guideline risks when public distribution is intended

## Output Rules

Default to a code-review report:

1. Findings first, highest severity first.
2. Match the output language to the primary language used by the user, repository docs, issue/PR text, or surrounding project communication. Prefer Japanese for Japanese requests and Japanese-heavy repos; prefer English for English-heavy repos or when preparing public upstream/WordPress.org-facing PR text.
3. Each finding includes severity, file/line, risk, evidence, how to fix it, and a verification idea.
4. Then list open questions or assumptions.
5. Then list verification performed and commands that failed or were unavailable.
6. Add PR preparation notes when findings are actionable: suggested branch name, commit theme, PR title, PR body bullets, test plan, and release/readme notes if relevant.
7. Keep summary brief. If no issues are found, say so clearly and note residual test gaps.

When the user asks for fixes, implement the smallest safe change set that addresses the reviewed issue. Preserve unrelated user changes and avoid broad formatting unless the review target is explicitly WPCS cleanup.

## References

- Read `references/review-checklist.md` for detailed review coverage.
- Read `references/output-formats.md` for concrete report format examples.
