#!/usr/bin/env python3
"""
generate_chart.py - Generate SVG charts for presentations

Usage:
    # Bar chart
    python generate_chart.py --type bar \
        --data '{"labels": ["Q1","Q2","Q3","Q4"], "values": [100,150,200,180]}' \
        --output assets/revenue-chart.svg

    # Pie chart
    python generate_chart.py --type pie \
        --data '{"labels": ["Sales","Marketing","R&D"], "values": [45,30,25]}' \
        --output assets/budget-chart.svg

    # Line chart
    python generate_chart.py --type line \
        --data '{"labels": ["Jan","Feb","Mar","Apr","May"], "values": [10,25,15,30,45]}' \
        --output assets/growth-chart.svg

    # With style file for theming
    python generate_chart.py --type bar \
        --data '{"labels": ["A","B","C"], "values": [10,20,30]}' \
        --style-file .claude-design/image-style.json \
        --title "Performance Metrics" \
        --output assets/metrics-chart.svg
"""

import argparse
import json
import math
import sys
from pathlib import Path


# Default colors if no style file provided
DEFAULT_COLORS = {
    "primary": "#1e293b",
    "secondary": "#64748b",
    "accent": "#2563eb",
    "background": "#ffffff",
    "chart_colors": ["#2563eb", "#7c3aed", "#db2777", "#ea580c", "#16a34a", "#0891b2"]
}


def load_style(style_file: str | None) -> dict:
    """Load colors from style file or return defaults."""
    if not style_file:
        return DEFAULT_COLORS

    try:
        with open(style_file, "r", encoding="utf-8") as f:
            style = json.load(f)
            colors = style.get("color_palette", {})
            return {
                "primary": colors.get("primary", DEFAULT_COLORS["primary"]),
                "secondary": colors.get("secondary", DEFAULT_COLORS["secondary"]),
                "accent": colors.get("accent", DEFAULT_COLORS["accent"]),
                "background": colors.get("background", DEFAULT_COLORS["background"]),
                "chart_colors": [
                    colors.get("accent", DEFAULT_COLORS["chart_colors"][0]),
                    *DEFAULT_COLORS["chart_colors"][1:]
                ]
            }
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load style file: {e}. Using defaults.", file=sys.stderr)
        return DEFAULT_COLORS


def parse_data(data_str: str) -> dict:
    """Parse JSON data string into labels and values."""
    try:
        data = json.loads(data_str)
        if "labels" not in data or "values" not in data:
            print("Error: Data must have 'labels' and 'values' keys", file=sys.stderr)
            sys.exit(1)
        if len(data["labels"]) != len(data["values"]):
            print("Error: labels and values must have same length", file=sys.stderr)
            sys.exit(1)
        return data
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON data: {e}", file=sys.stderr)
        sys.exit(1)


def escape_xml(text: str) -> str:
    """Escape special characters for XML/SVG."""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\"", "&quot;")
            .replace("'", "&#39;"))


def generate_bar_chart(data: dict, colors: dict, title: str | None,
                       width: int = 600, height: int = 400) -> str:
    """Generate an SVG bar chart."""
    labels = data["labels"]
    values = data["values"]
    n = len(values)

    # Layout
    margin_top = 60 if title else 30
    margin_bottom = 60
    margin_left = 60
    margin_right = 30
    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom

    # Calculate scales
    max_val = max(values) * 1.1  # Add 10% headroom
    bar_width = chart_width / n * 0.7
    bar_gap = chart_width / n * 0.15

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="system-ui, -apple-system, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{colors["background"]}"/>',
    ]

    # Title
    if title:
        svg_parts.append(
            f'<text x="{width/2}" y="30" text-anchor="middle" '
            f'font-size="18" font-weight="600" fill="{colors["primary"]}">'
            f'{escape_xml(title)}</text>'
        )

    # Y-axis gridlines and labels
    num_gridlines = 5
    for i in range(num_gridlines + 1):
        y = margin_top + chart_height - (i / num_gridlines * chart_height)
        val = int(max_val * i / num_gridlines)
        svg_parts.append(
            f'<line x1="{margin_left}" y1="{y}" x2="{width - margin_right}" y2="{y}" '
            f'stroke="{colors["secondary"]}" stroke-opacity="0.2"/>'
        )
        svg_parts.append(
            f'<text x="{margin_left - 10}" y="{y + 4}" text-anchor="end" '
            f'font-size="12" fill="{colors["secondary"]}">{val}</text>'
        )

    # Bars and labels
    for i, (label, value) in enumerate(zip(labels, values)):
        x = margin_left + i * (chart_width / n) + bar_gap
        bar_height = (value / max_val) * chart_height
        y = margin_top + chart_height - bar_height

        color = colors["chart_colors"][i % len(colors["chart_colors"])]

        # Bar
        svg_parts.append(
            f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" '
            f'fill="{color}" rx="4"/>'
        )

        # Value label
        svg_parts.append(
            f'<text x="{x + bar_width/2}" y="{y - 8}" text-anchor="middle" '
            f'font-size="12" font-weight="600" fill="{colors["primary"]}">{value}</text>'
        )

        # X-axis label
        svg_parts.append(
            f'<text x="{x + bar_width/2}" y="{height - margin_bottom + 20}" text-anchor="middle" '
            f'font-size="12" fill="{colors["secondary"]}">{escape_xml(label)}</text>'
        )

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_pie_chart(data: dict, colors: dict, title: str | None,
                       width: int = 600, height: int = 400) -> str:
    """Generate an SVG pie chart."""
    labels = data["labels"]
    values = data["values"]
    total = sum(values)

    # Layout
    margin_top = 50 if title else 20
    cx = width / 2 - 80  # Center X (shifted left for legend)
    cy = margin_top + (height - margin_top) / 2
    radius = min(cx - 40, cy - margin_top - 20)

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="system-ui, -apple-system, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{colors["background"]}"/>',
    ]

    # Title
    if title:
        svg_parts.append(
            f'<text x="{width/2}" y="30" text-anchor="middle" '
            f'font-size="18" font-weight="600" fill="{colors["primary"]}">'
            f'{escape_xml(title)}</text>'
        )

    # Draw pie slices
    start_angle = -90  # Start from top
    for i, (label, value) in enumerate(zip(labels, values)):
        percentage = value / total
        angle = percentage * 360
        end_angle = start_angle + angle

        # Convert to radians
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)

        # Calculate arc points
        x1 = cx + radius * math.cos(start_rad)
        y1 = cy + radius * math.sin(start_rad)
        x2 = cx + radius * math.cos(end_rad)
        y2 = cy + radius * math.sin(end_rad)

        # Large arc flag
        large_arc = 1 if angle > 180 else 0

        color = colors["chart_colors"][i % len(colors["chart_colors"])]

        # Path for slice
        path = f'M {cx},{cy} L {x1},{y1} A {radius},{radius} 0 {large_arc},1 {x2},{y2} Z'
        svg_parts.append(f'<path d="{path}" fill="{color}"/>')

        start_angle = end_angle

    # Legend
    legend_x = cx + radius + 60
    legend_y = cy - len(labels) * 12

    for i, (label, value) in enumerate(zip(labels, values)):
        y = legend_y + i * 28
        color = colors["chart_colors"][i % len(colors["chart_colors"])]
        percentage = round(value / total * 100)

        # Color box
        svg_parts.append(
            f'<rect x="{legend_x}" y="{y}" width="16" height="16" fill="{color}" rx="2"/>'
        )
        # Label
        svg_parts.append(
            f'<text x="{legend_x + 24}" y="{y + 12}" font-size="12" fill="{colors["primary"]}">'
            f'{escape_xml(label)} ({percentage}%)</text>'
        )

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_line_chart(data: dict, colors: dict, title: str | None,
                        width: int = 600, height: int = 400) -> str:
    """Generate an SVG line chart."""
    labels = data["labels"]
    values = data["values"]
    n = len(values)

    # Layout
    margin_top = 60 if title else 30
    margin_bottom = 60
    margin_left = 60
    margin_right = 30
    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom

    # Calculate scales
    max_val = max(values) * 1.1
    min_val = min(0, min(values))

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="system-ui, -apple-system, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{colors["background"]}"/>',
    ]

    # Title
    if title:
        svg_parts.append(
            f'<text x="{width/2}" y="30" text-anchor="middle" '
            f'font-size="18" font-weight="600" fill="{colors["primary"]}">'
            f'{escape_xml(title)}</text>'
        )

    # Y-axis gridlines and labels
    num_gridlines = 5
    for i in range(num_gridlines + 1):
        y = margin_top + chart_height - (i / num_gridlines * chart_height)
        val = int(min_val + (max_val - min_val) * i / num_gridlines)
        svg_parts.append(
            f'<line x1="{margin_left}" y1="{y}" x2="{width - margin_right}" y2="{y}" '
            f'stroke="{colors["secondary"]}" stroke-opacity="0.2"/>'
        )
        svg_parts.append(
            f'<text x="{margin_left - 10}" y="{y + 4}" text-anchor="end" '
            f'font-size="12" fill="{colors["secondary"]}">{val}</text>'
        )

    # Calculate points
    points = []
    for i, value in enumerate(values):
        x = margin_left + (i / (n - 1)) * chart_width if n > 1 else margin_left + chart_width / 2
        y = margin_top + chart_height - ((value - min_val) / (max_val - min_val)) * chart_height
        points.append((x, y))

    # Draw area under line (gradient fill)
    area_points = [f'{margin_left},{margin_top + chart_height}']
    area_points.extend([f'{x},{y}' for x, y in points])
    area_points.append(f'{points[-1][0]},{margin_top + chart_height}')

    svg_parts.append(
        f'<defs><linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">'
        f'<stop offset="0%" stop-color="{colors["accent"]}" stop-opacity="0.3"/>'
        f'<stop offset="100%" stop-color="{colors["accent"]}" stop-opacity="0.05"/>'
        f'</linearGradient></defs>'
    )
    svg_parts.append(
        f'<polygon points="{" ".join(area_points)}" fill="url(#areaGradient)"/>'
    )

    # Draw line
    line_points = ' '.join([f'{x},{y}' for x, y in points])
    svg_parts.append(
        f'<polyline points="{line_points}" fill="none" '
        f'stroke="{colors["accent"]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
    )

    # Draw points and labels
    for i, ((x, y), label, value) in enumerate(zip(points, labels, values)):
        # Point
        svg_parts.append(
            f'<circle cx="{x}" cy="{y}" r="5" fill="{colors["background"]}" '
            f'stroke="{colors["accent"]}" stroke-width="2"/>'
        )

        # Value label
        svg_parts.append(
            f'<text x="{x}" y="{y - 12}" text-anchor="middle" '
            f'font-size="11" font-weight="600" fill="{colors["primary"]}">{value}</text>'
        )

        # X-axis label
        svg_parts.append(
            f'<text x="{x}" y="{height - margin_bottom + 20}" text-anchor="middle" '
            f'font-size="12" fill="{colors["secondary"]}">{escape_xml(label)}</text>'
        )

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_alt_text(chart_type: str, data: dict, title: str | None) -> str:
    """Generate alt text for the chart."""
    labels = data["labels"]
    values = data["values"]

    type_names = {
        "bar": "Bar chart",
        "pie": "Pie chart",
        "line": "Line chart"
    }
    type_name = type_names.get(chart_type, "Chart")

    if title:
        desc = f"{type_name} titled '{title}'"
    else:
        desc = type_name

    # Summarize data
    if len(labels) <= 4:
        data_summary = ", ".join([f"{l}: {v}" for l, v in zip(labels, values)])
        return f"{desc} showing {data_summary}"
    else:
        return f"{desc} showing {len(labels)} data points from {labels[0]} to {labels[-1]}"


def main():
    parser = argparse.ArgumentParser(
        description="Generate SVG charts for presentations"
    )

    parser.add_argument(
        "--type", "-t",
        required=True,
        choices=["bar", "pie", "line"],
        help="Chart type: bar, pie, or line"
    )
    parser.add_argument(
        "--data", "-d",
        required=True,
        help='JSON data: {"labels": [...], "values": [...]}'
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output SVG file path"
    )
    parser.add_argument(
        "--style-file",
        help="Path to image-style.json for theming"
    )
    parser.add_argument(
        "--title",
        help="Chart title (optional)"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=600,
        help="Chart width in pixels (default: 600)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=400,
        help="Chart height in pixels (default: 400)"
    )

    args = parser.parse_args()

    # Load style
    colors = load_style(args.style_file)

    # Parse data
    data = parse_data(args.data)

    # Generate chart
    generators = {
        "bar": generate_bar_chart,
        "pie": generate_pie_chart,
        "line": generate_line_chart
    }

    svg = generators[args.type](data, colors, args.title, args.width, args.height)

    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write SVG
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    # Generate alt text
    alt_text = generate_alt_text(args.type, data, args.title)

    print(f"Generated: {args.output}")
    print(f"Suggested alt text: \"{alt_text}\"")


if __name__ == "__main__":
    main()
