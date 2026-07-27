# Project Profiles and Scaffold Levels

## Profile Selection

Select one primary profile after inspecting the repository. Use `mixed` only when the repository intentionally contains multiple independently distributed WordPress projects.

### Plugin

Detect a PHP file with a valid `Plugin Name` header.

Baseline:

- map the project through `.wp-env.json` `plugins`
- run container commands with `--env-cwd=wp-content/plugins/<slug>`
- load the main plugin file in integration-test bootstrap when the test database does not activate it
- include plugin headers and uninstall behavior in smoke checks when relevant

### Block Plugin

Detect a plugin header plus one or more `block.json` files.

Add only when source JavaScript or CSS exists:

- `@wordpress/scripts`
- build, lint-js, lint-style, format, and unit-test scripts as needed
- browser tests for editor registration, save behavior, dynamic rendering, or front-end interactions

Do not create a JavaScript build pipeline for a PHP-only dynamic block that has no source assets.

### Classic Theme

Detect a valid `Theme Name` header in root `style.css`.

Baseline:

- map the project through `.wp-env.json` `themes`
- run container commands with `--env-cwd=wp-content/themes/<slug>`
- activate or switch to the theme explicitly for environment and integration tests
- lint PHP templates and functions

Add browser tests only for behaviors that cannot be verified through PHP rendering or focused unit tests.

### Block Theme

Detect `theme.json` and block templates, with or without a `style.css` header while the project is being initialized.

Baseline:

- apply the theme profile
- validate JSON syntax and the intended `theme.json` schema/version
- inspect templates, parts, and patterns
- include PHP tooling only when PHP files exist

Do not add PHPUnit merely to test static JSON or HTML files. Prefer schema validation, linting, and E2E checks for editor-visible behavior.

### Mixed or Monorepo

Do not assume the repository root can be mounted as one plugin or theme. Identify package boundaries and choose one of:

- separate `.wp-env.json` files per package
- a repository-level config using explicit `mappings`
- package-specific scripts that pass `--config`

Avoid duplicating Composer and npm dependencies when the repository already manages them centrally.

## Scaffold Levels

### Minimal

Use for prototypes, tiny private projects, or a user request limited to local environment and coding standards.

Include:

- project-local `@wordpress/env`
- `.wp-env.json`
- environment npm scripts
- project-local PHPCS/WPCS when PHP exists
- `phpcs.xml.dist`
- `.editorconfig` only when absent and useful

### Standard

Use by default for maintained projects.

Include Minimal, plus applicable items:

- PHPUnit pure unit or WordPress integration tests
- PHPStan with WordPress-aware extensions
- JavaScript lint/build/test through `@wordpress/scripts`
- focused GitHub Actions checks when the repository uses GitHub
- `.distignore` or equivalent release exclusions when distribution is expected

Add each item only when the codebase contains behavior it can validate.

### Full

Use for public, commercial, complex, or release-critical projects.

Include Standard, plus applicable items:

- Playwright E2E coverage
- supported PHP/WordPress compatibility matrix
- multisite verification
- Plugin Check for distributable plugins
- theme-specific validation for distributable themes
- POT generation and i18n checks
- deterministic release ZIP creation
- optional Xdebug or profiling commands

Do not introduce Full automatically. Confirm the added maintenance cost and CI duration are acceptable.
