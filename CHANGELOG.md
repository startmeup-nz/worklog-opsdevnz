# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] — 2026-06-05

### Added
- Full-entry custom template: when `template` is set, the template defines
  the *complete* worklog entry including YAML frontmatter. The tool no longer
  auto-generates or prepends frontmatter (FR-6.1, Story 8 revision).
- `{{AUTHOR}}` placeholder — pulls `author` from config, falls back to
  `"unknown"` (FR-6.2.2, Story 9).
- `{{TAGS}}` placeholder — renders `default_tags` as a block-style YAML
  list, falls back to `[]` (FR-6.2.3, Story 9).
- 8 new tests covering AUTHOR/TAGS placeholders, full-entry template,
  case-sensitivity, and edge cases.

### Changed
- `render_template()` now accepts a `config` dict for AUTHOR/TAGS substitution.
- **Breaking:** templates no longer receive auto-generated frontmatter —
  the template defines the full entry. Existing templates should be updated
  to include their own YAML frontmatter block.

### Fixed
- Trailing whitespace after `tags:` colon when `{{TAGS}}` substitution
  produces a leading newline — `render_template()` now strips trailing
  whitespace from every line.

## [0.1.3] — 2026-05-26

### Added
- `template` field in `worklog.toml` — point to a custom Markdown file for
  the worklog body, with `{{DATE}}` and `{{TITLE}}` placeholder substitution
  (FR-6, Story 8)
- 4 new tests covering template rendering, placeholder substitution, missing
  file errors, and frontmatter preservation

### Changed
- Template paths resolved relative to config file directory (consistent with
  `worklog_dir` resolution)

## [0.1.2] — 2026-05-26

### Fixed
- Config discovery now checks cwd first before walking up parent directories,
  fixing a bug where parent `worklog.toml` files could silently override
  project-local configs (#7, FR-2.1.1/2.1.2, Story 7)

### Added
- `test_find_config_nearest_wins` — verifies subdirectory config takes
  priority over parent config
- Security design doc (`docs/design/security-trust-model.md`) — config
  trust model, editor path warning, threat analysis
- Design doc for config discovery strategy
  (`docs/design/config-discovery-strategy.md`) — documents the cwd-first
  approach and why `.git` boundaries were rejected
- NFR-9: Security & Config Trust non-functional requirements

### Changed
- Specs modularized: README → index, FRs, acceptance criteria, and
  implementation status in separate files
- Stories extracted from inline README into individual files

## [0.1.1] — 2026-05-25

### Added
- `editor` field in `worklog.toml` config — preferred editor, overridden by
  `-e` flag, `$VISUAL`, and `$EDITOR`
- Tests for config-based editor resolution and CLI override behaviour

### Changed
- README refreshed — removed stale scope section, `--list`, and `--previous`;
  added editor config example and updated for 0.1.0 reality
- `-e`/`--editor` help text updated to reflect resolution order

## [0.1.0] — 2026-05-25

### Added
- Automated release pipeline: Test PyPI gate + smoke test → real PyPI via
  OIDC Trusted Publishing (NFR-8)
- `docs/release-process.md` — step-by-step Trusted Publishing setup guide

### Changed
- CI: `test.yml` and `publish.yml` now use `uv` for dependency management
- Repo visibility: made public for Trusted Publishing

## [0.0.5] — 2026-05-25

### Added
- `--version` flag: prints installed version via `importlib.metadata` (#5)
- Spec FR-5.4: version reporting requirements documented
- Test for `--version` output (version-agnostic)

### Fixed
- `worklog_dir` now resolves relative to config file location, not CWD — running from any
  subdirectory creates files in the correct project-relative path (#4)
- Config discovery always anchored relative paths to the current working directory; now
  relative `worklog_dir` values are resolved against the config file's parent directory

### Added
- Spec FR-2.1.4: documents `worklog_dir` resolution rule
- Regression test: `test_get_config_worklog_dir_resolved_relative_to_config`

## [0.0.3] — 2026-05-24

### Changed
- Narrowed MVP scope: defer `list`, `init`, `create` subcommands to 0.1.0+
- Removed `-p` / `--previous` flag — current scope is create/open today's worklog only
- Removed unused `rich` dependency
- Cleaned up documentation to match actual implemented behaviour
- Spec cleaned up: removed stale requirements, renumbered FR sections, marked 0.1.0+ items

### Fixed
- README.md broken code block and stale `--list` reference
- docs/index.md references to non-existent commands (`create`, `list`, `init`, `-d`, `-t`)
- Spec implementation status updated to reflect reality

### Added
- Agents.md — minimal module-specific guidance, self-contained

## [0.0.2] — 2026-05-24

### Added
- Click CLI: bare command creates today's worklog, `-p` for yesterday, `-e` for editor
- Config discovery: walks up from cwd for `worklog.toml`/`worklog.yaml`, falls back to defaults
- Path resolution: three structure modes (flat, year, year-month)
- Frontmatter + body generation from config-driven sections
- Editor resolution: CLI override → `$VISUAL` → `$EDITOR`
- 17 tests covering config, paths, template, CLI (89% coverage)

### Changed
- Migrated from prototype script to Click-based module
- Removed hardcoded version strings from docs — DRY via pyproject.toml

### Fixed
- Linting issues (unused imports, missing `Path` import)
- Generated `site/` directory accidentally tracked — removed and gitignored

## [0.0.1] — Unreleased

### Added
- Initial module scaffold from template-opsdevnz
- Worklog specs, stories, and design docs ported from incubation
- pyproject.toml with Click, PyYAML dependencies
- GitHub Actions CI (test on push/PR) and PyPI publish (on tag)
- Dependabot weekly pip updates
