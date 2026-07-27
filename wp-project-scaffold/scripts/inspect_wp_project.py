#!/usr/bin/env python3
"""Inspect a WordPress plugin or theme project without modifying it."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


IGNORED_DIRS = {
    ".git",
    ".wp-env",
    "build",
    "dist",
    "node_modules",
    "vendor",
}

CONFIG_FILES = (
    ".distignore",
    ".editorconfig",
    ".gitignore",
    ".wp-env.json",
    ".wp-env.override.json",
    "composer.json",
    "package.json",
    "phpcs.xml",
    "phpcs.xml.dist",
    "phpstan.neon",
    "phpstan.neon.dist",
    "phpunit.xml",
    "phpunit.xml.dist",
    "theme.json",
)


def read_prefix(path: Path, size: int = 16384) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:size]
    except OSError:
        return ""


def header_value(content: str, field: str) -> str | None:
    match = re.search(
        rf"^[ \t/*#@]*{re.escape(field)}\s*:\s*(.+?)\s*$",
        content,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    return match.group(1).strip(" \t*/") if match else None


def visible_files(root: Path, pattern: str) -> list[Path]:
    results: list[Path] = []
    for path in root.rglob(pattern):
        if any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file():
            results.append(path)
    return sorted(results)


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return None, str(error)
    if not isinstance(data, dict):
        return None, "top-level JSON value is not an object"
    return data, None


def object_value(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key, {})
    return value if isinstance(value, dict) else {}


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def inspect(root: Path) -> dict[str, Any]:
    # WordPress only recognizes a plugin bootstrap in the plugin root. Restrict
    # header detection accordingly so fixture and example files do not misclassify
    # an otherwise unrelated repository.
    php_files = sorted(path for path in root.glob("*.php") if path.is_file())
    plugin_entries = []
    for path in php_files:
        name = header_value(read_prefix(path), "Plugin Name")
        if name:
            plugin_entries.append({"file": relative(root, path), "name": name})

    style_path = root / "style.css"
    theme_name = (
        header_value(read_prefix(style_path), "Theme Name")
        if style_path.exists()
        else None
    )
    has_theme_json = (root / "theme.json").is_file()
    has_block_templates = any(
        path.suffix == ".html"
        for directory in (root / "templates", root / "parts")
        if directory.is_dir()
        for path in directory.rglob("*.html")
    )
    block_files = visible_files(root, "block.json")

    if plugin_entries and block_files:
        profile = "block-plugin"
    elif plugin_entries:
        profile = "plugin"
    elif theme_name and has_theme_json and has_block_templates:
        profile = "block-theme"
    elif theme_name:
        profile = "classic-theme"
    elif has_theme_json and has_block_templates:
        profile = "block-theme"
    else:
        profile = "unknown"

    package, package_error = load_json(root / "package.json")
    composer, composer_error = load_json(root / "composer.json")

    npm_scripts = sorted(object_value(package or {}, "scripts"))
    composer_scripts = sorted(object_value(composer or {}, "scripts"))
    composer_require = {
        **object_value(composer or {}, "require"),
        **object_value(composer or {}, "require-dev"),
    }
    package_dependencies = {
        **object_value(package or {}, "dependencies"),
        **object_value(package or {}, "devDependencies"),
    }

    test_dirs = [
        path
        for path in ("tests", "test", "tests/phpunit", "tests/e2e", "tests/js")
        if (root / path).is_dir()
    ]
    workflows = (
        sorted(path.name for path in (root / ".github" / "workflows").glob("*.y*ml"))
        if (root / ".github" / "workflows").is_dir()
        else []
    )

    warnings = []
    if profile == "unknown":
        warnings.append("Could not confidently detect a WordPress project profile.")
    if package_error:
        warnings.append(f"package.json could not be parsed: {package_error}")
    if composer_error:
        warnings.append(f"composer.json could not be parsed: {composer_error}")
    if (root / ".wp-env.json").exists() and "@wordpress/env" not in package_dependencies:
        warnings.append(".wp-env.json exists but @wordpress/env is not a local dependency.")
    if any((root / name).exists() for name in ("phpcs.xml", "phpcs.xml.dist")):
        if "wp-coding-standards/wpcs" not in composer_require:
            warnings.append("PHPCS configuration exists but WPCS is not declared in Composer.")

    return {
        "root": str(root),
        "profile": profile,
        "project": {
            "plugin_entries": plugin_entries,
            "theme_name": theme_name,
            "block_json": [relative(root, path) for path in block_files],
            "has_theme_json": has_theme_json,
            "has_block_templates": has_block_templates,
        },
        "configuration": {
            name: (root / name).exists() for name in CONFIG_FILES
        },
        "tooling": {
            "npm_scripts": npm_scripts,
            "composer_scripts": composer_scripts,
            "npm_dependencies": sorted(package_dependencies),
            "composer_dependencies": sorted(composer_require),
            "test_directories": test_dirs,
            "github_workflows": workflows,
        },
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect WordPress project type and development tooling."
    )
    parser.add_argument(
        "project_root",
        nargs="?",
        default=".",
        help="Plugin or theme root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Emit compact JSON instead of indented JSON.",
    )
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve()
    if not root.is_dir():
        print(f"error: project root is not a directory: {root}", file=sys.stderr)
        return 2

    result = inspect(root)
    indent = None if args.compact else 2
    print(json.dumps(result, ensure_ascii=False, indent=indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
