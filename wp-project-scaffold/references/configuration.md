# Configuration Guide

## Contents

- Existing Repository Merge Policy
- wp-env
- npm
- Composer and WPCS
- PHPStan
- JavaScript Tooling
- CI
- Release Tooling

## Existing Repository Merge Policy

Before editing, inventory the existing keys and commands. Preserve:

- `name`, package type, autoloading, repositories, config, and plugin permissions in Composer
- package manager, engines, workspaces, dependencies, and unrelated npm scripts
- existing PHPCS rules, exclusions, test bootstrap behavior, and CI conventions

When a proposed command name already exists, use the repository’s command or choose a clearly scoped name. Do not change dependency ranges merely to normalize formatting.

## wp-env

Prefer a local `@wordpress/env` development dependency.

Use this shape for a plugin:

```json
{
  "$schema": "https://schemas.wp.org/trunk/wp-env.json",
  "plugins": ["."],
  "config": {
    "WP_DEBUG": true,
    "SCRIPT_DEBUG": true
  }
}
```

For a theme, replace `plugins` with `themes`. Add a lifecycle command to activate the theme only when it is idempotent.

Use a separate file such as `test.wp-env.json` for an isolated environment:

```json
{
  "$schema": "https://schemas.wp.org/trunk/wp-env.json",
  "plugins": ["."],
  "port": 8889
}
```

Do not use deprecated `testsEnvironment`. Avoid fixed ports when the repository already has a port convention; `autoPort` is useful locally but CI behavior differs.

Recommended npm commands, adapted to existing conventions:

```json
{
  "scripts": {
    "env:start": "wp-env start",
    "env:stop": "wp-env stop",
    "env:status": "wp-env status",
    "env:logs": "wp-env logs",
    "env:cli": "wp-env run cli wp"
  }
}
```

Add `env:reset` or `env:destroy` only when requested, and make their destructive behavior obvious.

For container Composer/PHPUnit commands, calculate the mounted path from the profile and slug:

```text
wp-env run cli --env-cwd=wp-content/plugins/<slug> composer <args>
wp-env run cli --env-cwd=wp-content/themes/<slug> phpunit <args>
```

## npm

Respect the existing lockfile:

- `package-lock.json`: npm
- `pnpm-lock.yaml`: pnpm
- `yarn.lock`: Yarn

Do not add a second lockfile. Do not install globally. Preserve the project’s Node engine constraints and prefer an active or maintenance LTS Node release compatible with selected WordPress packages.

## Composer and WPCS

Use project-local development dependencies:

- `wp-coding-standards/wpcs`
- its Composer installer when required by the selected WPCS setup
- `phpcompatibility/phpcompatibility-wp` only when supported PHP-range checks are wanted

Select versions compatible with the project’s PHP constraint. Ensure Composer plugin permissions are explicit where current Composer requires them.

Create or merge `phpcs.xml.dist` with:

- project-specific source paths rather than blind repository-root scanning
- exclusions for `vendor`, `node_modules`, generated builds, coverage, and third-party assets
- `WordPress` or a justified narrower ruleset
- the real text domain and function prefix/namespace when known
- `testVersion` only when PHPCompatibilityWP is configured

Provide scripts such as:

```json
{
  "scripts": {
    "lint": "phpcs",
    "format": "phpcbf"
  }
}
```

Do not run `phpcbf` over an existing project unless formatting changes are in scope.

## PHPStan

Add PHPStan only when PHP behavior justifies static analysis. Prefer a WordPress-aware extension and a conservative initial level. Include:

- actual source paths
- bootstrap/stub files only when required
- generated and third-party exclusions

Use a baseline only for an existing project with significant current debt. Do not use a baseline to hide new errors.

## JavaScript Tooling

Use `@wordpress/scripts` when the project builds blocks or WordPress-facing JavaScript. Add only applicable scripts:

- `build`
- `start`
- `lint:js`
- `lint:css`
- `format`
- `test:unit:js`

Preserve custom webpack, Jest, Babel, ESLint, or Stylelint configuration. Do not replace a working custom toolchain solely for uniformity.

## CI

Follow the repository’s CI provider. For GitHub Actions, use existing setup actions and cache conventions.

Order fast feedback first:

1. configuration validation
2. PHPCS
3. PHPStan
4. PHP tests
5. JavaScript lint/test/build
6. E2E

Use a PHP matrix only across declared supported versions. Test the lowest supported dependency set when compatibility matters, but do not add a large matrix without release justification.

## Release Tooling

For distributed projects, exclude development-only files and dependencies using `.distignore` or the existing packaging mechanism. Verify the archive contents, main entry file, text domain, license files, and built assets.

Add Plugin Check, theme validation, POT generation, or ZIP creation only for the applicable distribution target. Never package secrets, local override files, test databases, coverage, `node_modules`, or development-only Composer dependencies.
