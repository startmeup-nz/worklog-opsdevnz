"""CLI entry point for worklog-opsdevnz."""

import shutil
import subprocess
from datetime import date
from pathlib import Path

import click

from worklog_opsdevnz import __version__
from worklog_opsdevnz.config import get_config
from worklog_opsdevnz.paths import find_previous, resolve_path
from worklog_opsdevnz.template import generate_content


@click.command()
@click.version_option(version=__version__, prog_name="worklog-opsdevnz")
@click.option(
    "-e",
    "--editor",
    default=None,
    help="Override the editor command (overrides config, $VISUAL, $EDITOR).",
)
@click.option(
    "-p",
    "--previous",
    is_flag=True,
    help="Open the most recent worklog entry before today (never creates).",
)
def main(editor: str | None, previous: bool) -> None:
    """Create or open today's worklog entry, or the previous one with -p."""
    entry_date = date.today()

    config = get_config()

    if previous:
        target = find_previous(config, entry_date)
        if target is None:
            click.echo("No previous worklog entry found.", err=True)
            return
        print(f"Opening previous worklog: {target}")
        _open_editor(target, editor, config.get("editor"))
        return

    target = resolve_path(config, entry_date)
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        print(f"Opening existing worklog: {target}")
    else:
        content = generate_content(config, entry_date.isoformat())
        target.write_text(content)
        print(f"Created: {target}")

    _open_editor(target, editor, config.get("editor"))


def _open_editor(path: str | Path, override: str | None = None, config_editor: str | None = None) -> None:
    """Open the file in the configured editor, or print the path."""
    editor = _resolve_editor(override, config_editor)
    if editor:
        editor_cmd = shutil.which(editor)
        if editor_cmd:
            # fmt: off
            subprocess.run([editor_cmd, str(path)])
            # fmt: on
        else:
            print(f"Editor '{editor}' not found. Path: {path}")
    else:
        print(f"No editor configured. Path: {path}")


def _resolve_editor(override: str | None = None, config_editor: str | None = None) -> str | None:
    """Resolve editor from CLI, config, $VISUAL, or $EDITOR."""
    import os

    for candidate in (override, config_editor, os.environ.get("VISUAL"), os.environ.get("EDITOR")):
        if candidate:
            return candidate
    return None


if __name__ == "__main__":
    main()
