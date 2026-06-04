# Functional Requirements

**Module:** worklog-opsdevnz  
**Module Version:** see `pyproject.toml`

---

## FR-1: Worklog Entry Creation

### FR-1.1: Basic Creation

*Requirements in FR-1.1, FR-1.1.A, and FR-1.1.B describe the default entry
creation behaviour when no `template` is configured. When a template is
configured, the template defines the complete entry (see FR-6).*

- **FR-1.1.1**: Tool MUST create a new Markdown file with YAML frontmatter containing
  `title`, `date`, `author`, `tags`, and `draft` fields
- **FR-1.1.2**: Tool MUST target today's date by default
- **FR-1.1.3**: Tool MUST NOT overwrite existing entries — if a file already exists for the
  given date, it MUST open the existing file instead

### FR-1.1.A: Frontmatter Format (default, no template)

- **FR-1.1.A.1**: Frontmatter MUST use YAML format delimited by `---` markers
- **FR-1.1.A.2**: `title` field MUST follow the pattern `"Work Log - {date}"`
- **FR-1.1.A.3**: `date` field MUST be ISO 8601 format (`YYYY-MM-DD`)
- **FR-1.1.A.4**: `author` field MUST come from `worklog.toml` config
- **FR-1.1.A.5**: `tags` field MUST be a YAML list from `default_tags` in config
- **FR-1.1.A.6**: `draft` field MUST default to `false`

### FR-1.1.B: Body Generation (default, no template)

- **FR-1.1.B.1**: Tool MUST generate section headers from the `sections` list in config
- **FR-1.1.B.2**: Each section MUST be an H2 heading (`## Title`)
- **FR-1.1.B.3**: Sections MUST appear in the order defined in config
- **FR-1.1.B.4**: A blank line MUST separate frontmatter from the first section heading

---

## FR-2: Per-Project Configuration

### FR-2.1: Config Discovery

- **FR-2.1.1**: Tool MUST search for `worklog.toml`, `worklog.yaml`, or `worklog.yml`
  starting from the current working directory, checking it first, then walking up
  through parent directories until a config file is found or the filesystem root
  is reached
- **FR-2.1.2**: Tool MUST use the nearest config file found (closest to cwd). If
  multiple configs exist between cwd and root, the first one encountered during
  the walk-up is used
- **FR-2.1.3**: If no config file is found, tool MUST use built-in defaults
- **FR-2.1.4**: Relative `worklog_dir` paths MUST be resolved against the config file's
  parent directory, not the current working directory

### FR-2.2: Configuration Schema

The `worklog.toml` file supports the following fields:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `worklog_dir` | string | No | `"docs/worklog"` | Base directory for worklog files (relative paths resolved against config file's parent directory) |
| `structure` | string | No | `"year"` | Directory structure: `"flat"`, `"year"`, `"year-month"` |
| `suffix` | string | No | `"worklog"` | Filename suffix (e.g. `23-05-2026-worklog.md`) |
| `author` | string | No | `$USER` or `"unknown"` | Default author name |
| `default_tags` | list | No | `["internal", "log"]` | Default YAML tags |
| `editor` | string | No | (unset) | Preferred editor command (e.g. `"nvim"`, `"code"`). Overridden by `-e`/`--editor` CLI flag and `$VISUAL`/`$EDITOR` env vars |
| `template` | string | No | (unset) | Path to a custom Markdown template defining the complete entry, including frontmatter. Supports `{{DATE}}`, `{{TITLE}}`, `{{AUTHOR}}`, `{{TAGS}}` placeholders |
| `sections` | list | No | (see defaults) | Ordered section headers |

### FR-2.3: Config Initialisation *(0.1.0+)*

- **FR-2.3.1**: `worklog-opsdevnz init` MUST create a `worklog.toml` in the current directory
- **FR-2.3.2**: Tool MUST NOT overwrite an existing config file
- **FR-2.3.3**: Generated config MUST include all default fields with commented explanations

---

## FR-3: Directory Structure Modes

### FR-3.1: Flat Mode (`structure = "flat"`)

- **FR-3.1.1**: All worklog files placed directly in `worklog_dir`
- **FR-3.1.2**: Filename: `YYYY-MM-DD-{suffix}.md` (year first to sort correctly)

### FR-3.2: Year Mode (`structure = "year"`) — default

- **FR-3.2.1**: Files placed in `worklog_dir/YYYY/`
- **FR-3.2.2**: Filename: `DD-MM-YYYY-{suffix}.md`
- **FR-3.2.3**: Example: `docs/worklog/2026/23-05-2026-worklog.md`

### FR-3.3: Year-Month Mode (`structure = "year-month"`)

- **FR-3.3.1**: Files placed in `worklog_dir/YYYY/MM/`
- **FR-3.3.2**: Filename: `DD-MM-YYYY-{suffix}.md`
- **FR-3.3.3**: Example: `docs/worklog/2026/05/23-05-2026-worklog.md`

---

## FR-4: Editor Integration

### FR-4.1: Editor Resolution

- **FR-4.1.1**: Tool MUST check for editor in this order:
  1. `-e` / `--editor` CLI argument
  2. `editor` field in `worklog.toml` config
  3. `$VISUAL` environment variable
  4. `$EDITOR` environment variable
- **FR-4.1.2**: If no editor is configured, tool MUST print the file path and exit cleanly
- **FR-4.1.3**: Tool MUST resolve the editor command via `shutil.which()` and report
  if not found in PATH

### FR-4.2: File Opening

- **FR-4.2.1**: Tool MUST invoke the editor with the worklog file path as argument
- **FR-4.2.2**: Tool MUST wait for the editor process to complete before exiting

---

## FR-5: CLI Interface

### FR-5.1: Command

`worklog-opsdevnz` — create or open today's worklog (default, no args required).

### FR-5.2: Global Options

| Option | Description |
|--------|-------------|
| `-e`, `--editor` | Override editor command for this run |
| `--version` | Print the installed version and exit |

### FR-5.3: Error Handling

- **FR-5.3.1**: File write failures MUST produce a clear error message and non-zero exit
- **FR-5.3.2**: All errors MUST write to stderr

### FR-5.4: Version Reporting

- **FR-5.4.1**: `--version` MUST print the installed version to stdout and exit with code 0
- **FR-5.4.2**: Version MUST be read from installed package metadata via
  `importlib.metadata.version()` to avoid duplicating the version string across files
- **FR-5.4.3**: If package metadata is unavailable (e.g. local editable install), the tool
  MUST fall back to a `"0.0.0+local"` placeholder

---

## FR-6: Custom Template

### FR-6.1: Full-Entry Template

- **FR-6.1.1**: When `template` is set in `worklog.toml`, the template file defines the
  *complete* worklog entry, including both YAML frontmatter and body. The tool MUST NOT
  auto-generate or prepend any frontmatter of its own.
- **FR-6.1.2**: If no `template` field is configured, the tool MUST use the built-in
  default (config-driven frontmatter and sections from the `sections` list).

### FR-6.2: Placeholder Substitution

- **FR-6.2.1**: Template files MAY use `{{DATE}}` and `{{TITLE}}` placeholders, which the
  tool replaces with the current date and a title derived from the entry date.
- **FR-6.2.2**: Template files MAY use `{{AUTHOR}}` to pull the `author` value from
  config. If no `author` is set in config, `{{AUTHOR}}` substitutes `"unknown"`.
- **FR-6.2.3**: Template files MAY use `{{TAGS}}` to pull the `default_tags` from config
  as a YAML-formatted list. If no `default_tags` is set, `{{TAGS}}` substitutes an empty
  list `[]`.
- **FR-6.2.4**: All placeholders are case-sensitive — `{{date}}`, `{{title}}`, etc. are
  not substituted.

### FR-6.3: Template File Handling

- **FR-6.3.1**: The template path is resolved relative to the directory containing
  `worklog.toml` (same as `worklog_dir` resolution).
- **FR-6.3.2**: If the template file does not exist, the tool MUST print an error to
  stderr and exit with a non-zero code.
- **FR-6.3.3**: The template MUST be a valid Markdown file. The tool MUST treat the
  entire file content as the template — no sections or frontmatter are auto-generated.

**Example:**

`worklog.toml`:
```toml
author = "opsdev"
default_tags = ["dev", "log"]
template = "my-worklog-template.md"
```

`my-worklog-template.md`:
```markdown
---
title: "{{TITLE}}"
date: {{DATE}}
author: {{AUTHOR}}
tags: {{TAGS}}
mood: creative
project: outcome-engineering
draft: false
---

# {{TITLE}}

**Date:** {{DATE}}

Write whatever you want here — no predefined sections.
```
