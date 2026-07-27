---
name: wp-project-scaffold
description: Build or improve a reliable development foundation for WordPress plugins, classic themes, block themes, and block-based projects. Use when Codex is asked to scaffold a new WordPress project, add wp-env, configure project-local PHPCS and WPCS, introduce PHPUnit or integration tests, add PHPStan, configure WordPress JavaScript tooling, create CI checks, or standardize an existing plugin or theme repository without overwriting its conventions.
---

# WP Project Scaffold

## Goal

Create the smallest maintainable WordPress development foundation that satisfies the project’s actual needs. Support both new and existing repositories. Preserve working configuration, user changes, package-manager choices, namespace conventions, and supported version ranges.

## Core Workflow

1. Inspect the repository before proposing files:
   - read `AGENTS.md` and repository instructions
   - resolve the bundled script from this skill directory, then run `python3 <skill-dir>/scripts/inspect_wp_project.py <project-root>`; do not assume the target repository contains the script
   - inspect the detected entry files and existing `composer.json`, `package.json`, `.wp-env.json`, `phpcs.xml*`, `phpunit.xml*`, test directories, and CI workflows
   - use `rg` and `rg --files`; do not scan generated dependency directories
2. Determine the project profile and scaffold level:
   - read `references/profiles.md`
   - infer plugin, block plugin, classic theme, block theme, or mixed project
   - default to `standard` when the user does not specify a level
3. State the intended changes before installing dependencies:
   - distinguish files to create from files to merge
   - identify prerequisites such as Docker, Node.js, npm, Composer, and PHP
   - call out destructive environment commands separately
4. Implement incrementally:
   - merge JSON and XML configuration instead of replacing it
   - prefer project-local dependencies and repository scripts
   - preserve package manager and lockfile conventions
   - add only tooling justified by the selected profile and level
5. Validate proportionally:
   - validate configuration syntax first
   - install dependencies only when authorized
   - run focused lint and tests before broad suites
   - start `wp-env` only when Docker is available and environment mutation is in scope
6. Report:
   - selected profile and level
   - files created or changed
   - commands verified
   - prerequisites or commands left for the user

## Safety Rules

- Never overwrite an existing configuration file wholesale.
- Never run `wp-env reset`, `wp-env destroy`, database deletion, or volume deletion without explicit user authorization.
- Treat `.wp-env.override.json`, local ports, credentials, and developer-specific paths as local state; do not commit them unless requested.
- Do not install global npm, Composer, PHPCS, or WPCS packages. Prefer project-local development dependencies.
- Do not silently raise minimum PHP, WordPress, Node.js, PHPUnit, or Composer requirements.
- Do not introduce Git hooks or auto-fix-on-commit behavior unless requested.
- Do not claim an environment or test suite works unless the relevant command ran successfully.

## Configuration Rules

Read `references/configuration.md` before creating or changing wp-env, Composer, PHPCS/WPCS, npm, PHPStan, CI, or release configuration.

Apply these defaults:

- Use Docker-backed `wp-env` as the default runtime.
- Treat the Playground runtime as opt-in because its behavior and available commands differ.
- Add `$schema` to `.wp-env.json`.
- Map the current directory through `plugins` or `themes` according to the detected profile.
- Use a separate wp-env config file for isolated test environments; do not add deprecated `testsEnvironment`.
- Run Composer, PHPUnit, and WP-CLI through the `cli` container with the correct `--env-cwd` when container execution is selected.
- Use WPCS through Composer with a repository-owned `phpcs.xml.dist`.
- Resolve compatible dependency versions from the project’s declared PHP and WordPress support ranges. Do not copy stale version pins from examples.
- Verify current package compatibility through official documentation or package metadata when network access is available.

## Testing Rules

Read `references/testing.md` whenever the selected level includes tests.

- Distinguish pure PHP unit tests from WordPress integration tests.
- Use the WordPress PHPUnit files exposed by wp-env through `WP_TESTS_DIR` when tests run inside wp-env.
- Add one meaningful smoke test only when it exercises the project bootstrap or a real public behavior.
- Keep fixtures deterministic and do not depend on an existing developer database.
- Add JavaScript unit tests only when the project contains testable JavaScript behavior.
- Add E2E tests only for browser-dependent behavior such as admin screens, blocks, editor interactions, or front-end flows.
- Do not label integration tests as isolated unit tests.

## Verification Order

Run only commands supported by the resulting project:

1. Parse JSON, XML, YAML, and PHP configuration.
2. Run the inspection script again and review its warnings.
3. Run PHPCS/WPCS.
4. Run PHPStan when configured.
5. Run pure unit tests.
6. Run WordPress integration tests.
7. Run JavaScript lint, unit tests, and build.
8. Run E2E tests last.
9. Run packaging checks only when release tooling is in scope.

If dependency installation or Docker is unavailable, finish the file-level validation and clearly list the unverified runtime commands.

## Resources

- `scripts/inspect_wp_project.py`: read-only project detection and tooling inventory.
- `references/profiles.md`: project profiles and `minimal`, `standard`, and `full` levels.
- `references/configuration.md`: configuration decisions, command naming, merge rules, and optional tooling.
- `references/testing.md`: PHPUnit, WordPress integration, JavaScript, and E2E test guidance.
