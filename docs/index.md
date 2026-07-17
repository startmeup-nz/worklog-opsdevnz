# worklog-opsdevnz

Configurable CLI tool for creating and managing dated development worklogs.

- **Status:** Development
- **License:** Apache 2.0
- **Python:** 3.14+

## Overview

Across multiple projects, teams kept reinventing the same pattern: a script that
creates a dated Markdown file from a template, with YAML frontmatter for date,
author, tags, and draft status. Each implementation had slightly different
directory structures, section headers, and filenames, but the core concept was
always the same.

`worklog-opsdevnz` formalises this pattern into a single reusable module.
Install it once, configure it per project, and start logging.

## Quick Start

```bash
# Install (development)
uv pip install -e .

# Create today's worklog
worklog-opsdevnz

# Show version
worklog-opsdevnz --version

# Override the editor for this run
worklog-opsdevnz --editor nvim

# Open the most recent previous entry
worklog-opsdevnz -p
```

## Configuration

Each project gets a `worklog.toml` at its root:

```toml
worklog_dir = "docs/worklog"
structure = "flat"           # "flat", "year", or "year-month"
filename_pattern = "{date}-{slug}.md"
author = "Your Name"
default_tags = ["worklog", "log"]

[[sections]]
title = "🎯 Focus"

[[sections]]
title = "✅ Completed"

[[sections]]
title = "🧠 Notes"

[[sections]]
title = "⏳ Next"
```

## Directory Structure

The tool supports three directory layouts, configured per project:

| Mode | Layout | Best For |
|------|--------|----------|
| `flat` | `docs/worklog/2026-04-28-slug.md` | Occasional logging (< 20 entries) |
| `year` | `docs/worklog/2026/2026-04-28-slug.md` | Moderate logging (default) |
| `year-month` | `docs/worklog/2026/04/2026-04-28-slug.md` | Daily logging |

## Documentation

- **[Specifications](specs/)** — Functional and non-functional requirements
- **[Non-Functional Requirements](specs/NFR.md)** — Code quality and design guidelines
- **[Release Process](release-process.md)** — Trusted Publishing (OIDC) and CI/CD pipeline
- **[User Stories](stories/README.md)** — Persona-driven acceptance criteria
- **[Design Decisions](design/README.md)** — Architecture choices and rationale

## Development

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Lint
uv run ruff check src/

# Serve documentation
uv run zensical serve
```

## Related

- [OpsDev.nz Collective](https://opsdev.nz) — Parent project
- [GitHub Repository](https://github.com/startmeup-nz/worklog-opsdevnz) — Source code
