# Design Decision: Custom Template Scope — Full Entry vs. Body Only

**Status:** Proposal  
**Created:** 2026-06-05  
**Spec Reference:** FR-6, Story 8

---

## Problem Statement

Story 8 (custom template) shipped in v0.1.3 with the design that templates
control only the *body* of the worklog entry — frontmatter is always generated
by the tool. The template file uses `{{DATE}}` and `{{TITLE}}` placeholders.

However, a user creating a custom template naturally included YAML frontmatter
in it, expecting the template to define the full entry. The result was
duplicate frontmatter — the tool's auto-generated block plus the user's block
from the template.

The question: **Should a custom template define the full worklog entry
(frontmatter + body), or only the body?**

---

## Options Considered

### Option A: Body-only template (current design, documentation fix)

Template controls body content only. Frontmatter is always auto-generated.
The tool prepends frontmatter before writing the file.

**Template file:**
```markdown
# {{TITLE}}

**Date:** {{DATE}}

## Today's Focus
```

**Generated entry:**
```markdown
---
title: "Work Log - 2026-06-05"
date: 2026-06-05
author: opsdev
tags:
  - dev
  - log
draft: false
---

# Work Log - 2026-06-05

**Date:** 2026-06-05

## Today's Focus
```

**Pros:**
- Config-driven `author` and `tags` always present
- Consistent frontmatter format across entries
- No code change needed — just documentation

**Cons:**
- Counter-intuitive: `{{DATE}}` and `{{TITLE}}` are naturally frontmatter fields
- No way to add custom frontmatter fields (e.g. `mood`, `project`, `client`)
- Template files look incomplete — they lack the surrounding structure

**What would change:**
- Update Story 8 to explicitly state: "Templates control body only. Frontmatter
  is always auto-generated. Do not include YAML frontmatter in template files."
- Update the custom template example in `functional-requirements.md` to clarify

---

### Option B: Full-entry template

The template file defines the entire worklog — frontmatter + body. The tool
performs placeholder substitution across the whole file without prepending
anything.

**Template file:**
```markdown
---
title: "{{TITLE}}"
date: {{DATE}}
author: "User"
tags:
  - art
  - daily
mood: creative
project: wilde-studio
draft: false
---

# {{TITLE}}

**Date:** {{DATE}}

## Today's Focus
```

**Generated entry:**
```markdown
---
title: "Work Log - 2026-06-05"
date: 2026-06-05
author: "User"
tags:
  - art
  - daily
mood: creative
project: wilde-studio
draft: false
---

# Work Log - 2026-06-05

**Date:** 2026-06-05

## Today's Focus
```

**Pros:**
- Simple mental model: "your template = your file"
- Full control over frontmatter fields
- `{{DATE}}` and `{{TITLE}}` work everywhere, naturally
- No duplicate frontmatter

**Cons:**
- Loses config-driven `author`/`tags` injection — user must manage them in template
- Breaking change for any existing template users (none known yet — v0.1.3 just shipped)
- Template files are more verbose (must include the full `---` block)
- No `{{AUTHOR}}` or `{{TAGS}}` placeholder exists yet (could be added)

**What would change:**
- `generate_content()`: if template is set, return `render_template()` output
  directly — no auto-generated frontmatter prepended
- Add `{{AUTHOR}}` placeholder (or keep user managing `author` manually in template)
- Updated docs: "Template defines the entire entry, including YAML frontmatter"
- FR-6 revision: remove the "frontmatter always generated" constraint
- AC-8.4: replace with "If template is set, frontmatter comes from the template"

---

### Option C: Hybrid — merge / extend frontmatter

Tool generates base frontmatter (author, tags, draft), then detects if the
template also contains YAML frontmatter and merges the user's custom fields in.

**Template file:**
```markdown
---
mood: creative
project: wilde-studio
---

# {{TITLE}}

{{DATE}}
```

**Generated entry:**
```markdown
---
title: "Work Log - 2026-06-05"
date: 2026-06-05
author: opsdev
tags:
  - dev
  - log
draft: false
mood: creative
project: wilde-studio
---

# Work Log - 2026-06-05
2026-06-05
```

**Pros:**
- Best of both worlds: config base + template extras
- Backwards compatible with existing templates (no frontmatter → no merge needed)
- User adds only the custom fields they care about

**Cons:**
- Complex to implement: YAML parsing, merge logic, field conflict rules
- Magic behavior: user might not expect frontmatter to be merged
- YAML parsing introduces error cases (malformed frontmatter in template)
- Merging semantics unclear: do user fields override tool fields? vice versa?
- Template is neither body-only nor full-entry — ambiguous responsibility

**What would change:**
- Add YAML frontmatter extraction from template content
- Parse template's frontmatter, merge with auto-generated base, write merged result
- Template body = everything after the frontmatter `---` delimiter
- Define merge precedence: user fields override tool defaults? or tool fields
  always win for `title`, `date`, `author`, `tags`, `draft`?
- Significant code change — new merge logic + tests + error handling

---

### Option D: Config-driven extra frontmatter fields

Template stays body-only. User specifies extra frontmatter fields in
`worklog.toml` config instead of in the template file.

**worklog.toml:**
```toml
template = "my-template.md"
[frontmatter]
mood = "creative"
project = "wilde-studio"
```

**Generated entry:**
```markdown
---
title: "Work Log - 2026-06-05"
date: 2026-06-05
author: opsdev
tags:
  - dev
  - log
draft: false
mood: creative
project: wilde-studio
---

<body from template>
```

**Pros:**
- Explicit, no magic — user declares custom fields in config
- Template stays simple (body only)
- Config is version-controllable alongside the template
- Works with or without a custom template (just `[frontmatter]` alone adds fields)

**Cons:**
- Template still doesn't define its own frontmatter — separate concern in config
- Configuration grows (`[frontmatter]` section in `worklog.toml`)
- No inline control — if `mood` changes daily, user must edit config each time
- Doesn't solve Floyd's core expectation (template = full file control)

**What would change:**
- Add `[frontmatter]` section to config schema (optional, TOML table)
- Merge with auto-generated fields before writing
- Update `get_config()` to include extra frontmatter
- Template behavior unchanged — still body-only

---

## Comparison Matrix

| Criterion | A: Body-only | B: Full-entry | C: Hybrid merge | D: Config extra |
|-----------|:---:|:---:|:---:|:---:|
| Implementation effort | Trivial (docs only) | Small | Medium | Small |
| Breaking change | No | Minor (pre-1.0) | No | No |
| User controls frontmatter | No | Yes | Partial | Yes |
| Custom fields per entry | No | Yes (template per entry) | Yes (template per entry) | No (config is global) |
| Simple mental model | Moderate | High | Low | Moderate |
| Backwards compatible | Yes | Yes (no known users) | Yes | Yes |

---

## Recommendation

Option **B (full-entry template)** is the strongest design for the long term:

1. It matches what users naturally expect — the template is the file
2. It eliminates the duplicate frontmatter bug without special-casing
3. The breaking-change concern is minimal (v0.1.3 just shipped, no known
   template users beyond Floyd)
4. Mental model is the simplest: "template = your worklog file"

Option **A** is the fastest fix (update docs only) and could be adopted as an
intermediate step, but defers the underlying UX mismatch.

Option **C** and **D** add complexity without meaningfully improving the user
experience over B.

### Open Questions for B

- Should we add `{{AUTHOR}}` and/or `{{TAGS}}` placeholders so users can
  optionally pull these from config into their template?
- If `{{AUTHOR}}` is supported but not present in the template, should the
  tool warn? Or silently skip?
- Should the template path support `{{DATE}}` in the filename for
  date-specific templates? (e.g. `template-{{DATE}}.md`)

---

## Related

- [Story 8: Custom Entry Template](../stories/story-8-custom-template.md)
- [FR-6: Custom Template](../specs/functional-requirements.md#fr-6-custom-template)
- [GitHub Issue #13](https://github.com/startmeup-nz/worklog-opsdevnz/issues/13)
- [Current implementation: `template.py:generate_content()`](../../src/worklog_opsdevnz/template.py)
