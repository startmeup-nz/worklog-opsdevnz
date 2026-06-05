# Story 9: Custom Frontmatter Fields in Template

**As a** user who tracks extra context with each worklog entry,
**I want to** include additional YAML frontmatter fields (e.g. `mood`, `client`, `project`)
in my custom template,
**so that** I can record structured metadata beyond the built-in fields.

## Acceptance Criteria

### AC-9.1: Template defines full frontmatter

- [ ] When a custom `template` is configured, the template file defines the
      entire frontmatter block, including any custom fields the user chooses
- [ ] The tool does not auto-generate frontmatter when a template is used
- [ ] Existing `{{DATE}}` and `{{TITLE}}` placeholders are substituted in
      frontmatter fields, just as they are in the body

### AC-9.2: `{{AUTHOR}}` placeholder

- [ ] Templates MAY use `{{AUTHOR}}` to pull the `author` value from config
      into frontmatter or body
- [ ] If `{{AUTHOR}}` is used but no `author` is set in config, the tool
      substitutes `"unknown"` (matching existing default behaviour)
- [ ] `{{AUTHOR}}` is case-sensitive — `{{author}}` is not substituted

### AC-9.3: `{{TAGS}}` placeholder

- [ ] Templates MAY use `{{TAGS}}` to pull the `default_tags` from config
      into frontmatter or body as a block-style YAML list (each tag on its
      own indented line with `-` prefix)
- [ ] If `{{TAGS}}` is used but no `default_tags` is set, it substitutes
      an empty list `[]`

## Example

`worklog.toml`:
```toml
author = "opsdev"
default_tags = ["dev", "log"]
template = "my-template.md"
```

`my-template.md`:
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

## Today's Focus
```

Generated entry:
```markdown
---
title: "Work Log - 2026-06-05"
date: 2026-06-05
author: opsdev
tags:
  - dev
  - log
mood: creative
project: outcome-engineering
draft: false
---

# Work Log - 2026-06-05

**Date:** 2026-06-05

## Today's Focus
```

## Priority

| Field | Value |
|-------|-------|
| **Priority** | Medium |
| **Version Target** | 0.2.0 |
| **Dependencies** | Design decision on custom template scope — resolved: Option B (full-entry), see [custom-template.md](../design/custom-template.md) |
| **Spec Reference** | FR-6 (revision) |

---

*Created: 2026-06-05*
