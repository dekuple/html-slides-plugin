---
name: html-slides-pptx
description: "Convert PowerPoint presentations (.ppt, .pptx) to HTML slide decks. Use when the user uploads a PowerPoint file and wants it converted to a web-based presentation."
---

# HTML Slides — PowerPoint Conversion

Convert existing PowerPoint files to the multi-file HTML presentation format.

## Quick Reference

| Step | Action |
|------|--------|
| 1. Extract | Run Python script to pull content and images |
| 2. Review | Confirm extracted content with user |
| 3. Style | Choose visual style (→ [html-slides-style](../html-slides-style/SKILL.md)) |
| 4. Generate | Create slide files from extracted content |
| 5. Build | Run `./build.sh` and preview |

---

## Prerequisites

Install the required Python package:

```bash
pip install python-pptx --break-system-packages
```

---

## Phase 1: Extract Content

### Step 1.1: Run Extraction Script

Create and run this extraction script:

```python
#!/usr/bin/env python3
"""
extract_pptx.py - Extract content and images from PowerPoint files
"""

import json
import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE


def extract_pptx(file_path: str, output_dir: str) -> dict:
    """
    Extract all content from a PowerPoint file.
    
    Returns a dict with slides, text, images, and speaker notes.
    """
    prs = Presentation(file_path)
    output_path = Path(output_dir)
    assets_dir = output_path / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    slides_data = []
    
    for slide_num, slide in enumerate(prs.slides, start=1):
        slide_data = {
            "number": slide_num,
            "title": "",
            "content": [],
            "images": [],
            "notes": "",
            "layout": get_layout_name(slide)
        }
        
        # Extract shapes
        for shape in slide.shapes:
            # Title
            if shape.is_placeholder and shape == slide.shapes.title:
                if shape.has_text_frame:
                    slide_data["title"] = shape.text.strip()
            
            # Text content
            elif shape.has_text_frame:
                text = extract_text_frame(shape.text_frame)
                if text:
                    slide_data["content"].append({
                        "type": "text",
                        "content": text
                    })
            
            # Tables
            elif shape.has_table:
                table_data = extract_table(shape.table)
                slide_data["content"].append({
                    "type": "table",
                    "content": table_data
                })
            
            # Images
            elif shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                image_info = extract_image(shape, slide_num, len(slide_data["images"]) + 1, assets_dir)
                if image_info:
                    slide_data["images"].append(image_info)
        
        # Speaker notes
        if slide.has_notes_slide:
            notes_frame = slide.notes_slide.notes_text_frame
            if notes_frame:
                slide_data["notes"] = notes_frame.text.strip()
        
        slides_data.append(slide_data)
    
    result = {
        "source_file": os.path.basename(file_path),
        "slide_count": len(slides_data),
        "slides": slides_data
    }
    
    # Save extraction result
    json_path = output_path / "extracted_content.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(slides_data)} slides to {output_dir}")
    print(f"Content saved to {json_path}")
    
    return result


def get_layout_name(slide) -> str:
    """Get the layout name for slide type hints."""
    try:
        return slide.slide_layout.name
    except:
        return "unknown"


def extract_text_frame(text_frame) -> list:
    """Extract paragraphs from a text frame."""
    paragraphs = []
    for para in text_frame.paragraphs:
        text = para.text.strip()
        if text:
            paragraphs.append({
                "text": text,
                "level": para.level  # Indentation level (0 = top level)
            })
    return paragraphs


def extract_table(table) -> dict:
    """Extract table data as rows and columns."""
    rows = []
    for row in table.rows:
        cells = []
        for cell in row.cells:
            cells.append(cell.text.strip())
        rows.append(cells)
    
    return {
        "rows": len(table.rows),
        "cols": len(table.columns),
        "data": rows
    }


def extract_image(shape, slide_num: int, img_num: int, assets_dir: Path) -> dict:
    """Extract and save an image from a shape."""
    try:
        image = shape.image
        ext = image.ext
        filename = f"slide{slide_num:02d}_img{img_num}.{ext}"
        filepath = assets_dir / filename
        
        with open(filepath, "wb") as f:
            f.write(image.blob)
        
        return {
            "path": f"assets/{filename}",
            "width": shape.width,
            "height": shape.height,
            "alt": f"Image from slide {slide_num}"
        }
    except Exception as e:
        print(f"Warning: Could not extract image from slide {slide_num}: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pptx.py <input.pptx> [output_dir]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    extract_pptx(input_file, output_dir)
```

### Step 1.2: Run Extraction

```bash
python extract_pptx.py presentation.pptx ./my-presentation
```

This creates:
- `my-presentation/extracted_content.json` — Structured content
- `my-presentation/assets/` — Extracted images

---

## Phase 2: Review Extracted Content

Present the extraction summary to the user:

```
I've extracted content from your PowerPoint:

**Source:** presentation.pptx
**Slides:** 12

**Slide 1: "Welcome to Our Company"** (Title Slide)
- Subtitle text
- 1 image

**Slide 2: "Our Mission"** (Title and Content)
- 3 bullet points
- Speaker notes: "Emphasize the customer focus..."

**Slide 3: "Key Metrics"** (Two Content)
- Table (3 rows × 4 columns)
- 2 images

...

All images saved to assets/ folder.

Does this look correct? Ready to choose a visual style?
```

### Handling Issues

| Issue | Solution |
|-------|----------|
| Missing text | Some SmartArt/charts don't extract cleanly — note for manual recreation |
| Image quality | Original resolution preserved; suggest optimization if files are large |
| Complex layouts | Note which slides may need manual adjustment |
| Speaker notes | Preserve as HTML comments or separate file |

---

## Phase 3: Style Selection

Proceed to style discovery. See [html-slides-style/SKILL.md](../html-slides-style/SKILL.md).

The user may want to:
- Match the original PPT style (extract colors if possible)
- Choose a completely new style
- Enhance with animations the PPT didn't have

---

## Phase 4: Generate Slide Files

### Step 4.1: Create Project Structure

```bash
mkdir -p my-presentation/slides
# assets/ already created by extraction
```

### Step 4.2: Create Template Files

Based on chosen style, create `template-header.html` and `template-footer.html`.

See [html-slides-style/SKILL.md](../html-slides-style/SKILL.md) for templates.

### Step 4.3: Convert Each Slide

Map extracted content to slide files using patterns from [html-slides-slide/SKILL.md](../html-slides-slide/SKILL.md).

#### Content Type Mapping

| PPT Content | HTML Pattern |
|-------------|--------------|
| Title + subtitle | Title slide |
| Bullets | List slide or Content slide |
| Two columns | Two-column slide |
| Image + text | Image slide variant |
| Table | Table HTML |
| Chart | Describe or recreate (charts don't extract) |
| SmartArt | Recreate manually |

#### Example Conversion

**Extracted JSON:**
```json
{
  "number": 3,
  "title": "Our Services",
  "content": [
    {
      "type": "text",
      "content": [
        {"text": "Consulting", "level": 0},
        {"text": "Help you define strategy", "level": 1},
        {"text": "Development", "level": 0},
        {"text": "Build custom solutions", "level": 1},
        {"text": "Support", "level": 0},
        {"text": "24/7 assistance", "level": 1}
      ]
    }
  ],
  "images": []
}
```

**Generated slide file:**
```html
<!-- slides/03-services.html -->
<section class="slide">
    <h2 class="reveal">Our Services</h2>
    <div class="icon-rows">
        <div class="icon-row reveal">
            <span class="icon">💼</span>
            <div>
                <h3>Consulting</h3>
                <p>Help you define strategy</p>
            </div>
        </div>
        <div class="icon-row reveal">
            <span class="icon">⚙️</span>
            <div>
                <h3>Development</h3>
                <p>Build custom solutions</p>
            </div>
        </div>
        <div class="icon-row reveal">
            <span class="icon">🛟</span>
            <div>
                <h3>Support</h3>
                <p>24/7 assistance</p>
            </div>
        </div>
    </div>
</section>
```

**Note:** The conversion improves the presentation, not just translates it literally. Bullets become icon rows, plain text gets visual hierarchy.

#### Converting Tables

**Extracted:**
```json
{
  "type": "table",
  "content": {
    "rows": 3,
    "cols": 3,
    "data": [
      ["Feature", "Basic", "Pro"],
      ["Users", "5", "Unlimited"],
      ["Storage", "10GB", "100GB"]
    ]
  }
}
```

**Generated:**
```html
<section class="slide">
    <h2 class="reveal">Pricing Comparison</h2>
    <table class="reveal">
        <thead>
            <tr>
                <th>Feature</th>
                <th>Basic</th>
                <th>Pro</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Users</td>
                <td>5</td>
                <td>Unlimited</td>
            </tr>
            <tr>
                <td>Storage</td>
                <td>10GB</td>
                <td>100GB</td>
            </tr>
        </tbody>
    </table>
</section>
```

Add table styles to template-header.html:
```css
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
}

th, td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid var(--text-secondary);
}

th {
    font-weight: 600;
    color: var(--accent);
}

tr:hover {
    background: var(--bg-secondary);
}
```

#### Converting Images

**Extracted:**
```json
{
  "images": [
    {
      "path": "assets/slide05_img1.png",
      "alt": "Image from slide 5"
    }
  ]
}
```

**Generated:**
```html
<section class="slide">
    <h2 class="reveal">Product Screenshot</h2>
    <figure class="reveal">
        <img src="assets/slide05_img1.png" alt="Dashboard showing analytics view">
        <figcaption>Our intuitive dashboard</figcaption>
    </figure>
</section>
```

**Important:** Update the `alt` text to be descriptive.

### Step 4.4: Handle Speaker Notes

Option 1: HTML comments (preserved but hidden)
```html
<!-- slides/03-services.html -->
<!-- Speaker notes: Remember to mention the 24/7 support is included in all plans -->
<section class="slide">
    ...
</section>
```

Option 2: Separate notes file
```
my-presentation/
├── slides/
├── notes/
│   ├── 03-services.md
│   └── ...
```

Option 3: Data attribute (accessible via JS if needed)
```html
<section class="slide" data-notes="Remember to mention...">
```

---

## Phase 5: Build and Review

### Step 5.1: Create Build Script

```bash
#!/bin/bash
cat template-header.html > presentation.html
for slide in slides/*.html; do
    cat "$slide" >> presentation.html
done
cat template-footer.html >> presentation.html
echo "Built presentation.html"
```

### Step 5.2: Build and Preview

```bash
chmod +x build.sh
./build.sh
open presentation.html
```

### Step 5.3: Compare with Original

Open both the original PPT and the HTML version side by side. Check:

- [ ] All slides present
- [ ] Content accurate
- [ ] Images displaying correctly
- [ ] Visual hierarchy preserved or improved
- [ ] Nothing important lost

### Step 5.4: Iterate

Common adjustments after first build:
- Reword headlines for impact
- Add animations to static content
- Improve image placement
- Enhance data visualization
- Add visual elements PPT didn't have

---

## Automated Conversion Script

For faster conversion, use this script that generates slide files from extracted JSON:

```python
#!/usr/bin/env python3
"""
generate_slides.py - Generate HTML slide files from extracted content
"""

import json
import os
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
    import re
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
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generate_slides.py <extracted_content.json> [output_dir]")
        sys.exit(1)
    
    json_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    generate_slides(json_path, output_dir)
```

### Usage

```bash
# Step 1: Extract
python extract_pptx.py presentation.pptx ./my-presentation

# Step 2: Generate initial slides
python generate_slides.py ./my-presentation/extracted_content.json ./my-presentation

# Step 3: Review and refine individual slides
# Edit slides/*.html files as needed

# Step 4: Build
cd my-presentation
./build.sh
```

---

## Limitations

Content that **does not extract** cleanly:

| PPT Feature | Handling |
|-------------|----------|
| Charts | Screenshot or recreate with HTML/CSS |
| SmartArt | Recreate manually with appropriate pattern |
| Animations | Note timing, recreate with CSS animations |
| Transitions | Use scroll-snap; note if specific transition needed |
| Videos | Note file, embed with `<video>` tag |
| Audio | Note file, embed with `<audio>` tag |
| 3D models | Not supported; use static image |
| Complex shapes | Screenshot or recreate with SVG |

**Recommendation:** For slides with complex visuals, take a screenshot from the PPT and include as an image, then enhance progressively.

---

## Complete Conversion Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. User uploads presentation.pptx                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Run extract_pptx.py                                     │
│     → extracted_content.json                                │
│     → assets/ (images)                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Review extraction with user                             │
│     → Confirm content is complete                           │
│     → Note any complex elements                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Style discovery (html-slides-style)                 │
│     → Generate 3 style previews                             │
│     → User picks one                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  5. Create template files                                   │
│     → template-header.html (with chosen style)              │
│     → template-footer.html                                  │
│     → build.sh                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  6. Generate slide files                                    │
│     → Run generate_slides.py for initial version            │
│     → Refine each slide manually                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  7. Build and review                                        │
│     → ./build.sh                                            │
│     → Compare with original                                 │
│     → Iterate until satisfied                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  8. Deliver                                                 │
│     → Clean up temp files                                   │
│     → Test print to PDF                                     │
│     → Hand off presentation.html                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Related Skills

- **[html-slides](../html-slides/SKILL.md)** — Project setup and workflow
- **[html-slides-slide](../html-slides-slide/SKILL.md)** — Slide content patterns
- **[html-slides-style](../html-slides-style/SKILL.md)** — CSS and theming
