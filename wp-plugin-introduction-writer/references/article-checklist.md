# WordPress Plugin Article Checklist

Use this checklist when preparing a WordPress plugin introduction article.

## Research

- Confirm the canonical plugin name, slug, and official URL.
- Check the latest visible version, last update date, tested WordPress version, required WordPress version, required PHP version, license, and maintainer.
- Review the plugin's official description, screenshots, FAQ, changelog, support docs, and pricing or plan limits.
- For repository-based plugins, inspect the main plugin header, README, package/composer metadata, changelog, and activation/setup code.
- Look for operational signals: update frequency, unresolved support issues, known compatibility notes, required services, database changes, cron/background processing, REST/Ajax endpoints, blocks, shortcodes, and uninstall behavior.
- If recommending the plugin, check whether there are security advisories, major unresolved bugs, or recent ownership/support changes.

## Reader-Fit Questions

- What reader problem does this plugin solve?
- Is the reader likely a non-technical site owner, a WordPress implementer, or a developer?
- What does the reader need to decide after reading: try it, install it, compare it, avoid it, or configure it better?
- What knowledge should not be assumed?
- What setup steps might fail in a normal WordPress site?

## Useful Article Sections

- Why this plugin matters now
- What the plugin can do
- When it is a good fit
- When another approach may be better
- Installation and initial setup
- Settings that deserve attention
- Example workflow or expected output
- Compatibility, pricing, and maintenance notes
- Caveats from hands-on testing or source review
- References

## Hands-On Verification

When a local plugin environment is available, prefer observed behavior over description-only writing:

- Install and activate the plugin.
- Confirm the admin menu, settings screen, block, shortcode, widget, REST endpoint, or front-end output that the article describes.
- Capture exact setting labels or UI names only after seeing them.
- Verify deactivation/uninstall caveats only when safe to do so.
- Record the environment: WordPress version, PHP version, theme, and plugin version.

## Claim Hygiene

- Do not state "free", "lightweight", "secure", "SEO-friendly", "fast", or "easy" as fact unless supported by evidence or framed as an impression.
- Distinguish official features from practical recommendations.
- Mention paid features only after verifying current plan boundaries.
- Avoid ranking a plugin above competitors without explicit comparison criteria.
- Keep warnings concrete: describe the condition, impact, and what the reader should check.

## Final Self-Check

- The article explains what the plugin helps the reader accomplish, not just what features it has.
- Key facts are sourced from official or high-confidence references.
- Caveats are visible enough that the article does not read like promotion.
- Setup steps are plausible for the target reader.
- Links appear near the claims they support, plus a consolidated reference list when external sources are used.
- Final prose has been handled with `$olein-writing-style`.
