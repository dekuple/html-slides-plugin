# CLAUDE.md

## Overview

A Claude Code plugin for creating HTML presentations. Six skills:
- `/html-slides` - Main workflow (start here)
- `/html-slides-slide` - Edit individual slides
- `/html-slides-style` - Modify theme/CSS
- `/html-slides-pptx` - Convert PowerPoint files
- `/html-slides-image` - Add images: download logos/web images, generate charts, or create AI illustrations (AI images require GEMINI_API_KEY)
- `/html-slides-style-extract` - Extract style from existing PPTX/PDF to use as template

## Build Command

```bash
./build.sh  # Concatenates template-header + slides/*.html + template-footer → presentation.html
```

## PowerPoint Conversion

```bash
pip install python-pptx
python scripts/extract_pptx.py input.pptx ./output-dir
python scripts/generate_slides.py ./output-dir/extracted_content.json ./output-dir
```

## Style Extraction

```bash
pip install python-pptx Pillow
python scripts/extract_style.py model.pptx [output.json]
# Outputs: CSS custom properties, image-style.json, Google Fonts link
```

## Key Conventions

- Slide files: `NN-name.html` (e.g., `01-title.html`) containing only `<section class="slide">...</section>`
- Each skill's SKILL.md in `skills/` has comprehensive patterns - reference those, don't repeat them
