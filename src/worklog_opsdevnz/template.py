"""Frontmatter and body generation for worklog entries."""

from typing import Any


def generate_frontmatter(
    config: dict[str, Any],
    iso_date: str,
) -> str:
    """Generate YAML frontmatter."""
    title = f"Work Log - {iso_date}"
    tags = "\n".join(f"  - {t}" for t in config.get("default_tags", []))
    author = config.get("author", "unknown")

    return f"""---
title: "{title}"
date: {iso_date}
author: {author}
tags:
{tags}
draft: false
---
"""


def generate_body(config: dict[str, Any]) -> str:
    """Generate section headers from config."""
    sections = config.get("sections", [])
    lines = []
    for section in sections:
        title = section.get("title", "")
        content = section.get("content", "")
        lines.append(f"## {title}\n")
        if content:
            lines.append(f"{content}\n")
    return "\n".join(lines)


def _render_tags(tags: list[str]) -> str:
    """Render tags as a block-style YAML list substitution.

    Empty list → '[]'. Populated list → leading newline followed by
    each tag on its own indented line with '-' prefix.
    """
    if not tags:
        return "[]"
    return "\n" + "\n".join(f"  - {t}" for t in tags)


def render_template(
    template_path: str,
    iso_date: str,
    config: dict[str, Any],
) -> str:
    """Render a custom Markdown template with placeholder substitution.

    Supports {{DATE}}, {{TITLE}}, {{AUTHOR}}, and {{TAGS}} placeholders.
    All placeholders are case-sensitive.
    """
    title = f"Work Log - {iso_date}"
    tags = _render_tags(config.get("default_tags", []))
    author = config.get("author", "unknown")
    with open(template_path) as f:
        content = f.read()
    content = content.replace("{{DATE}}", iso_date)
    content = content.replace("{{TITLE}}", title)
    content = content.replace("{{AUTHOR}}", author)
    content = content.replace("{{TAGS}}", tags)
    # Clean trailing whitespace (avoids artifacts when placeholder
    # substitution leaves space before a newline, e.g. 'tags: \n')
    content = "\n".join(line.rstrip() for line in content.split("\n"))
    return content


def generate_content(
    config: dict[str, Any],
    iso_date: str,
) -> str:
    """Generate full worklog content.

    If a 'template' field is set in config, the template defines the
    complete entry (including YAML frontmatter). Placeholders are
    substituted but nothing else is prepended.

    Otherwise uses the built-in default: config-driven frontmatter and
    sections-based body.
    """
    template_path = config.get("template")
    if template_path:
        return render_template(template_path, iso_date, config)

    frontmatter = generate_frontmatter(config, iso_date)
    body = generate_body(config)
    return f"{frontmatter}\n{body}"
