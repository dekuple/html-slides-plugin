---
name: html-slides-image
description: "Add AI-generated images to HTML presentations using Gemini 3 Pro Image Preview. Use sparingly for slides that genuinely benefit from visual content—not every slide needs an image."
---

# HTML Slides — AI Image Generation

Generate consistent, on-brand images for presentations using the Gemini 3 Pro Image Preview API.

## Quick Reference

| Task | Section |
|------|---------|
| Decide what type of image | [Unified Image Decision Logic](#unified-image-decision-logic) |
| Set up API access | [API Setup](#api-setup) |
| Create style signature | [Image Style Signature](#image-style-signature) |
| Decide which slides need images | [Image Scoring System](#image-scoring-system) |
| Download images from URLs | [Web Images](#web-images) |
| Generate data charts | [Charts](#charts) |
| Generate AI background images | [Background Images](#background-images) |
| Generate AI content images | [Content Images](#content-images) |

---

## Unified Image Decision Logic

This skill supports three types of images:

| Type | Use For | Script |
|------|---------|--------|
| **Chart** | Numeric data with 3+ data points | `scripts/generate_chart.py` |
| **Web Image** | Logos, known brands, reference imagery | `scripts/download_image.py` |
| **AI-Generated** | Abstract concepts, metaphors, atmosphere | `scripts/generate_image.py` |

### Decision Flowchart

When a slide scores >= 4 for image-worthiness, determine the image type:

```
Slide scores >= 4 for image?
│
├─ NO → No image needed
│
└─ YES → Analyze content:
         │
         ├─ Has numeric data (3+ labeled values)?
         │  → CHART (bar/pie/line)
         │
         ├─ References known entity (company, product, brand)?
         │  → WEB IMAGE (download logo/product shot)
         │
         ├─ User provided a URL?
         │  → WEB IMAGE (download from URL)
         │
         └─ Abstract concept, metaphor, or atmosphere?
            → AI-GENERATED (use Gemini API)
```

### Signal Detection Table

| Signal in Content | Image Type | Example |
|-------------------|------------|---------|
| Numbers with labels (Q1: $100K, Q2: $150K...) | **Chart** | Revenue slide |
| Percentages that add to 100% | **Chart (pie)** | Budget allocation |
| Time series data (Jan, Feb, Mar...) | **Chart (line)** | Growth trends |
| Company/brand name mentioned | **Web Image** | "Our partners include Acme Corp" |
| Product name with visual identity | **Web Image** | "Integrates with Slack" |
| User says "use this image: [URL]" | **Web Image** | Direct request |
| Abstract noun (innovation, synergy) | **AI-Generated** | Concept slide |
| Process/workflow description | **AI-Generated** | How-it-works slide |
| Atmosphere/mood request | **AI-Generated** | Title slide background |

### Unified Recommendation Format

When presenting image recommendations to the user:

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
```

---

## Core Philosophy

**Images are not decoration.** Only add images when they:

1. **Explain an abstract concept** — "workflow automation" becomes clearer with a visual
2. **Fill a visual gap** — a two-column layout with an empty side
3. **Support narrative content** — storytelling benefits from imagery
4. **Create atmosphere** — title/section slides can use subtle backgrounds

**Never add images to:**
- Stats slides (numbers are the visual)
- Code slides (code is the content)
- Quote slides (the words are the focus)
- Simple bullet lists (they don't need illustration)

---

## API Setup

### Environment Variable

The generation script requires `GEMINI_API_KEY`:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Getting an API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with Google account
3. Create API key
4. Save securely

### Error Handling

If `GEMINI_API_KEY` is missing:

```
Error: GEMINI_API_KEY environment variable not set.

To generate images, you need a Gemini API key:
1. Go to https://aistudio.google.com/
2. Sign in and create an API key
3. Run: export GEMINI_API_KEY="your-key"
```

---

## Image Style Signature

All images in a presentation share visual DNA via a **style signature** stored in `.claude-design/image-style.json`.

### Purpose

Without a style signature, AI-generated images would have inconsistent aesthetics—some photorealistic, some illustrated, different color temperatures. The signature ensures cohesion.

### Structure

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
  "negative_prompt": "photorealistic, 3D render, cluttered, neon, stock photo, cheesy, corporate clip art"
}
```

### Creating a Style Signature

Derive the signature from the presentation's CSS variables in `template-header.html`:

```css
:root {
    --bg-primary: #faf7f2;      /* → background */
    --text-primary: #292524;    /* → primary */
    --text-secondary: #78716c;  /* → secondary */
    --accent: #b45309;          /* → accent */
}
```

**Map moods to visual styles:**

| Mood | Style Keywords |
|------|----------------|
| Impressed/Confident | professional, clean lines, subtle gradients, sophisticated |
| Excited/Energized | bold shapes, dynamic angles, vibrant, high contrast |
| Calm/Focused | minimalist, soft shadows, muted tones, editorial |
| Inspired/Moved | cinematic, atmospheric, depth, emotive lighting |

### Example Signatures by Theme

**Dark Tech Theme:**
```json
{
  "signature": "futuristic digital illustration, dark background with cyan accents (#00ffcc), circuit-like patterns, subtle glow effects",
  "mood": "excited/energized",
  "color_palette": {
    "primary": "#ffffff",
    "secondary": "#9ca3af",
    "accent": "#00ffcc",
    "background": "#0a0f1c"
  },
  "style_keywords": ["futuristic", "digital", "glow", "tech"],
  "negative_prompt": "photorealistic, warm colors, organic shapes, vintage"
}
```

**Warm Editorial Theme:**
```json
{
  "signature": "minimalist editorial illustration, warm paper texture, amber accent (#b45309), hand-drawn feel with clean lines",
  "mood": "calm/focused",
  "color_palette": {
    "primary": "#292524",
    "secondary": "#78716c",
    "accent": "#b45309",
    "background": "#faf7f2"
  },
  "style_keywords": ["editorial", "minimalist", "warm", "hand-drawn"],
  "negative_prompt": "neon, 3D render, photorealistic, cold colors, corporate"
}
```

**Corporate Professional Theme:**
```json
{
  "signature": "clean professional illustration, navy blue (#1e3a5f) and white, geometric shapes, business context",
  "mood": "impressed/confident",
  "color_palette": {
    "primary": "#1e293b",
    "secondary": "#64748b",
    "accent": "#2563eb",
    "background": "#ffffff"
  },
  "style_keywords": ["professional", "clean", "geometric", "corporate"],
  "negative_prompt": "cartoon, playful, neon, grunge, hand-drawn"
}
```

---

## Image Scoring System

Not every slide needs an image. Use this scoring system to identify candidates:

### Scoring Factors

| Factor | Score |
|--------|-------|
| Explains abstract concept (e.g., "automation", "synergy", "growth") | +3 |
| Two-column layout with empty visual side | +2 |
| Narrative/story content (journey, transformation) | +2 |
| Section divider (benefits from atmosphere) | +1 |
| Already has an image | -5 |
| Stats/metrics slide | -3 |
| Code snippet slide | -3 |
| Quote slide | -3 |
| Simple bullet list (no conceptual content) | -2 |

### Threshold

**Only generate images for slides scoring >= 4** (conservative approach).

### Example Scoring

**Slide: "How Automation Transforms Your Workflow"**
- Abstract concept (automation, transforms): +3
- Narrative content (transformation story): +2
- **Total: 5** → Candidate for image

**Slide: "Our Q3 Results"**
- Stats slide: -3
- **Total: -3** → No image

**Slide: "The Problem"**
- Two-column layout, one side empty: +2
- Abstract concept (problem visualization): +3
- **Total: 5** → Candidate for image

**Slide: "Key Takeaways"**
- Simple bullet list: -2
- **Total: -2** → No image

### User Confirmation

Always present recommendations before generating:

```
Based on the content, I recommend adding AI-generated images to these slides:

**Slide 3: "How Automation Works"** (score: 5)
→ Concept illustration showing workflow transformation

**Slide 7: "Our Approach"** (score: 4)
→ Two-column with visual on right

Would you like me to generate these? You can also:
- Remove slides from this list
- Add other slides you'd like images for
- Skip image generation entirely
```

---

## Web Images

Download images from URLs for logos, product shots, and reference imagery.

### Use Cases

- Company/partner logos
- Product screenshots
- Reference designs
- User-provided image URLs

### Download Script

```bash
# Basic download
python scripts/download_image.py \
  --url "https://example.com/logo.png" \
  --output assets/company-logo.png

# With resize limit (requires Pillow)
python scripts/download_image.py \
  --url "https://example.com/large-image.jpg" \
  --output assets/image.jpg \
  --max-size 2048

# With custom timeout
python scripts/download_image.py \
  --url "https://slow-server.com/image.png" \
  --output assets/image.png \
  --timeout 60
```

### Options

| Option | Description |
|--------|-------------|
| `--url`, `-u` | URL of the image to download (required) |
| `--output`, `-o` | Output file path (required) |
| `--max-size` | Max dimension in pixels; resize if larger |
| `--timeout` | Request timeout in seconds (default: 30) |

### Output

```
Downloading: https://example.com/logo.png

Downloaded: assets/company-logo.png
Suggested alt text: "Image: Company Logo"
```

### Best Practices for Web Images

**Do:**
- Verify URL is publicly accessible before downloading
- Use `--max-size` to avoid huge files
- Save with descriptive filenames (`partner-acme.png`, not `image1.png`)
- Include proper attribution if required by source

**Don't:**
- Download copyrighted images without permission
- Use web images for concepts that should be AI-generated
- Skip the alt text

### Slide Patterns for Web Images

See [html-slides-slide/SKILL.md](../html-slides-slide/SKILL.md) for:
- Partner logo grids
- Product screenshots
- Reference image slides

---

## Charts

Generate SVG charts from numeric data. Pure vector graphics for print-friendly output.

### Chart Types

| Type | Use For |
|------|---------|
| `bar` | Comparing discrete categories |
| `pie` | Showing parts of a whole (percentages) |
| `line` | Trends over time |

### Chart Script

```bash
# Bar chart
python scripts/generate_chart.py \
  --type bar \
  --data '{"labels": ["Q1","Q2","Q3","Q4"], "values": [100,150,200,180]}' \
  --output assets/revenue-chart.svg

# Pie chart
python scripts/generate_chart.py \
  --type pie \
  --data '{"labels": ["Sales","Marketing","R&D"], "values": [45,30,25]}' \
  --output assets/budget-chart.svg

# Line chart
python scripts/generate_chart.py \
  --type line \
  --data '{"labels": ["Jan","Feb","Mar","Apr","May"], "values": [10,25,15,30,45]}' \
  --output assets/growth-chart.svg

# With style file for theming
python scripts/generate_chart.py \
  --type bar \
  --data '{"labels": ["A","B","C"], "values": [10,20,30]}' \
  --style-file .claude-design/image-style.json \
  --title "Performance Metrics" \
  --output assets/metrics-chart.svg
```

### Data Format

```json
{
  "labels": ["Category 1", "Category 2", "Category 3"],
  "values": [100, 150, 200]
}
```

- `labels`: Array of strings for X-axis or legend
- `values`: Array of numbers (same length as labels)

### Options

| Option | Description |
|--------|-------------|
| `--type`, `-t` | Chart type: `bar`, `pie`, or `line` (required) |
| `--data`, `-d` | JSON data with labels and values (required) |
| `--output`, `-o` | Output SVG file path (required) |
| `--style-file` | Path to image-style.json for theming |
| `--title` | Chart title (optional) |
| `--width` | Chart width in pixels (default: 600) |
| `--height` | Chart height in pixels (default: 400) |

### Output

```
Generated: assets/revenue-chart.svg
Suggested alt text: "Bar chart showing Q1: 100, Q2: 150, Q3: 200, Q4: 180"
```

### Choosing Chart Types

| Data Pattern | Recommended Chart |
|--------------|-------------------|
| Comparing 3-8 categories | **Bar chart** |
| Parts of a whole (must sum to 100%) | **Pie chart** |
| Changes over time (5+ points) | **Line chart** |
| Before/after comparison | **Bar chart** (2 bars) |
| Multiple series | **Line chart** or grouped bar |

### Chart Theming

When you provide `--style-file`, the chart uses colors from the presentation theme:

- **Primary color** → Text and axis labels
- **Secondary color** → Gridlines and captions
- **Accent color** → First bar/line color, pie chart primary

### Slide Patterns for Charts

See [html-slides-slide/SKILL.md](../html-slides-slide/SKILL.md) for:
- Full-width chart slides
- Chart with explanation (two-column)
- Multiple charts comparison

### Print Quality

SVG charts are vector graphics—they scale perfectly for print:
- No pixelation at any size
- Small file size
- Colors adjust automatically in print mode

---

## Background Images

Atmospheric images for title and section slides. No focal point—they create mood.

### Characteristics

- **Subtle**: Won't compete with text
- **Atmospheric**: Gradients, textures, abstract patterns
- **Dark/desaturated**: Works with text overlay
- **No subjects**: No people, objects, or focal points

### Prompt Pattern

```
Abstract atmospheric background, [style signature],
subtle gradient from [color1] to [color2],
soft texture, no focal point, no objects, no text,
suitable for text overlay
```

### Example Prompts

**Dark Tech:**
```
Abstract atmospheric background, futuristic digital aesthetic,
subtle gradient from deep navy (#0a0f1c) to dark gray,
faint circuit-like patterns, soft cyan glow in corner,
no focal point, no objects, suitable for text overlay
```

**Warm Editorial:**
```
Abstract atmospheric background, warm paper texture,
subtle gradient from cream (#faf7f2) to soft tan,
gentle organic shapes, editorial feel,
no focal point, no objects, suitable for text overlay
```

### CSS for Background Image Slides

See [html-slides-style/SKILL.md](../html-slides-style/SKILL.md) for the `.slide--background-image` modifier.

---

## Content Images

Concept illustrations that visualize ideas. These have a subject and focal point.

### Characteristics

- **Conceptual**: Represents an idea, not a literal photo
- **Clean composition**: Single focal point
- **On-brand**: Uses style signature colors and aesthetics
- **Appropriate scale**: Works in the slide context

### Prompt Pattern

```
[Style signature], [concept description],
[composition guidance], [color constraints],
clean background, professional presentation quality
```

### Example Prompts

**Workflow Automation:**
```
Minimalist editorial illustration, workflow automation concept,
interconnected gears and flowing arrows representing seamless process,
warm earth tones with amber accent (#b45309),
clean white background, soft shadows, professional quality
```

**Data Security:**
```
Futuristic digital illustration, data security concept,
shield icon with circuit patterns and lock symbol,
dark background with cyan (#00ffcc) glow effects,
tech aesthetic, clean composition, professional quality
```

**Team Collaboration:**
```
Clean professional illustration, team collaboration concept,
abstract figures working together around shared project,
navy blue (#1e3a5f) and white color scheme,
geometric shapes, corporate aesthetic, clean background
```

### Prompt Engineering Tips

1. **Be specific about style**: "minimalist illustration" not just "illustration"
2. **Include colors as hex codes**: Models understand color values
3. **Describe composition**: "centered", "left-aligned", "with negative space on right"
4. **Avoid clichés**: Skip "handshake", "lightbulb", "puzzle pieces" unless truly needed
5. **Add negative prompt**: Exclude unwanted styles explicitly

---

## Generation Scripts

Three scripts for three image types. All use Python standard library only (no pip install required):

| Script | Purpose | Requirements |
|--------|---------|--------------|
| `scripts/generate_image.py` | AI-generated images | `GEMINI_API_KEY` env var |
| `scripts/download_image.py` | Web images | None (optional `Pillow` for resize) |
| `scripts/generate_chart.py` | SVG charts | None |

### AI Image Generation (generate_image.py)

```bash
# Direct prompt
python scripts/generate_image.py \
  --prompt "minimalist illustration of workflow automation" \
  --output assets/workflow.png

# With style signature
python scripts/generate_image.py \
  --style-file .claude-design/image-style.json \
  --concept "workflow automation with interconnected gears" \
  --output assets/slide03-workflow.png

# Background image
python scripts/generate_image.py \
  --style-file .claude-design/image-style.json \
  --type background \
  --output assets/title-bg.png
```

**Options:**

| Option | Description |
|--------|-------------|
| `--prompt` | Full prompt (ignores style file) |
| `--style-file` | Path to image-style.json |
| `--concept` | Concept description (combined with style) |
| `--output` | Output file path |
| `--type` | `content` (default) or `background` |
| `--size` | `1024x1024` (default), `1024x768`, `768x1024` |

### Web Image Download (download_image.py)

```bash
python scripts/download_image.py \
  --url "https://example.com/logo.png" \
  --output assets/logo.png \
  --max-size 1024
```

**Options:**

| Option | Description |
|--------|-------------|
| `--url`, `-u` | Source URL (required) |
| `--output`, `-o` | Output file path (required) |
| `--max-size` | Resize if larger than this (optional) |
| `--timeout` | Request timeout in seconds (default: 30) |

### Chart Generation (generate_chart.py)

```bash
python scripts/generate_chart.py \
  --type bar \
  --data '{"labels": ["A","B","C"], "values": [10,20,30]}' \
  --style-file .claude-design/image-style.json \
  --title "Comparison" \
  --output assets/chart.svg
```

**Options:**

| Option | Description |
|--------|-------------|
| `--type`, `-t` | `bar`, `pie`, or `line` (required) |
| `--data`, `-d` | JSON with labels and values (required) |
| `--output`, `-o` | Output SVG path (required) |
| `--style-file` | Theme colors from image-style.json |
| `--title` | Chart title (optional) |
| `--width` | Width in pixels (default: 600) |
| `--height` | Height in pixels (default: 400) |

### Output Format

All scripts return:
1. Status message
2. Suggested alt text

```
Generated: assets/slide03-workflow.png
Suggested alt text: "Illustration representing workflow automation"
```

---

## Workflow Integration

### In Main Workflow (html-slides/SKILL.md)

**Phase 2.4 — After style selection:**

1. Extract colors from chosen CSS theme
2. Map mood to style keywords
3. Generate image-style.json
4. Optionally generate a sample image to preview style

**Phase 3.1b — Before slide generation:**

1. Score each planned slide for image-worthiness
2. Present recommendations to user
3. Generate approved images
4. Update slide files with image references

### File Locations

```
my-presentation/
├── .claude-design/
│   ├── style-previews/
│   └── image-style.json      ← Style signature
├── assets/
│   ├── slide03-workflow.png  ← Generated images
│   ├── slide07-approach.png
│   └── ...
├── slides/
│   ├── 03-workflow.html      ← References the image
│   └── ...
```

---

## Best Practices

### Do

- **Generate sparingly**: 2-4 images per 10-slide deck is plenty
- **Confirm with user**: Always show recommendations before generating
- **Use consistent style**: All images should feel like they belong together
- **Optimize for print**: Generated images should work in grayscale
- **Write good alt text**: Describe what the image represents, not just what it shows

### Don't

- **Don't illustrate everything**: Not every concept needs a visual
- **Don't use generic stock imagery prompts**: Avoid "business team meeting"
- **Don't forget the negative prompt**: Exclude unwanted styles explicitly
- **Don't skip user confirmation**: Image generation costs API credits
- **Don't generate very small images**: Minimum 1024px on one dimension

### Alt Text Guidelines

**Good:**
```html
<img src="assets/workflow.png"
     alt="Illustration showing interconnected steps in an automation workflow">
```

**Bad:**
```html
<img src="assets/workflow.png" alt="Image">
<img src="assets/workflow.png" alt="AI generated image">
<img src="assets/workflow.png" alt="workflow.png">
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API key not found | Set `GEMINI_API_KEY` environment variable |
| Rate limit exceeded | Wait and retry; reduce batch size |
| Image doesn't match style | Strengthen style keywords in signature; add more negative prompts |
| Image too busy | Add "clean background", "minimal elements" to prompt |
| Colors don't match | Use explicit hex codes in prompt |
| Generation fails | Check API status; verify prompt isn't triggering content filters |

---

## Related Skills

- **[html-slides](../html-slides/SKILL.md)** — Main workflow and project setup
- **[html-slides-slide](../html-slides-slide/SKILL.md)** — Slide patterns including image slides
- **[html-slides-style](../html-slides-style/SKILL.md)** — CSS for background images
