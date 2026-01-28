# HTML Slides Plugin

Create stunning, animation-rich HTML presentations with a multi-file workflow. This Claude Code plugin provides skills for slide authoring, theming, and PowerPoint conversion.

## Features

- **Multi-file workflow** - Organize slides as individual HTML files for easy editing
- **Rich animations** - CSS-powered reveal animations and scroll-snap navigation
- **Theming system** - Customizable styles with CSS variables
- **PowerPoint conversion** - Convert existing .pptx files to HTML presentations
- **Print-ready** - Optimized for PDF export

## Included Skills

| Skill | Description |
|-------|-------------|
| `/html-slides` | Main orchestrator - start here for new presentations |
| `/html-slides-slide` | Slide content authoring patterns |
| `/html-slides-style` | Theming and CSS customization |
| `/html-slides-pptx` | PowerPoint to HTML conversion |
| `/html-slides-image` | Add AI-generated images (requires `GEMINI_API_KEY`) |
| `/html-slides-style-extract` | Extract style from existing PPTX/PDF as template |

## Installation

### From GitHub (Recommended)

Install directly from GitHub without cloning:

```bash
claude skill add github:dekuple/html-slides-plugin
```

This adds the plugin to your Claude Code configuration. The skills will be available in all your Claude Code sessions.

### Local Installation

Alternatively, clone the repo and use it locally:

```bash
git clone https://github.com/dekuple/html-slides-plugin.git
cd html-slides-plugin
claude skill add .
```

## Usage

### Create a New Presentation

```
/html-slides
```

This starts an interactive workflow to:
1. Gather presentation requirements
2. Choose a visual style
3. Generate the project structure
4. Create slides iteratively

### Convert a PowerPoint File

```
/html-slides-pptx
```

Upload your .pptx file and the skill will:
1. Extract content and images
2. Help you choose a style
3. Generate HTML slide files
4. Build the final presentation

### Customize Styles

```
/html-slides-style
```

Explore theming options:
- Color schemes
- Typography
- Animation timing
- Layout variations

### Author Individual Slides

```
/html-slides-slide
```

Get patterns and templates for specific slide types:
- Title slides
- Content slides
- Image slides
- Two-column layouts
- Code slides
- And more...

## Project Structure

A typical presentation project:

```
my-presentation/
├── slides/
│   ├── 01-title.html
│   ├── 02-intro.html
│   └── ...
├── assets/
│   └── (images, etc.)
├── template-header.html
├── template-footer.html
├── build.sh
└── presentation.html (generated)
```

## Scripts

The `scripts/` directory contains Python utilities:

- **extract_pptx.py** - Extract content and images from PowerPoint files
- **generate_slides.py** - Generate HTML slides from extracted JSON

### Requirements

```bash
pip install python-pptx
```

## Acknowledgments

This plugin was inspired by and incorporates ideas and code from [frontend-slides](https://github.com/zarazhangrui/frontend-slides) by Zara Zhang. We gratefully acknowledge their work on creating elegant HTML presentation workflows.

## License

MIT - See [LICENSE](LICENSE) for details.
