---
name: html-slides-style-extract
description: Extract visual style from an existing presentation (PPTX or PDF) to use as a template for new presentations
---

# Style Extraction Skill

Extract colors, fonts, and visual patterns from an existing presentation to create a matching theme for new HTML slides.

## Quick Reference

| Task | Section |
|------|---------|
| Extract style from PPTX | Phase 1: PPTX Extraction |
| Extract style from PDF | Phase 2: PDF Analysis |
| Apply extracted style | Phase 3: Style Application |
| Fine-tune colors | Phase 4: Refinement |

## Prerequisites

```bash
pip install python-pptx Pillow
```

## Phase 0: Input Detection

REQUIRED: Determine the source format.

**If user provides a `.pptx` file:**
→ Go to Phase 1 (PPTX Extraction)

**If user provides a `.pdf` file:**
→ Go to Phase 2 (PDF Analysis)

**If user provides both or multiple files:**
→ Ask which should be the primary style source

## Phase 1: PPTX Extraction

### 1.1 Run the Extraction Script

```bash
python scripts/extract_style.py path/to/model.pptx extracted-style.json
```

The script extracts:
- **Background colors** from slide backgrounds
- **Text colors** categorized by brightness (primary, secondary, accent)
- **Fonts** with frequency analysis
- **Font sizes** for heading/body differentiation
- **Layout patterns** from slide layout names
- **Accent colors** from shapes and images (saturation-based detection)

### 1.2 Review Extracted Style

The script outputs:
1. **JSON style definition** - Complete extracted data
2. **CSS custom properties** - Ready to paste into template-header.html
3. **Image style JSON** - For .claude-design/image-style.json
4. **Google Fonts link** - For typography

Example output structure:
```json
{
  "metadata": {
    "source_file": "brand-deck.pptx",
    "slide_count": 24,
    "theme_type": "dark",
    "layouts_detected": ["Title Slide", "Title and Content", "Two Content"]
  },
  "colors": {
    "bg_primary": "#0f172a",
    "bg_secondary": "#1e293b",
    "text_primary": "#f8fafc",
    "text_secondary": "#94a3b8",
    "accent": "#3b82f6",
    "accent_glow": "#3b82f640"
  },
  "typography": {
    "font_display": "Montserrat",
    "font_body": "Open Sans",
    "heading_size_pt": 44,
    "body_size_pt": 18,
    "google_fonts_url": "https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Open+Sans:wght@400;600;700&display=swap"
  }
}
```

### 1.3 Validate Colors

Check the extracted colors make sense:
- **bg_primary** should be the dominant slide background
- **text_primary** should contrast well against bg_primary
- **accent** should be a saturated, attention-grabbing color

If colors look wrong, check `raw_data` in the JSON for alternatives.

## Phase 2: PDF Analysis

For PDF files, use visual analysis since there's no structured extraction.

### 2.1 Read the PDF

```
Use the Read tool to view the PDF pages visually.
```

### 2.2 Manual Style Extraction

Analyze the PDF and identify:

1. **Background color** - Most common slide background
2. **Text colors** - Primary (headings), secondary (body), accent (highlights)
3. **Typography** - Font families (or close Google Fonts alternatives)
4. **Layout patterns** - Common slide structures (title+content, two-column, etc.)

### 2.3 Create Style Definition Manually

Based on analysis, create the style JSON:

```json
{
  "metadata": {
    "source_file": "model-presentation.pdf",
    "theme_type": "light",
    "layouts_detected": ["title", "content", "two-column", "image-focused"]
  },
  "colors": {
    "bg_primary": "#ffffff",
    "bg_secondary": "#f3f4f6",
    "text_primary": "#1f2937",
    "text_secondary": "#6b7280",
    "accent": "#2563eb",
    "accent_glow": "#2563eb40"
  },
  "typography": {
    "font_display": "Poppins",
    "font_body": "Inter",
    "google_fonts_url": "https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@400;600;700&display=swap"
  }
}
```

## Phase 3: Style Application

### 3.1 Generate CSS Custom Properties

If using the script, CSS is auto-generated. Otherwise, create manually:

```css
:root {
    /* Colors */
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --accent: #3b82f6;
    --accent-glow: #3b82f640;

    /* Typography */
    --font-display: 'Montserrat', sans-serif;
    --font-body: 'Open Sans', sans-serif;

    /* Spacing */
    --slide-padding: clamp(2rem, 5vw, 4rem);

    /* Animation */
    --duration-normal: 0.6s;
    --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
}
```

### 3.2 Update template-header.html

1. Replace the Google Fonts `<link>` tag
2. Replace the `:root` CSS custom properties block
3. Keep all other CSS unchanged (base styles, animations, components, print styles)

### 3.3 Create image-style.json

Save to `.claude-design/image-style.json`:

```json
{
  "signature": "minimalist illustration, dark theme, colors (#0f172a, #3b82f6), soft shadows, editorial feel",
  "mood": "modern/dramatic",
  "color_palette": {
    "primary": "#f8fafc",
    "secondary": "#94a3b8",
    "accent": "#3b82f6",
    "background": "#0f172a"
  },
  "style_keywords": ["minimalist", "illustration", "soft shadows", "editorial", "dark"],
  "negative_prompt": "photorealistic, 3D render, cluttered, neon, stock photo"
}
```

### 3.4 Rebuild Presentation

```bash
./build.sh
```

## Phase 4: Refinement

### 4.1 Preview and Adjust

Open `presentation.html` in a browser. Check:
- [ ] Text is readable against backgrounds
- [ ] Accent color stands out appropriately
- [ ] Fonts load correctly
- [ ] Print preview looks correct (Cmd/Ctrl+P)

### 4.2 Common Adjustments

**Low contrast text:**
```css
/* Increase brightness difference */
--text-primary: #ffffff;  /* Was #f8fafc */
--text-secondary: #a1a1aa; /* Was #94a3b8 */
```

**Accent too subtle:**
```css
/* Increase saturation */
--accent: #60a5fa;  /* Lighter blue */
--accent-glow: #60a5fa60;  /* More visible glow */
```

**Font not loading:**
- Check Google Fonts URL is correct
- Use fallback: `'Font Name', 'Fallback Font', sans-serif`

### 4.3 Font Substitutions

Common PowerPoint fonts and their Google Fonts alternatives:

| PowerPoint Font | Google Fonts Alternative |
|-----------------|-------------------------|
| Calibri | Open Sans, Roboto |
| Cambria | Merriweather, Lora |
| Arial | Inter, Roboto |
| Times New Roman | Libre Baskerville, PT Serif |
| Segoe UI | Inter, Source Sans Pro |
| Century Gothic | Poppins, Raleway |
| Franklin Gothic | Oswald, Barlow |
| Garamond | EB Garamond, Cormorant Garamond |

## Integration with Other Skills

After extracting style, continue with:

- **`/html-slides`** - Use extracted theme for a new presentation
- **`/html-slides-pptx`** - Convert PPTX content while preserving extracted style
- **`/html-slides-style`** - Further customize the extracted theme

## Troubleshooting

### Script fails with "python-pptx not found"
```bash
pip install python-pptx Pillow
```

### Colors extracted are all black/white
The PPTX may use theme colors that aren't directly readable. Check `raw_data.all_text_colors` for alternatives, or analyze visually by opening the PPTX.

### Fonts don't match exactly
PowerPoint often uses proprietary or system fonts. Find the closest Google Fonts match using: https://fonts.google.com

### PDF analysis is imprecise
PDFs don't contain structured style data. Use the PDF as visual reference and manually match colors using a color picker tool or browser dev tools.
