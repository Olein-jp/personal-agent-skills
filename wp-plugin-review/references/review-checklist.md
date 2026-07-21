# WP Plugin Review Checklist

## Review Scope

Start by classifying the plugin:

- distribution: private/client-only, commercial, WordPress.org, or broad public/global
- architecture: single-file, class-based, namespaced, mu-plugin, block plugin, WooCommerce/add-on, SaaS connector
- surfaces: admin, frontend, REST, Ajax, CLI, cron, blocks, shortcodes, widgets, webhooks, uploads, imports/exports
- persistence: options, post meta, user meta, terms, custom tables, files, transients, external APIs

## Automated Checks

Use existing project tooling first:

- `composer run phpcs`, `composer run lint`, `composer test`, `vendor/bin/phpcs`
- `npm test`, `npm run lint`, `npm run build` when JS/block assets exist
- PHPUnit, Playwright, E2E, or plugin-specific tests when present

If no WPCS config exists, recommend a project-local PHPCS setup using WordPressCS/WPCS. Do not treat missing tooling as proof that the code is unsafe; treat it as a release-readiness gap.

## Authentication And Authorization

Check every state-changing or sensitive read path:

- Admin actions must check a capability appropriate to the object/action, not only `manage_options` by habit.
- Meta capabilities such as `edit_post`, `delete_post`, `edit_user`, and object IDs are preferable where object ownership matters.
- REST routes need explicit `permission_callback`; public routes must be intentionally public and read-only unless strongly justified.
- Ajax handlers must distinguish `wp_ajax_*` from `wp_ajax_nopriv_*`; nopriv handlers require extra scrutiny.
- WP-CLI commands, cron callbacks, webhooks, and background jobs still need input validation and safe assumptions.
- Nonces protect against CSRF only; they do not prove identity or permission.

Common findings:

- nonce check exists but no capability check
- capability checked only when rendering a button, not when processing the request
- REST `permission_callback` returns `true` for sensitive operations
- capability uses a role name instead of a capability
- multisite/network admin actions use single-site assumptions

## Input Validation And Sanitization

Trace all untrusted inputs from:

- `$_GET`, `$_POST`, `$_REQUEST`, `$_COOKIE`, `$_FILES`, `php://input`
- REST request params and JSON bodies
- Ajax payloads
- shortcodes and block attributes
- settings/options/meta imported from prior versions
- remote API responses and webhooks
- CSV/XML/JSON imports

Expect:

- `wp_unslash()` before sanitizing WordPress-slashed request data
- strict allowlists for enum-like values
- type casting for IDs, counts, booleans, and numeric values
- `sanitize_text_field()`, `sanitize_textarea_field()`, `sanitize_key()`, `sanitize_email()`, `sanitize_url()`, `sanitize_file_name()`, `wp_kses()` or more specific validation as context requires
- rejection of invalid values when the domain is constrained

Flag:

- broad sanitization used where validation/allowlist is required
- unsanitized block attributes rendered in PHP
- trusted remote API data rendered or stored without validation
- settings registered without a `sanitize_callback`

## Output Escaping

Verify escaping at the output boundary:

- `esc_html()` for text nodes
- `esc_attr()` for attributes
- `esc_url()` for URLs in output
- `esc_js()` or safer JSON/script patterns for inline JavaScript
- `esc_textarea()` for textarea content
- `wp_kses()`, `wp_kses_post()`, or a narrow allowed-HTML map for limited HTML
- `wp_json_encode()` for JSON output or JavaScript data

Flag:

- values escaped on save but echoed raw later
- admin notices, settings fields, list tables, block render callbacks, shortcodes, REST-rendered HTML, or email templates echo unescaped data
- escaping function mismatches context
- PHPCS ignores around escaping without clear justification

## Database And Storage

Check:

- `$wpdb->prepare()` for dynamic values
- allowlists for table names, column names, `ORDER BY`, `LIMIT`, directions, and SQL fragments
- `dbDelta()` and schema versioning for custom tables
- autoload impact for large options
- option/meta names are namespaced
- no sensitive tokens stored plain unless WordPress has no better project-appropriate option and access is tightly controlled
- cleanup is explicit and proportional on uninstall

Flag:

- concatenated SQL using request data
- `%s` placeholders used for SQL identifiers
- direct table deletion on uninstall without user intent or plugin namespace checks
- network option handling mixed with single-site option handling

## Files, Uploads, And Paths

Check:

- file names sanitized and normalized
- uploads use WordPress APIs where possible
- MIME/type checks do not rely only on extension
- paths are constrained to plugin-owned or upload-owned directories
- no user-controlled `include`, `require`, `fopen`, `unlink`, `copy`, `rename`, or archive extraction path
- generated files avoid executable PHP in upload locations

Flag:

- path traversal via `../`
- arbitrary file deletion/read/write
- remote downloads written to executable paths
- CSV/export endpoints lack authorization

## Remote Requests, Redirects, And Privacy

Check:

- `wp_remote_get()` / `wp_remote_post()` timeouts and error handling
- SSRF risk when users control URLs
- `wp_safe_redirect()` for local redirects
- consent and disclosure for tracking, telemetry, license checks, external embeds, and third-party APIs
- API keys/tokens are not exposed to frontend users
- public distribution complies with WordPress.org expectations around tracking, external code, admin notices, and links

## JavaScript, Blocks, And Assets

Check:

- block attributes are validated in PHP render callbacks
- `render.php` or dynamic callbacks escape output
- REST/Ajax endpoints used by JS enforce capabilities server-side
- localized script data avoids leaking secrets
- dependencies are declared correctly
- build artifacts are committed only when the project expects them
- no remote executable code loaded in a way that violates public repository guidelines

## Lifecycle, Cron, And Uninstall

Check:

- activation/deactivation hooks are registered at plugin-load scope
- activation does not perform heavy remote or destructive actions
- rewrite flushing happens only when needed
- cron is idempotent, unscheduled on deactivation when appropriate, and validates stored inputs
- migrations are versioned and recoverable
- uninstall removes only plugin-owned data and respects user expectations

## WPCS Review Lens

Treat WPCS as more than formatting when it points to:

- missing sanitization, validation, escaping, nonce, or capability checks
- direct access to superglobals without unslashing/sanitization
- prepared SQL issues
- discouraged functions where WordPress APIs are safer
- naming collisions, global namespace pollution, or missing prefixes

Keep purely mechanical style findings low priority unless the user explicitly requests strict WPCS cleanup.

## Internationalization Policy

Use the distribution target:

- WordPress.org, translate.wordpress.org, public/global plugin: require i18n for user-facing strings and correct text domain usage.
- Commercial/public but region-specific: strongly recommend i18n when future distribution may broaden.
- Private/client-only/internal: low priority unless the user asks, strings are already mixed inconsistently, or lack of i18n breaks an expected workflow.

For required i18n, check:

- text domain matches plugin slug
- user-facing PHP strings use gettext functions
- escaped translation helpers are used where outputting
- JavaScript strings use the WordPress i18n package and script translations where applicable
- placeholders are translator-friendly
- no variables or constants as text domain arguments unless the project has a justified exception

## WordPress.org And Public Release Readiness

When the user mentions official repository submission or broad public distribution, also check:

- GPL-compatible licensing for all included code/assets
- readable source and no intentionally obfuscated code
- no executable code loaded from third-party systems
- tracking/telemetry requires explicit consent
- admin notices are not hijacking or overly persistent
- readme has stable tag, tested up to, requires at least, license, and clear external service disclosure
- bundled dependencies have license and source clarity

## Finding Quality Bar

Only report a finding when you can point to code or a missing required path. Good findings include:

- exact location
- attacker or failure precondition
- impact
- why existing checks are insufficient
- concrete remediation, including the safest likely WordPress API or code pattern to use
- verification command or manual test idea
- PR preparation notes when the finding should become a patch

Avoid:

- generic "sanitize all inputs" comments with no data-flow evidence
- WPCS noise before security issues
- i18n blocker language for private plugins
- recommending broad rewrites when a localized fix is enough

## PR Preparation Notes

For actionable findings, preserve enough information for a later pull request:

- suggested branch name, usually `fix/<short-risk-area>` or the repository's existing convention
- commit theme or small commit sequence
- PR title in the repository's primary collaboration language
- PR body bullets covering problem, fix, and risk reduction
- test plan with exact commands and manual role/permission checks
- release notes or readme updates when security, WordPress.org readiness, i18n, privacy, or external service behavior changes

Keep PR notes scoped to the reviewed issue. Do not invent implementation details that were not verified in the code.
