# CLAUDE.md

## Overview

A Claude Code plugin for creating HTML presentations. Five skills:
- `/html-slides` - Main workflow (start here)
- `/html-slides-slide` - Edit individual slides
- `/html-slides-style` - Modify theme/CSS
- `/html-slides-pptx` - Convert PowerPoint files
- `/html-slides-image` - Add AI-generated images (requires GEMINI_API_KEY)

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

## Key Conventions

- Slide files: `NN-name.html` (e.g., `01-title.html`) containing only `<section class="slide">...</section>`
- Each skill's SKILL.md in `skills/` has comprehensive patterns - reference those, don't repeat them
