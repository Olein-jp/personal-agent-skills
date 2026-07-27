# Testing Guide

## Contents

- Choose Test Boundaries
- Pure PHP Unit Tests
- WordPress Integration Tests
- Plugin Bootstrap
- Theme Bootstrap
- JavaScript Unit Tests
- E2E Tests
- Smoke Tests and Fixtures

## Choose Test Boundaries

Use the narrowest test that proves the behavior:

| Behavior | Preferred test |
| --- | --- |
| Pure value transformation or domain object | PHP unit |
| Hook registration, options, metadata, REST, database | WordPress integration |
| JavaScript state or utility behavior | JavaScript unit |
| Block editor, admin UI, browser navigation | E2E |
| Static `theme.json` or JSON metadata | schema/config validation |

Do not add every test type by default.

## Pure PHP Unit Tests

Use PHPUnit without loading WordPress for code that does not depend on WordPress globals, hooks, database access, or core classes. Keep these tests fast and runnable on the host when possible.

If mocks for WordPress functions become extensive, prefer an integration test or isolate the WordPress adapter from the domain logic. Optional mocking libraries must solve a concrete need.

## WordPress Integration Tests

When running inside wp-env, use its matching WordPress PHPUnit files:

```php
<?php

$_tests_dir = getenv( 'WP_TESTS_DIR' );

if ( ! $_tests_dir ) {
	fwrite( STDERR, "WP_TESTS_DIR is not set.\n" );
	exit( 1 );
}

require_once $_tests_dir . '/includes/functions.php';

// Add profile-specific bootstrap hooks here.

require $_tests_dir . '/includes/bootstrap.php';
```

Run from the mapped project directory so that `phpunit.xml.dist`, Composer autoloading, and relative paths resolve correctly. Use a separate wp-env config when test isolation from the developer site matters.

Keep `WP_TESTS_CONFIG_FILE_PATH` optional. Use it only when the bundled wp-env test configuration does not satisfy the project.

## Plugin Bootstrap

If the test installation does not activate the plugin, load the detected main plugin file before WordPress bootstrap:

```php
tests_add_filter(
	'muplugins_loaded',
	static function () {
		require dirname( __DIR__, 2 ) . '/plugin-slug.php';
	}
);
```

Adjust the path to the actual bootstrap location. Avoid loading the plugin twice; detect or control activation consistently.

For a smoke test, verify a meaningful registration or public behavior rather than asserting only that a constant exists.

## Theme Bootstrap

Ensure the theme is mounted in wp-env. Switch to its real stylesheet slug during test setup or bootstrap only when the relevant WordPress functions are available. Restore global state when an individual test changes themes.

Prefer integration tests for PHP hooks, setup support, patterns registered in PHP, and rendering callbacks. Use schema checks or E2E tests for static block-theme templates and Site Editor behavior.

## JavaScript Unit Tests

Use the repository’s existing test runner. With `@wordpress/scripts`, add Jest tests only for logic that can run meaningfully outside a browser.

Avoid snapshots for large editor trees. Prefer focused assertions on behavior, accessible labels, dispatched actions, and serialized attributes.

## E2E Tests

Add Playwright only when UI behavior is a release risk. Typical cases:

- block insertion, editing, save, and reload
- admin settings permissions and persistence
- front-end interactivity
- theme templates or style variations in the Site Editor

Make setup idempotent. Create content and users per test or controlled suite fixture. Do not depend on data in a developer’s existing environment. Capture traces/screenshots on failure in CI, not as committed output.

## Smoke Tests and Fixtures

A generated smoke test must:

- load the real project bootstrap
- assert one observable behavior
- avoid network requests
- avoid current time, locale, or random ordering unless controlled
- clean up options, posts, users, terms, and files it creates

Use WordPress factories for integration fixtures. Keep fixtures local to the test unless shared setup materially improves speed without coupling tests.
