# worklog-opsdevnz

Configurable CLI tool for creating and managing dated development worklogs.
Generates Markdown entries with YAML frontmatter from per-project templates.

## Quick Start

```bash
pip install worklog-opsdevnz

# Create today's worklog
worklog-opsdevnz

# Show installed version
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
structure = "year"           # "flat", "year", or "year-month"
author = "Your Name"
editor = "nvim"              # optional, overridden by -e / $VISUAL / $EDITOR
template = "my-template.md"  # optional custom body template
default_tags = ["worklog", "log"]

[[sections]]
title = "Focus for Today"

[[sections]]
title = "Completed"

[[sections]]
title = "Notes"

[[sections]]
title = "Next"
```

## Features

- Per-project configuration via `worklog.toml`
- Three directory structure modes: `flat`, `year`, `year-month`
- YAML frontmatter: date, author, tags, draft status
- Configurable section headers per project
- Custom body templates with `{{DATE}}` and `{{TITLE}}` placeholders
- Editor integration: `-e` flag → config → `$VISUAL` → `$EDITOR`
- `-p` / `--previous` flag to open the most recent past entry
- `--version` flag for installed version

## Requirements

- Python 3.12+
- See [pyproject.toml](pyproject.toml) for full dependencies

## Documentation

- [Release Process](docs/release-process.md)
- [Functional Requirements](docs/specs/README.md)
- [Non-Functional Requirements](docs/specs/NFR.md)
- [Design Decisions](docs/design/README.md)
- [User Stories](docs/stories/README.md)

## Related

- [PyPI](https://pypi.org/project/worklog-opsdevnz/)
- [GitHub](https://github.com/startmeup-nz/worklog_opsdevnz)
- [OpsDev.nz Collective](https://opsdev.nz)
