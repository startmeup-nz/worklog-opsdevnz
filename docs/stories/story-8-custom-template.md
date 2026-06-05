# Story 8: Custom Entry Template

**As a** developer who uses a custom worklog format different from the
built-in section headers,

**I want to** point `worklog.toml` at a Markdown template file that
defines the complete entry — frontmatter and body — with `{{DATE}}`,
`{{TITLE}}`, `{{AUTHOR}}`, and `{{TAGS}}` placeholders,

**so that** I can define my own worklog structure and add custom
frontmatter fields without being limited to the default "Focus /
Completed / Notes / Related / Next" sections.

---

## Acceptance Criteria

### AC-8.1: Template defines the complete entry

- [ ] Setting `template = "my-template.md"` in `worklog.toml` makes the tool
      use that file for the *complete* worklog entry — both frontmatter and
      body — instead of the built-in defaults.
- [ ] The template path is resolved relative to the directory containing
      `worklog.toml` (same as `worklog_dir` resolution).
- [ ] If no `template` field is set, the tool uses the built-in frontmatter
      and `[[sections]]` body (unchanged behaviour).

### AC-8.2: Placeholder substitution

- [ ] `{{DATE}}` in the template is replaced with the entry date in
      ISO format (`2026-06-05`).
- [ ] `{{TITLE}}` in the template is replaced with `"Work Log - {date}"`.
- [ ] `{{AUTHOR}}` in the template is replaced with the `author` value from
      config, or `"unknown"` if not set.
- [ ] `{{TAGS}}` in the template is replaced with the `default_tags` from
      config as a block-style YAML list, or `[]` if not set.
- [ ] Placeholders are case-sensitive — `{{date}}`, `{{title}}`, etc. are
      not substituted.

### AC-8.3: Template file handling

- [ ] If the template file does not exist, the tool prints an error to
      stderr and exits with a non-zero code.
- [ ] The tool does not auto-generate or prepend any frontmatter —
      the template is the complete entry.

### AC-8.4: Custom frontmatter fields

- [ ] Users may include any additional YAML frontmatter fields in the
      template (e.g. `mood`, `client`, `project`), and they appear in
      the generated entry unchanged.

---

## Example

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

## Priority

| Field | Value |
|-------|-------|
| **Priority** | Medium |
| **Version Target** | 0.2.0 |
| **Dependencies** | Full-entry template design decision — see `docs/design/custom-template.md` |
| **Spec Reference** | FR-6 |

---

*Created: 2026-05-26*
