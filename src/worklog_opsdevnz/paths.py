"""Path resolution for worklog files."""

from datetime import date, datetime
from pathlib import Path
from typing import Any


def resolve_path(
    config: dict[str, Any],
    entry_date: date,
) -> Path:
    """Compute the target file path based on config structure."""
    base = Path(config.get("worklog_dir", "docs/worklog"))
    structure = config.get("structure", "year")
    suffix = config.get("suffix", "worklog")

    if structure == "flat":
        filename = f"{entry_date.isoformat()}-{suffix}.md"
        return base / filename
    elif structure == "year-month":
        year = entry_date.strftime("%Y")
        month = entry_date.strftime("%m")
        filename = f"{entry_date.strftime('%d-%m-%Y')}-{suffix}.md"
        return base / year / month / filename
    else:  # "year" (default)
        year = entry_date.strftime("%Y")
        filename = f"{entry_date.strftime('%d-%m-%Y')}-{suffix}.md"
        return base / year / filename


_DATE_FORMATS = ("%Y-%m-%d", "%d-%m-%Y")


def _parse_entry_date(filename: str, suffix: str) -> date | None:
    """Extract the entry date from a worklog filename, or None if not parseable."""
    stem = filename.removesuffix(".md")
    prefix = stem.removesuffix(f"-{suffix}")
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(prefix, fmt).date()
        except ValueError:
            continue
    return None


def find_previous(config: dict[str, Any], today: date) -> Path | None:
    """Locate the most recent worklog entry strictly before *today*.

    Scans the directory tree implied by the configured structure mode
    (flat, year, or year-month) for files matching ``*-{suffix}.md``,
    parses their dates, and returns the newest one older than today.
    Returns None when no previous entry exists. Never creates anything.
    """
    base = Path(config.get("worklog_dir", "docs/worklog"))
    suffix = config.get("suffix", "worklog")
    structure = config.get("structure", "year")

    pattern = f"*-{suffix}.md"
    if structure == "flat":
        candidates = base.glob(pattern)
    elif structure == "year-month":
        candidates = base.glob(f"*/*/{pattern}")
    else:  # "year" (default)
        candidates = base.glob(f"*/{pattern}")

    best: tuple[date, Path] | None = None
    for path in candidates:
        entry_date = _parse_entry_date(path.name, suffix)
        if entry_date is None or entry_date >= today:
            continue
        if best is None or entry_date > best[0]:
            best = (entry_date, path)
    return best[1] if best else None
