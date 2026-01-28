---
name: html-slides
description: "Create stunning, animation-rich HTML presentations with a multi-file workflow optimized for iterative editing. Use when the user wants to build a web-based slide deck, convert a PPT/PPTX to HTML, or create presentations that can be printed to PDF with one slide per page."
---

# HTML Slides Skill

Create zero-dependency, animation-rich HTML presentations using a multi-file architecture designed for efficient editing with Claude Code.

## Quick Reference

| Task | Action |
|------|--------|
| Start new presentation | Follow [Phase 1: Setup](#phase-1-project-setup) |
| Edit a single slide | Read [html-slides-slide/SKILL.md](../html-slides-slide/SKILL.md) |
| Change theme/animations | Read [html-slides-style/SKILL.md](../html-slides-style/SKILL.md) |
| Convert from PowerPoint | Read [html-slides-pptx/SKILL.md](../html-slides-pptx/SKILL.md) |
| Add AI-generated images | Read [html-slides-image/SKILL.md](../html-slides-image/SKILL.md) |
| Build final presentation | Run `./build.sh` |
| Preview in browser | `open presentation.html` |

---

## Core Philosophy

1. **Multi-File Architecture** — Individual slide files for efficient editing. Claude only reads/writes the files it needs.
2. **Zero Dependencies at Runtime** — Final output is a single HTML file with inline CSS/JS. No npm, no build tools for the user.
3. **Print-Ready** — Browser's print function produces a PDF with one slide per page.
4. **Show, Don't Tell** — Generate visual previews for style selection, not abstract choices.
5. **Distinctive Design** — Avoid generic "AI slop" aesthetics. Every presentation should feel custom-crafted.

---

## Project Structure

```
my-presentation/
├── slides/
│   ├── 01-title.html
│   ├── 02-problem.html
│   ├── 03-solution.html
│   └── ...
├── assets/
│   └── (images, if any)
├── template-header.html
├── template-footer.html
├── build.sh
├── presentation.html      ← generated output
└── .claude-design/        ← temporary design files (gitignore)
    └── style-previews/
```

**Key principle:** Each slide is a tiny file (~20-50 lines) containing only a `<section class="slide">` element. The template files contain `<head>`, styles, and scripts.

---

## Phase 0: Detect Mode

Determine what the user wants:

| Mode | Trigger | Action |
|------|---------|--------|
| **New Presentation** | "Create a presentation about..." | → Phase 1 |
| **PPT Conversion** | User uploads .ppt/.pptx | → [html-slides-pptx](../html-slides-pptx/SKILL.md) |
| **Enhancement** | "Improve my presentation" + existing project | → Assess and enhance |
| **Single Slide Edit** | "Edit slide 5" or "Add a slide after intro" | → [html-slides-slide](../html-slides-slide/SKILL.md) |
| **Style Change** | "Make it darker" or "Change the animations" | → [html-slides-style](../html-slides-style/SKILL.md) |

---

## Phase 1: Project Setup

### Step 1.1: Create Directory Structure

```bash
mkdir -p my-presentation/slides my-presentation/assets my-presentation/.claude-design/style-previews
cd my-presentation
```

### Step 1.2: Create Build Script

```bash
#!/bin/bash
# build.sh - Concatenates slides into final presentation

set -e

# Concatenate: header + all slides (sorted) + footer
cat template-header.html > presentation.html
for slide in slides/*.html; do
    cat "$slide" >> presentation.html
done
cat template-footer.html >> presentation.html

echo "Built presentation.html with $(ls -1 slides/*.html | wc -l) slides"
```

Make executable: `chmod +x build.sh`

### Step 1.3: Gather Content Requirements

**REQUIRED: You MUST ask the user these questions and wait for their response before proceeding to Phase 2. Do not assume defaults or skip this step, even if the user provides content.**

Ask the user:

**Purpose:**
- Pitch deck (selling an idea/product)
- Teaching/Tutorial (explaining concepts)
- Conference talk (speaking at an event)
- Internal presentation (team updates)

**Length:**
- Short (5-10 slides)
- Medium (10-20 slides)
- Long (20+ slides)

**Content Status:**
- Content ready (just need design)
- Rough notes (need organization)
- Topic only (need full outline)

If the user has content, ask them to share it.

---

## Phase 2: Style Discovery

**REQUIRED: Do not proceed to Phase 3 until the user has explicitly selected a style from the previews you generate. Never choose a style autonomously.**

**This is the "show, don't tell" phase.** Most people can't articulate design preferences in words.

### Step 2.1: Ask About Desired Feeling

What feeling should the audience have?

| Feeling | Description |
|---------|-------------|
| Impressed/Confident | Professional, trustworthy |
| Excited/Energized | Innovative, bold, futuristic |
| Calm/Focused | Clear, thoughtful, easy to follow |
| Inspired/Moved | Emotional, storytelling, memorable |

User can pick up to 2.

### Step 2.2: Generate Style Previews

Based on mood, generate **3 distinct style previews** as single-slide HTML files.

See [html-slides-style/SKILL.md](../html-slides-style/SKILL.md) for:
- Style templates for each mood
- CSS custom properties structure
- Animation patterns

Create previews in `.claude-design/style-previews/`:
- `style-a.html` — e.g., "Corporate Elegant"
- `style-b.html` — e.g., "Neon Cyber"
- `style-c.html` — e.g., "Warm Editorial"

Each preview should be self-contained, showing typography, colors, and animation style.

### Step 2.3: Present and Iterate

```
I've created 3 style previews:

**Style A: [Name]** — [1 sentence description]
**Style B: [Name]** — [1 sentence description]
**Style C: [Name]** — [1 sentence description]

Open each to see them in action, then tell me:
1. Which resonates most?
2. What do you like about it?
3. Anything you'd change?
```

### Step 2.4: Generate Image Style Signature (Optional)

If the presentation may benefit from AI-generated images, create an image style signature derived from the chosen CSS theme.

**Create `.claude-design/image-style.json`:**

```json
{
  "signature": "minimalist illustration, muted earth tones (#292524, #78716c), soft shadows, editorial feel",
  "mood": "calm/focused",
  "color_palette": {
    "primary": "#292524",
    "secondary": "#78716c",
    "accent": "#b45309",
    "background": "#faf7f2"
  },
  "style_keywords": ["minimalist", "illustration", "soft shadows", "editorial"],
  "negative_prompt": "photorealistic, 3D render, cluttered, neon, stock photo"
}
```

**Derive from CSS variables:**

| CSS Variable | Maps To |
|--------------|---------|
| `--text-primary` | `color_palette.primary` |
| `--text-secondary` | `color_palette.secondary` |
| `--accent` | `color_palette.accent` |
| `--bg-primary` | `color_palette.background` |

**Map mood to style keywords:**

| Mood | Style Keywords |
|------|----------------|
| Impressed/Confident | professional, clean lines, sophisticated |
| Excited/Energized | bold shapes, dynamic, vibrant |
| Calm/Focused | minimalist, soft shadows, editorial |
| Inspired/Moved | cinematic, atmospheric, emotive |

See [html-slides-image/SKILL.md](../html-slides-image/SKILL.md) for complete signature examples.

---

## Phase 3: Generate Presentation

**PREREQUISITE: Only enter this phase after the user has:**
1. **Answered the content requirements questions** (Phase 1, Step 1.3)
2. **Selected a style from the previews** (Phase 2, Step 2.3)

If you haven't completed both interactions, STOP and go back.

### Step 3.1: Create Template Files

Based on chosen style, create:
- `template-header.html` — DOCTYPE through opening `<body>` and any wrapper elements
- `template-footer.html` — Closing elements, navigation JS, closing `</body></html>`

**Read [html-slides-style/SKILL.md](../html-slides-style/SKILL.md) for template structure.**

### Step 3.1b: Evaluate Slides for Images (Optional)

If an image style signature was created in Phase 2.4, evaluate which slides would benefit from images.

**Use this scoring system:**

| Factor | Score |
|--------|-------|
| Explains abstract concept | +3 |
| Two-column with empty visual side | +2 |
| Narrative/story content | +2 |
| Section divider | +1 |
| Already has an image | -5 |
| Stats/metrics slide | -3 |
| Code/quote slide | -3 |
| Simple bullet list | -2 |

**Only recommend images for slides scoring >= 4.**

**Determine image type for each qualifying slide:**

| Signal in Content | Image Type |
|-------------------|------------|
| Numeric data (3+ labeled values) | **Chart** |
| Company/brand/product reference | **Web Image** |
| User-provided URL | **Web Image** |
| Abstract concept, metaphor | **AI-Generated** |

**Present unified recommendations:**

```
Based on content analysis, I recommend these images:

**Slide 3: "Revenue Growth"** (score: 5)
→ Type: CHART (bar)
→ Data: Q1: $100K, Q2: $150K, Q3: $200K, Q4: $180K
→ Will generate: assets/slide03-revenue.svg

**Slide 5: "Our Partners"** (score: 4)
→ Type: WEB IMAGE
→ Source: Download logos for Acme, Globex, Initech
→ Will save to: assets/partner-*.png

**Slide 7: "How Automation Works"** (score: 5)
→ Type: AI-GENERATED
→ Concept: Workflow automation with interconnected steps
→ Will generate: assets/slide07-automation.png

Would you like me to proceed? You can:
- Change image types for any slide
- Remove slides from this list
- Add other slides
- Skip image generation entirely

Note: AI-generated images require GEMINI_API_KEY environment variable.
```

**Generate approved images using the appropriate script:**

```bash
# Chart
python scripts/generate_chart.py \
  --type bar \
  --data '{"labels": ["Q1","Q2","Q3","Q4"], "values": [100,150,200,180]}' \
  --style-file .claude-design/image-style.json \
  --title "Revenue Growth" \
  --output assets/slide03-revenue.svg

# Web image
python scripts/download_image.py \
  --url "https://example.com/acme-logo.png" \
  --output assets/partner-acme.png \
  --max-size 512

# AI-generated
python scripts/generate_image.py \
  --style-file .claude-design/image-style.json \
  --concept "workflow automation with interconnected steps" \
  --output assets/slide07-automation.png
```

See [html-slides-image/SKILL.md](../html-slides-image/SKILL.md) for complete decision logic and best practices.

### Step 3.2: Create Individual Slides

For each slide, create a file in `slides/`:

```
slides/
├── 01-title.html
├── 02-agenda.html
├── 03-problem.html
├── 04-solution.html
├── 05-demo.html
└── ...
```

**Read [html-slides-slide/SKILL.md](../html-slides-slide/SKILL.md) for:**
- Slide file format
- Available slide types (title, content, image, comparison, etc.)
- Animation classes
- Naming conventions

### Step 3.3: Build and Preview

```bash
./build.sh
open presentation.html
```

---

## Phase 4: Iteration

When the user requests changes:

| Request | Action |
|---------|--------|
| "Edit slide 5" | Edit `slides/05-*.html` only |
| "Add a slide after the intro" | Create new file, renumber if needed |
| "Reorder slides" | Rename files to change numerical order |
| "Change the color scheme" | Edit `template-header.html` (CSS variables) |
| "Fix the animations" | Edit `template-header.html` or `template-footer.html` |
| "Preview changes" | Run `./build.sh && open presentation.html` |

**Key benefit:** Most edits only touch one small file, keeping context minimal.

**Note:** Slide numbers are displayed in the bottom-right corner of each slide (except title slides), making it easy to reference specific slides during editing. See [html-slides-style/SKILL.md](../html-slides-style/SKILL.md#slide-numbers) to customize the appearance.

---

## Phase 5: Delivery

### Step 5.1: Final Build

```bash
./build.sh
```

### Step 5.2: Verify Print Output

Critical: Test that printing produces one slide per page.

1. Open `presentation.html` in browser
2. Print → Preview (or Save as PDF)
3. Verify each slide is on its own page
4. Check no content is cut off

If print layout is broken, see [html-slides-style/SKILL.md](../html-slides-style/SKILL.md) for print CSS debugging.

### Step 5.3: Clean Up

```bash
rm -rf .claude-design/  # Remove temporary design files
```

### Step 5.4: Provide Summary

```
Your presentation is ready!

📁 File: presentation.html
🎨 Style: [Style Name]
📊 Slides: [count]

**To view:** Open presentation.html in any browser

**Navigation:**
- Arrow keys (← →) or Space to navigate
- Scroll/swipe also works
- Dots on the side to jump to slides

**To print as PDF:**
- Open in browser → Print → Save as PDF
- Each slide will be on its own page

**To edit later:**
- Individual slides are in slides/
- Run ./build.sh after changes

Would you like any adjustments?
```

---

## Reordering Slides

To reorder, rename files to change the numerical prefix:

```bash
# Move slide 03 to position 05
mv slides/03-solution.html slides/05-solution.html

# Renumber affected slides
mv slides/04-demo.html slides/03-demo.html
mv slides/05-conclusion.html slides/04-conclusion.html

# Rebuild
./build.sh
```

Or use a helper script:

```bash
# reorder.sh - Renumber slides sequentially
cd slides
i=1
for f in *.html; do
    name=$(echo "$f" | sed 's/^[0-9]*-//')
    mv "$f" "$(printf '%02d' $i)-$name"
    ((i++))
done
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Slides not appearing | Check `slides/*.html` files exist; run `./build.sh` |
| Print shows multiple slides per page | Check `@media print` CSS; see style skill |
| Animations not working | Verify JS in `template-footer.html`; check `.visible` class logic |
| Build fails | Ensure `template-header.html` and `template-footer.html` exist |
| Fonts not loading | Check font URLs in `template-header.html` |

---

## Related Skills

- **[html-slides-slide](../html-slides-slide/SKILL.md)** — Writing individual slide files
- **[html-slides-style](../html-slides-style/SKILL.md)** — Theme, CSS, animations, print styles
- **[html-slides-pptx](../html-slides-pptx/SKILL.md)** — Converting PowerPoint files
- **[html-slides-image](../html-slides-image/SKILL.md)** — AI-generated images
