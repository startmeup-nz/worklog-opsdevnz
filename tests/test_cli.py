"""Tests for CLI entry point."""

from datetime import date, timedelta

from click.testing import CliRunner

from worklog_opsdevnz.cli import main


def test_main_creates_file(tmp_path, monkeypatch):
    """Running with no args creates today's worklog in tmp_path."""
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Created" in result.output
    expected_leaf = (
        f"docs/worklog/{date.today().year}/{date.today():%d-%m-%Y}-worklog.md"
    )
    assert expected_leaf in result.output


def test_main_opens_existing(tmp_path, monkeypatch):
    """Running again opens the existing file."""
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main, [])
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Opening existing" in result.output


def test_main_help():
    """--help works."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "--editor" in result.output


def test_main_version():
    """--version prints the installed version."""
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "worklog-opsdevnz, version" in result.output
    # Extract and verify it's a non-empty version string
    version_str = result.output.strip().split(", version ")[-1]
    assert version_str


def test_main_editor_from_config(tmp_path, monkeypatch):
    """Editor in worklog.toml is resolved before $VISUAL/$EDITOR."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "worklog.toml").write_text('editor = "fake-editor-test"\n')
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    # config-based editor picked up but not found in PATH
    assert "Editor 'fake-editor-test' not found" in result.output


def test_main_editor_cli_overrides_config(tmp_path, monkeypatch):
    """-e flag overrides the editor set in worklog.toml."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "worklog.toml").write_text('editor = "fake-editor-test"\n')
    runner = CliRunner()
    result = runner.invoke(main, ["-e", "override-editor-test"])
    assert result.exit_code == 0
    # CLI override takes priority over config
    assert "Editor 'override-editor-test' not found" in result.output


def test_previous_no_entries(tmp_path, monkeypatch):
    """-p with no prior entries: message to stderr, exit 0, creates nothing."""
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main, ["-p"])
    assert result.exit_code == 0
    assert "No previous worklog entry found." in result.stderr
    assert not (tmp_path / "docs").exists()


def test_previous_opens_most_recent_before_today(tmp_path, monkeypatch):
    """-p opens the newest prior entry, not today's, and creates no file."""
    monkeypatch.chdir(tmp_path)
    today = date.today()
    year_dir = tmp_path / "docs" / "worklog" / str(today.year)
    year_dir.mkdir(parents=True)
    older = (today - timedelta(days=3)).strftime("%d-%m-%Y")
    recent = (today - timedelta(days=1)).strftime("%d-%m-%Y")
    (year_dir / f"{older}-worklog.md").write_text("older")
    (year_dir / f"{recent}-worklog.md").write_text("recent")
    today_file = year_dir / f"{today:%d-%m-%Y}-worklog.md"
    today_file.write_text("today")

    runner = CliRunner()
    result = runner.invoke(main, ["--previous"])
    assert result.exit_code == 0
    assert recent in result.output
    assert today.strftime("%d-%m-%Y") not in result.output


def test_previous_does_not_create_today(tmp_path, monkeypatch):
    """-p must not create today's entry even though it does not exist."""
    monkeypatch.chdir(tmp_path)
    today = date.today()
    year_dir = tmp_path / "docs" / "worklog" / str(today.year)
    year_dir.mkdir(parents=True)
    (year_dir / f"{(today - timedelta(days=2)):%d-%m-%Y}-worklog.md").write_text("x")

    runner = CliRunner()
    runner.invoke(main, ["-p"])
    assert not (year_dir / f"{today:%d-%m-%Y}-worklog.md").exists()


def test_previous_editor_override(tmp_path, monkeypatch):
    """-p combined with -e applies the editor override to the previous entry."""
    monkeypatch.chdir(tmp_path)
    today = date.today()
    year_dir = tmp_path / "docs" / "worklog" / str(today.year)
    year_dir.mkdir(parents=True)
    recent = (today - timedelta(days=1)).strftime("%d-%m-%Y")
    (year_dir / f"{recent}-worklog.md").write_text("recent")

    runner = CliRunner()
    result = runner.invoke(main, ["-p", "-e", "override-editor-test"])
    assert result.exit_code == 0
    assert "Editor 'override-editor-test' not found" in result.output


def test_previous_help():
    """--help mentions the --previous flag."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "--previous" in result.output
