# WP Plugin Review Output Formats

## Language Selection

Choose the output language by the strongest local signal:

- user request language
- existing issue/PR/review discussion language
- repository documentation language
- plugin audience and distribution target

Prefer Japanese when the user asks in Japanese or the repo is Japanese-heavy. Prefer English when the repo, PR, or public upstream contribution is English-heavy, especially for WordPress.org-facing or international collaboration. If the review report is Japanese but a PR will likely target an English repository, include an English PR title/body draft as a separate "PR preparation" section.

## Default: Severity-Ordered Review

Use this for most code reviews.

```markdown
## Findings

### Critical
- [Critical] `includes/rest.php:84` - REST endpoint allows unauthenticated option updates
  - Risk: Any visitor can change plugin settings because `permission_callback` returns `true`.
  - Evidence: The route accepts `site_id` and `enabled` and calls `update_option()` without a capability check.
  - How to fix: Require `current_user_can( 'manage_options' )` or a narrower custom capability in `permission_callback`; keep nonce checks for cookie-authenticated admin requests where applicable.
  - Verification: Call the endpoint as an unauthenticated visitor and as a low-privilege user; both should be rejected.

### High
- [High] `admin/save.php:42` - Nonce is used without authorization
  - Risk: A stolen or leaked nonce lets a low-privilege logged-in user save privileged settings.
  - How to fix: Check the correct capability immediately before processing the save.
  - Verification: Confirm a Subscriber cannot save the setting even with a valid nonce.

## Open Questions
- Is this plugin intended for WordPress.org submission? If yes, the i18n gaps below become release blockers.

## Verification
- Ran `composer run phpcs`.
- Did not run browser tests; no E2E setup was present.

## PR preparation
- Branch: `fix/rest-settings-permissions`
- Commit theme: Harden REST settings updates with capability checks
- PR title: `Harden REST settings update permissions`
- PR body bullets:
  - Adds capability checks to the settings update REST route.
  - Keeps nonce validation for cookie-authenticated admin requests.
  - Adds regression coverage for unauthenticated and low-privilege requests.
- Test plan:
  - `composer run phpcs`
  - `composer test`
  - Manual REST request as unauthenticated, Subscriber, and Administrator users
```

## Category-Based Review

Use when the user wants a broad audit or when many findings span different domains.

```markdown
## Security
- [High] Missing capability check in Ajax save handler.
- [Medium] Dynamic `ORDER BY` value needs an allowlist.

## WPCS
- [Medium] Superglobal access is not unslashed/sanitized in settings import.
- [Low] Several files need prefix/naming cleanup.

## WordPress.org Readiness
- [High] Public plugin loads executable code from a remote CDN.
- [Medium] `readme.txt` does not disclose the external API dependency.

## Internationalization
- [Release blocker for WordPress.org] User-facing admin strings are not wrapped in gettext functions.
- [Low for private use] Text domain is missing in a few strings.
```

## PR Review Comment Style

Use when the user wants comments they can paste into a pull request.

```markdown
`includes/class-settings-controller.php:117`

This handler verifies the nonce, but it does not check whether the current user can change this setting. Nonces only protect against CSRF; they do not authorize the action. Please add an action-appropriate capability check, ideally immediately before the update call.
```

## Fix-Oriented Report

Use when the user asks for implementation guidance or wants Codex to patch the plugin after review.

```markdown
## Recommended Fix Plan

1. Add capability checks to all settings, REST, and Ajax write paths.
2. Normalize request handling: `wp_unslash()` then validate/sanitize by field.
3. Escape admin output at render time.
4. Add or update WPCS configuration and run PHPCS.

## Minimal Patch Direction

- In `Admin\Settings::save()`, return early when `! current_user_can( 'manage_options' )`.
- Replace raw `$_POST['title']` usage with a checked key, `wp_unslash()`, and `sanitize_text_field()`.
- Escape saved option values with `esc_attr()` in input attributes and `esc_html()` in text nodes.

## PR Preparation

- Suggested branch: `fix/settings-save-hardening`
- Suggested commits:
  - `Harden settings save permissions`
  - `Sanitize settings request payloads`
  - `Escape settings form output`
- PR title: `Harden settings save flow`
- PR description:
  - Adds server-side capability checks before settings updates.
  - Normalizes and sanitizes request data before persistence.
  - Escapes saved values in the admin settings UI.
- Test plan:
  - Run WPCS/PHPCS.
  - Save settings as Administrator.
  - Confirm lower-privilege users cannot save settings.
```

## PR-Ready Review Summary

Use this when the user is likely to create a pull request after the review, even if fixes are not implemented yet.

```markdown
## Pull request preparation

- Suggested branch: `fix/ajax-export-permissions`
- Suggested PR title: `Harden CSV export permissions`
- Scope:
  - Add capability checks to the CSV export Ajax handler.
  - Validate requested export type against an allowlist.
  - Escape generated admin notice output.
- Out of scope:
  - Broad WPCS formatting across unrelated files.
  - Changing CSV column structure.
- Test plan:
  - `composer run phpcs`
  - Manual export as Administrator.
  - Confirm Subscriber and unauthenticated requests are rejected.
- Release notes:
  - Security hardening for CSV export permissions.
```

## No Findings Format

Use when no actionable issues are found.

```markdown
重大な問題は見つかりませんでした。

確認した範囲:
- REST/Ajax の権限チェック
- 設定保存時の nonce / capability / sanitization
- 管理画面出力の escaping
- WPCS 実行結果

残るリスク:
- 手元ではブラウザ操作の E2E は未実行です。
- WordPress.org 登録前提なら、readme と i18n の最終確認は別途必要です。
```

## Choosing A Format

- Default to severity-ordered review for actionable code review.
- Use category-based review for audit summaries, handoff docs, or many mixed concerns.
- Use PR comment style for inline review workflows.
- Use fix-oriented report when the user asks to implement changes next.
- Include PR preparation whenever the review identifies actionable changes that are likely to become a pull request.
- Use no-findings format only after stating what was actually checked.
