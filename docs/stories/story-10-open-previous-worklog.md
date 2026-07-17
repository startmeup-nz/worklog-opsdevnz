# Story 10: Open Previous Worklog

**As a** developer returning to a project after a break,  
**I want to** open my most recent worklog entry with a simple flag,  
**so that** I can pick up where I left off without navigating directories
or remembering which date I last wrote.

## Acceptance Criteria

- [ ] `worklog-opsdevnz -p` opens the most recent worklog entry before today
- [ ] `worklog-opsdevnz --previous` works as the long-form alias
- [ ] If today's entry already exists, `-p` still opens the entry *before*
  today (the actual previous one, not today's)
- [ ] If no previous entries are found (first use, empty directory), the
  tool prints a clear message to stderr and exits with code 0
- [ ] Discovery respects the configured `structure` mode (`flat`, `year`,
  `year-month`) and `suffix` — it looks in the same directory tree that
  `worklog-opsdevnz` (no args) writes to
- [ ] `-p` does NOT create a new file — it only opens existing entries
- [ ] When combined with `-e` / `--editor`, the editor override applies to
  the previous entry the same way it would for today's

## Boundaries

| In scope | Out of scope |
|----------|-------------|
| Open the single most recent entry before today | Listing entries (`list` command — Story 3) |
| Discovery via configured structure + suffix | Searching by tag, author, or content |
| No creation — open-only | Creating entries for past dates (Story 5) |
| Works with all three structure modes | Custom filename patterns beyond the suffix |

---

| Field | Value |
|-------|-------|
| **Priority** | Medium |
| **Version Target** | 0.2.1 |

*Created: 2026-07-18*
