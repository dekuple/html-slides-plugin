#!/usr/bin/env python3
"""
generate_slides.py - Generate HTML slide files from extracted content
"""

import json
import re
import sys
from pathlib import Path


def generate_slides(json_path: str, output_dir: str):
    """Generate slide HTML files from extracted content JSON."""

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    slides_dir = Path(output_dir) / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)

    for slide in data["slides"]:
        num = slide["number"]
        title = slide["title"]
        slug = slugify(title) if title else f"slide-{num}"
        filename = f"{num:02d}-{slug}.html"

        html = generate_slide_html(slide)

        filepath = slides_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"Created {filename}")

    print(f"\nGenerated {len(data['slides'])} slide files in {slides_dir}")


def slugify(text: str) -> str:
    """Convert title to filename-safe slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text[:30]  # Limit length


def generate_slide_html(slide: dict) -> str:
    """Generate HTML for a single slide."""

    num = slide["number"]
    title = slide["title"]
    content = slide["content"]
    images = slide["images"]
    notes = slide["notes"]
    layout = slide.get("layout", "")

    # Determine slide type
    is_title_slide = num == 1 or "title" in layout.lower()
    has_images = len(images) > 0
    has_table = any(c.get("type") == "table" for c in content)

    lines = []

    # Speaker notes as comment
    if notes:
        lines.append(f"<!-- Speaker notes: {notes[:200]}{'...' if len(notes) > 200 else ''} -->")

    # Opening tag
    modifier = " slide--title" if is_title_slide else ""
    lines.append(f'<section class="slide{modifier}">')

    # Title
    if title:
        tag = "h1" if is_title_slide else "h2"
        lines.append(f'    <{tag} class="reveal">{escape_html(title)}</{tag}>')

    # Content
    for item in content:
        if item["type"] == "text":
            lines.extend(generate_text_content(item["content"], is_title_slide))
        elif item["type"] == "table":
            lines.extend(generate_table_content(item["content"]))

    # Images
    for img in images:
        lines.append(f'    <figure class="reveal">')
        lines.append(f'        <img src="{img["path"]}" alt="{img.get("alt", "")}">')
        lines.append(f'    </figure>')

    lines.append('</section>')

    return '\n'.join(lines)


def generate_text_content(paragraphs: list, is_title_slide: bool) -> list:
    """Generate HTML for text content."""
    lines = []

    # Group by level for list detection
    has_hierarchy = any(p.get("level", 0) > 0 for p in paragraphs)

    if has_hierarchy:
        # Render as list
        lines.append('    <ul class="reveal-list">')
        for para in paragraphs:
            level = para.get("level", 0)
            text = escape_html(para["text"])
            indent = "        " + ("    " * level)
            lines.append(f'{indent}<li class="reveal">{text}</li>')
        lines.append('    </ul>')
    else:
        # Render as paragraphs
        for para in paragraphs:
            text = escape_html(para["text"])
            css_class = "subtitle" if is_title_slide else ""
            class_attr = f' class="reveal {css_class}"'.strip() if css_class else ' class="reveal"'
            lines.append(f'    <p{class_attr}>{text}</p>')

    return lines


def generate_table_content(table: dict) -> list:
    """Generate HTML for table content."""
    lines = []
    data = table["data"]

    if not data:
        return lines

    lines.append('    <table class="reveal">')

    # First row as header
    lines.append('        <thead>')
    lines.append('            <tr>')
    for cell in data[0]:
        lines.append(f'                <th>{escape_html(cell)}</th>')
    lines.append('            </tr>')
    lines.append('        </thead>')

    # Rest as body
    if len(data) > 1:
        lines.append('        <tbody>')
        for row in data[1:]:
            lines.append('            <tr>')
            for cell in row:
                lines.append(f'                <td>{escape_html(cell)}</td>')
            lines.append('            </tr>')
        lines.append('        </tbody>')

    lines.append('    </table>')

    return lines


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;"))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_slides.py <extracted_content.json> [output_dir]")
        sys.exit(1)

    json_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    generate_slides(json_path, output_dir)
