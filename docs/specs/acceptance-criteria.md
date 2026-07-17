# Acceptance Criteria

**Module:** worklog-opsdevnz

---

## 0.0.1 Staging Complete When:

- [ ] Module package structure created under `src/worklog_opsdevnz/`
- [ ] `pyproject.toml` with correct metadata and dependencies
- [ ] Functional and non-functional requirements documented
- [ ] Design decision documented for Zensical blog integration (deferred)
- [ ] Prototype `scripts/worklog.py` from opsdev.nz reviewed and mapped to requirements
- [ ] Empty `src/worklog_opsdevnz/` package scaffolded
- [ ] Empty `tests/` directory scaffolded

## 0.0.2 MVP Complete When:

- [ ] `worklog-opsdevnz` (no args) creates today's worklog with YAML frontmatter and config-driven sections
- [ ] `-e` / `--editor` overrides the configured editor
- [ ] Config discovery walks up the tree, falls back to defaults
- [ ] Three structure modes work: flat, year, year-month
- [ ] Filename follows `DD-MM-YYYY-{suffix}.md` (year/month modes) or `YYYY-MM-DD-{suffix}.md` (flat)
- [ ] Tests cover config loading, path resolution, frontmatter generation

## 0.1.0 MVP Complete When:

- [x] `init` command generates valid `worklog.toml` (deferred)
- [x] Published to PyPI as `worklog-opsdevnz`
- [x] Published to `public/opsdev.nz/modules/` as 4th submodule
- [x] Automated release pipeline with Test PyPI gate (NFR-8)

## 0.1.1 Config Discovery Fix When:

- [x] Cwd-first config search (fix parent-first bug in `config.py`)
- [x] Tests updated for new search order
- [x] Backward compatibility confirmed: standalone repos unaffected

## 0.1.3 Custom Template When:

- [x] `template` field in `worklog.toml` renders when set
- [x] `{{DATE}}` and `{{TITLE}}` placeholders substituted
- [x] Template path resolved relative to config file
- [x] Template file not found → error
- [x] No template field → falls back to sections body
- [x] Frontmatter always generated (templates only affect body)

## 0.2.1 Previous Entry Flag When:

- [ ] `-p` / `--previous` opens the most recent worklog entry before today
- [ ] Discovery works across `flat`, `year`, and `year-month` structure modes
- [ ] `-p` does not create a new file — only opens existing entries
- [ ] No previous entries found → message to stderr, exit code 0
- [ ] `-p` combined with `-e` applies editor override to the previous entry
