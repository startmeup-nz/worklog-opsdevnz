# Design Decisions

This directory contains design decision records for worklog-opsdevnz.

Design decisions capture "how should we implement this?" before writing code.
They link to spec requirements and preserve the thought process.

---

## Design Documents

| Document | Status | Spec Reference | Description |
|----------|--------|----------------|-------------|
| [worklog-as-blog.md](worklog-as-blog.md) | Decision | FR-1, FR-5 | Zensical blog integration — deferred |
| [structure-modes.md](structure-modes.md) | Proposal | FR-3 | Directory structure mode selection |
| [config-discovery-strategy.md](config-discovery-strategy.md) | Decision | FR-2.1, Story 7 | Config file discovery approach — cwd-first walk-up bug fix |
| [security-trust-model.md](security-trust-model.md) | Decision | FR-2.1, Story 7, NFR-9 | Config trust model, editor path validation, threat analysis |
| [custom-template.md](custom-template.md) | Proposal | FR-6, Story 8, Story 9 | Custom template scope — full-entry vs body-only |

---

## Process

1. **Proposal** - Document the problem and proposed solution
2. **Decision** - Record the chosen approach and rationale
3. **Implementation** - Write the code
4. **Review** - Verify implementation matches design
5. **Archive** - Keep as decision record

---

## Related

- [Specifications](../specs/) — Functional and non-functional requirements
- [User Stories](../stories/README.md) - Persona-driven narratives
