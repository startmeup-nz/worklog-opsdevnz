"""Tests for frontmatter and body generation."""

import pytest

from worklog_opsdevnz.template import (
    generate_frontmatter,
    generate_body,
    generate_content,
    render_template,
)


def test_generate_frontmatter():
    config = {
        "author": "Test Author",
        "default_tags": ["internal", "test"],
    }
    fm = generate_frontmatter(config, "2026-05-23")
    assert "title: " in fm
    assert "Work Log - 2026-05-23" in fm
    assert "date: 2026-05-23" in fm
    assert "author: Test Author" in fm
    assert "  - internal" in fm
    assert "  - test" in fm
    assert "draft: false" in fm
    assert fm.startswith("---")
    assert fm.strip().endswith("---")


def test_generate_body_with_sections():
    config = {
        "sections": [
            {"title": "Focus", "content": ""},
            {"title": "Notes", "content": "some note"},
        ]
    }
    body = generate_body(config)
    assert "## Focus" in body
    assert "## Notes" in body
    assert "some note" in body


def test_generate_content_full():
    config = {
        "author": "opsdev",
        "default_tags": ["log"],
        "sections": [{"title": "Today", "content": ""}],
    }
    content = generate_content(config, "2026-05-23")
    assert content.startswith("---")
    assert "Work Log - 2026-05-23" in content
    assert "## Today" in content


def test_render_template_with_placeholders(tmp_path):
    template = tmp_path / "my-template.md"
    template.write_text(
        "---\n"
        'title: "{{TITLE}}"\n'
        "date: {{DATE}}\n"
        "author: {{AUTHOR}}\n"
        "tags: {{TAGS}}\n"
        "draft: false\n"
        "---\n\n"
        "# {{TITLE}}\n\n"
        "Date: {{DATE}}\n\n"
        "Free-form notes."
    )

    config = {"author": "opsdev", "default_tags": ["dev", "log"]}
    result = render_template(str(template), "2026-05-26", config)

    # Placeholders replaced
    assert "{{DATE}}" not in result
    assert "{{TITLE}}" not in result
    assert "{{AUTHOR}}" not in result
    assert "{{TAGS}}" not in result

    # Content verified
    assert "# Work Log - 2026-05-26" in result
    assert "Date: 2026-05-26" in result
    assert "Free-form notes." in result
    assert 'title: "Work Log - 2026-05-26"' in result
    assert "date: 2026-05-26" in result
    assert "author: opsdev" in result
    assert "draft: false" in result

    # Tags rendered as block-style YAML
    assert "  - dev" in result
    assert "  - log" in result


def test_render_template_file_not_found():
    with pytest.raises(FileNotFoundError):
        render_template("/nonexistent/template.md", "2026-05-26", {})


def test_generate_content_with_template(tmp_path):
    """When template is set, it defines the complete entry.
    
    No auto-generated frontmatter is prepended.
    """
    template = tmp_path / "my-template.md"
    template.write_text(
        "---\n"
        'title: "{{TITLE}}"\n'
        "date: {{DATE}}\n"
        "author: {{AUTHOR}}\n"
        "tags: {{TAGS}}\n"
        "draft: false\n"
        "---\n\n"
        "# {{TITLE}}\n\n"
        "Date: {{DATE}}"
    )

    config = {
        "author": "opsdev",
        "default_tags": ["log"],
        "template": str(template),
    }
    content = generate_content(config, "2026-05-26")

    # Template defines the full entry — its frontmatter is present
    assert content.startswith("---")
    assert 'title: "Work Log - 2026-05-26"' in content
    assert "date: 2026-05-26" in content
    assert "author: opsdev" in content
    assert "  - log" in content
    assert "draft: false" in content

    # Body comes from template
    assert "# Work Log - 2026-05-26" in content
    assert "Date: 2026-05-26" in content

    # No duplicate frontmatter — only one '---' block
    assert content.count("---") == 2  # opening + closing

    # Sections are NOT present (template controls everything)
    assert "## Focus for Today" not in content


def test_generate_content_without_template():
    """No template field → built-in sections body, unchanged behaviour."""
    config = {
        "author": "opsdev",
        "default_tags": ["log"],
        "sections": [{"title": "Today", "content": ""}],
    }
    content = generate_content(config, "2026-05-26")
    assert "## Today" in content


# ── {{TAGS}} rendering ────────────────────────────────────────────


def test_render_template_tags_empty(tmp_path):
    """Empty default_tags → {{TAGS}} substitutes as '[]'."""
    template = tmp_path / "t.md"
    template.write_text("tags: {{TAGS}}\n")

    result = render_template(str(template), "2026-06-01", {"default_tags": []})
    assert "tags: []" in result
    assert "{{TAGS}}" not in result


def test_render_template_tags_populated(tmp_path):
    """Populated default_tags → {{TAGS}} renders as block-style YAML list."""
    template = tmp_path / "t.md"
    template.write_text("tags: {{TAGS}}\n")

    config = {"default_tags": ["dev", "log", "ops"]}
    result = render_template(str(template), "2026-06-01", config)

    # Block-style: leading newline + indented items
    # (template line is 'tags: {{TAGS}}', substitution starts with \n)
    assert "tags:" in result
    assert "  - dev" in result
    assert "  - log" in result
    assert "  - ops" in result
    assert "{{TAGS}}" not in result


def test_render_template_tags_not_configured(tmp_path):
    """No default_tags in config → {{TAGS}} substitutes as '[]'."""
    template = tmp_path / "t.md"
    template.write_text("tags: {{TAGS}}\n")

    result = render_template(str(template), "2026-06-01", {})
    assert "tags: []" in result


# ── {{AUTHOR}} rendering ──────────────────────────────────────────


def test_render_template_author_configured(tmp_path):
    """{{AUTHOR}} pulls the author value from config."""
    template = tmp_path / "t.md"
    template.write_text("author: {{AUTHOR}}\n")

    result = render_template(str(template), "2026-06-01", {"author": "opsdev"})
    assert "author: opsdev" in result
    assert "{{AUTHOR}}" not in result


def test_render_template_author_fallback(tmp_path):
    """{{AUTHOR}} falls back to 'unknown' when not in config."""
    template = tmp_path / "t.md"
    template.write_text("author: {{AUTHOR}}\n")

    result = render_template(str(template), "2026-06-01", {})
    assert "author: unknown" in result


# ── Full-entry template edge cases ────────────────────────────────


def test_generate_content_template_defines_full_entry(tmp_path):
    """Template with custom YAML fields — the tool only substitutes placeholders."""
    template = tmp_path / "custom.md"
    template.write_text(
        "---\n"
        'title: "{{TITLE}}"\n'
        "date: {{DATE}}\n"
        "author: {{AUTHOR}}\n"
        "tags: {{TAGS}}\n"
        "mood: creative\n"
        "project: outcome-engineering\n"
        "draft: false\n"
        "---\n\n"
        "# {{TITLE}}\n\n"
        "Custom body content."
    )

    config = {
        "author": "opsdev",
        "default_tags": ["dev"],
        "template": str(template),
    }
    content = generate_content(config, "2026-06-05")

    # Custom fields preserved verbatim
    assert "mood: creative" in content
    assert "project: outcome-engineering" in content

    # Placeholders substituted
    assert 'title: "Work Log - 2026-06-05"' in content
    assert "date: 2026-06-05" in content
    assert "author: opsdev" in content
    assert "  - dev" in content

    # Body preserved
    assert "Custom body content." in content

    # No auto-generated frontmatter prepended
    assert content.count("---") == 2  # only the template's opening/closing


def test_generate_content_template_no_frontmatter(tmp_path):
    """Template without frontmatter — entry has no frontmatter at all."""
    template = tmp_path / "body-only.md"
    template.write_text("# {{TITLE}}\n\nJust body content.")

    config = {"template": str(template)}
    content = generate_content(config, "2026-06-05")

    # No frontmatter markers, just the rendered template
    assert "---" not in content
    assert "# Work Log - 2026-06-05" in content
    assert "Just body content." in content


def test_render_template_case_sensitive(tmp_path):
    """Lowercase placeholders are NOT substituted."""
    template = tmp_path / "t.md"
    template.write_text(
        "title: {{title}}\n"
        "date: {{date}}\n"
        "author: {{author}}\n"
        "tags: {{tags}}\n"
    )

    config = {"author": "opsdev", "default_tags": ["dev"]}
    result = render_template(str(template), "2026-06-05", config)

    # Lowercase placeholders left untouched
    assert "{{title}}" in result
    assert "{{date}}" in result
    assert "{{author}}" in result
    assert "{{tags}}" in result
