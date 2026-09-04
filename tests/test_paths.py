"""Tests for path resolution."""

from datetime import date

from worklog_opsdevnz.paths import find_previous, resolve_path


def test_resolve_path_flat():
    config = {"worklog_dir": "docs/worklog", "structure": "flat", "suffix": "worklog"}
    path = resolve_path(config, date(2026, 5, 23))
    assert str(path) == "docs/worklog/2026-05-23-worklog.md"


def test_resolve_path_year():
    config = {"worklog_dir": "logs", "structure": "year", "suffix": "log"}
    path = resolve_path(config, date(2026, 5, 23))
    assert str(path) == "logs/2026/23-05-2026-log.md"


def test_resolve_path_year_month():
    config = {"worklog_dir": "logs", "structure": "year-month", "suffix": "ops"}
    path = resolve_path(config, date(2026, 5, 23))
    assert str(path) == "logs/2026/05/23-05-2026-ops.md"


def test_resolve_path_custom_suffix():
    config = {"structure": "year", "suffix": "retro"}
    path = resolve_path(config, date(2026, 1, 1))
    assert str(path).endswith("-retro.md")


def test_find_previous_year(tmp_path):
    base = tmp_path / "logs" / "2026"
    base.mkdir(parents=True)
    (base / "28-08-2026-worklog.md").write_text("old")
    (base / "01-09-2026-worklog.md").write_text("prev")
    (base / "03-09-2026-worklog.md").write_text("today")
    config = {"worklog_dir": str(tmp_path / "logs"), "structure": "year", "suffix": "worklog"}
    result = find_previous(config, date(2026, 9, 3))
    assert result is not None
    assert result.name == "01-09-2026-worklog.md"


def test_find_previous_year_month(tmp_path):
    base = tmp_path / "docs" / "worklogs"
    (base / "2026" / "08").mkdir(parents=True)
    (base / "2026" / "09").mkdir(parents=True)
    (base / "2026" / "08" / "27-08-2026-worklog.md").write_text("aug")
    (base / "2026" / "09" / "01-09-2026-worklog.md").write_text("sep")
    config = {"worklog_dir": str(base), "structure": "year-month", "suffix": "worklog"}
    result = find_previous(config, date(2026, 9, 2))
    assert result is not None
    assert result.name == "01-09-2026-worklog.md"


def test_find_previous_flat_iso_names(tmp_path):
    base = tmp_path / "wl"
    base.mkdir()
    (base / "2026-08-30-worklog.md").write_text("a")
    (base / "2026-09-01-worklog.md").write_text("b")
    config = {"worklog_dir": str(base), "structure": "flat", "suffix": "worklog"}
    result = find_previous(config, date(2026, 9, 2))
    assert result is not None
    assert result.name == "2026-09-01-worklog.md"


def test_find_previous_ignores_today_unrelated_and_wrong_suffix(tmp_path):
    base = tmp_path / "logs" / "2026"
    base.mkdir(parents=True)
    (base / "03-09-2026-worklog.md").write_text("today")
    (base / "README.md").write_text("not an entry")
    (base / "01-09-2026-journal.md").write_text("wrong suffix")
    config = {"worklog_dir": str(tmp_path / "logs"), "structure": "year", "suffix": "worklog"}
    assert find_previous(config, date(2026, 9, 3)) is None


def test_find_previous_missing_dir(tmp_path):
    config = {"worklog_dir": str(tmp_path / "nothing"), "structure": "year", "suffix": "worklog"}
    assert find_previous(config, date(2026, 9, 3)) is None
