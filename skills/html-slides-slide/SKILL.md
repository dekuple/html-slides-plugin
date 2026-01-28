---
name: html-slides-slide
description: "Write and edit individual slide files for HTML presentations. Use when creating a new slide, editing existing slide content, or needing slide layout patterns. Each slide is a small, self-contained file."
---

# HTML Slides — Slide Authoring

This skill covers writing individual slide files. Each slide is a tiny HTML file containing only a `<section>` element.

## Quick Reference

| Slide Type | Use For |
|------------|---------|
| [Title](#title-slide) | Opening slide, section breaks |
| [Content](#content-slide) | Text with optional subpoints |
| [Two-Column](#two-column-slide) | Side-by-side content |
| [Image](#image-slide) | Full or partial image with text |
| [Quote](#quote-slide) | Testimonials, key quotes |
| [Stats](#stats-slide) | Big numbers, metrics |
| [Comparison](#comparison-slide) | Before/after, pros/cons |
| [Code](#code-slide) | Code snippets |
| [List](#list-slide) | Bullet points, numbered items |
| [Closing](#closing-slide) | Call to action, thank you |

---

## File Format

### What a Slide File Contains

```html
<!-- slides/03-problem.html -->
<section class="slide">
    <h2 class="reveal">The Problem</h2>
    <p class="reveal">Users struggle to create presentations efficiently.</p>
</section>
```

**That's it.** No `<!DOCTYPE>`, no `<head>`, no `<script>`. Just the `<section>` element.

### What a Slide File Does NOT Contain

- ❌ `<!DOCTYPE html>`
- ❌ `<html>`, `<head>`, `<body>` tags
- ❌ `<style>` blocks (styles go in template-header.html)
- ❌ `<script>` blocks (scripts go in template-footer.html)
- ❌ Font imports
- ❌ CSS custom properties

The build script concatenates all slides between the template header and footer.

---

## Naming Convention

```
slides/
├── 01-title.html
├── 02-agenda.html
├── 03-problem.html
├── 04-solution.html
├── 05-demo.html
├── 06-pricing.html
├── 07-team.html
├── 08-closing.html
```

**Format:** `NN-descriptive-name.html`

- **NN** — Two-digit number for sort order (01-99)
- **descriptive-name** — Lowercase, hyphenated, describes content
- Always use `.html` extension

### Renumbering

To insert a slide between 03 and 04:
1. Create `04-new-slide.html`
2. Rename `04-solution.html` → `05-solution.html`
3. Continue renumbering downstream slides

Or: use gaps (01, 05, 10, 15...) to allow insertions without renumbering.

---

## Animation Classes

Apply these classes to elements for entrance animations. The `.visible` class is added by JavaScript when the slide enters the viewport.

| Class | Effect |
|-------|--------|
| `.reveal` | Fade in + slide up (default) |
| `.reveal-left` | Fade in + slide from left |
| `.reveal-right` | Fade in + slide from right |
| `.reveal-scale` | Fade in + scale up |
| `.reveal-blur` | Fade in + blur clear |

### Staggered Animation

Child elements animate sequentially based on their order:

```html
<section class="slide">
    <h2 class="reveal">Title</h2>           <!-- delay: 0.1s -->
    <p class="reveal">First point</p>       <!-- delay: 0.2s -->
    <p class="reveal">Second point</p>      <!-- delay: 0.3s -->
    <p class="reveal">Third point</p>       <!-- delay: 0.4s -->
</section>
```

### Custom Delay

For manual control, use inline styles:

```html
<p class="reveal" style="transition-delay: 0.5s;">Appears later</p>
```

---

## Slide Types

### Title Slide

Opening slide with presentation title and subtitle.

```html
<!-- slides/01-title.html -->
<section class="slide slide--title">
    <h1 class="reveal">Presentation Title</h1>
    <p class="reveal subtitle">Subtitle or Tagline</p>
    <p class="reveal author">Author Name · Date</p>
</section>
```

**Variants:**
- Add `slide--dark` for dark background
- Add `slide--center` to center all content

---

### Content Slide

Standard slide with heading and text content.

```html
<!-- slides/03-problem.html -->
<section class="slide">
    <h2 class="reveal">The Problem We're Solving</h2>
    <p class="reveal">
        Traditional presentation tools force a tradeoff between 
        design quality and editing efficiency.
    </p>
    <p class="reveal">
        Teams waste hours fighting with templates instead of 
        focusing on their message.
    </p>
</section>
```

---

### Two-Column Slide

Side-by-side content layout.

```html
<!-- slides/04-comparison.html -->
<section class="slide">
    <h2 class="reveal">Two Approaches</h2>
    <div class="columns">
        <div class="column reveal">
            <h3>Traditional Tools</h3>
            <p>Drag-and-drop interfaces that become unwieldy at scale.</p>
        </div>
        <div class="column reveal">
            <h3>Our Approach</h3>
            <p>Code-based slides that are easy to version and maintain.</p>
        </div>
    </div>
</section>
```

**For unequal columns**, use modifiers:

```html
<div class="columns columns--60-40">
    <div class="column">Wider content (60%)</div>
    <div class="column">Narrower content (40%)</div>
</div>
```

---

### Image Slide

Slide featuring an image prominently.

**Image with caption:**

```html
<!-- slides/05-product.html -->
<section class="slide">
    <h2 class="reveal">Our Product</h2>
    <figure class="reveal">
        <img src="assets/screenshot.png" alt="Product screenshot">
        <figcaption>Dashboard view showing key metrics</figcaption>
    </figure>
</section>
```

**Full-bleed image with text overlay:**

```html
<!-- slides/05-hero.html -->
<section class="slide slide--image" style="background-image: url('assets/hero.jpg');">
    <div class="overlay">
        <h2 class="reveal">Bold Statement</h2>
        <p class="reveal">Supporting text over the image</p>
    </div>
</section>
```

**Image alongside text:**

```html
<!-- slides/05-feature.html -->
<section class="slide">
    <div class="columns columns--50-50">
        <div class="column reveal">
            <h2>Feature Name</h2>
            <p>Description of what this feature does and why it matters.</p>
        </div>
        <div class="column reveal">
            <img src="assets/feature.png" alt="Feature illustration">
        </div>
    </div>
</section>
```

---

### Quote Slide

Testimonial or impactful quote.

```html
<!-- slides/06-testimonial.html -->
<section class="slide slide--quote">
    <blockquote class="reveal">
        <p>"This tool transformed how our team creates presentations. 
        We ship decks in half the time."</p>
        <footer>
            <cite>Jane Smith</cite>
            <span>CEO, Acme Corp</span>
        </footer>
    </blockquote>
</section>
```

---

### Stats Slide

Big numbers that make an impact.

```html
<!-- slides/07-metrics.html -->
<section class="slide">
    <h2 class="reveal">Our Impact</h2>
    <div class="stats">
        <div class="stat reveal">
            <span class="stat-number">50%</span>
            <span class="stat-label">Time Saved</span>
        </div>
        <div class="stat reveal">
            <span class="stat-number">10K+</span>
            <span class="stat-label">Users</span>
        </div>
        <div class="stat reveal">
            <span class="stat-number">99%</span>
            <span class="stat-label">Satisfaction</span>
        </div>
    </div>
</section>
```

---

### Comparison Slide

Before/after, pros/cons, or options comparison.

```html
<!-- slides/08-before-after.html -->
<section class="slide">
    <h2 class="reveal">Before & After</h2>
    <div class="comparison">
        <div class="comparison-item comparison-item--negative reveal">
            <h3>Before</h3>
            <ul>
                <li>Hours spent on formatting</li>
                <li>Inconsistent designs</li>
                <li>Difficult to update</li>
            </ul>
        </div>
        <div class="comparison-item comparison-item--positive reveal">
            <h3>After</h3>
            <ul>
                <li>Minutes to create</li>
                <li>Consistent, polished look</li>
                <li>Easy version control</li>
            </ul>
        </div>
    </div>
</section>
```

---

### Code Slide

Display code snippets with syntax context.

```html
<!-- slides/09-code.html -->
<section class="slide">
    <h2 class="reveal">Simple Configuration</h2>
    <pre class="reveal"><code class="language-bash">./build.sh
# Output: Built presentation.html with 12 slides</code></pre>
    <p class="reveal">One command to build your entire deck.</p>
</section>
```

**For longer code blocks**, consider reducing font size:

```html
<pre class="reveal code--small"><code>...</code></pre>
```

---

### List Slide

Bullet points or numbered items.

```html
<!-- slides/10-features.html -->
<section class="slide">
    <h2 class="reveal">Key Features</h2>
    <ul class="reveal-list">
        <li class="reveal">Zero dependencies at runtime</li>
        <li class="reveal">Print to PDF with one slide per page</li>
        <li class="reveal">Keyboard and touch navigation</li>
        <li class="reveal">Fully customizable themes</li>
    </ul>
</section>
```

**Keep lists short** — 4-6 items maximum per slide.

---

### Closing Slide

Final slide with call to action.

```html
<!-- slides/12-closing.html -->
<section class="slide slide--closing">
    <h2 class="reveal">Get Started Today</h2>
    <p class="reveal">Visit example.com/start</p>
    <div class="reveal contact">
        <p>Questions? hello@example.com</p>
    </div>
</section>
```

**Or a simple thank you:**

```html
<!-- slides/12-thanks.html -->
<section class="slide slide--title">
    <h1 class="reveal">Thank You</h1>
    <p class="reveal">@username · email@example.com</p>
</section>
```

---

## Slide Modifiers

Add these classes to `<section class="slide ...">` for variations:

| Class | Effect |
|-------|--------|
| `slide--title` | Centered, larger typography |
| `slide--dark` | Dark background variant |
| `slide--light` | Light background variant |
| `slide--center` | Center all content vertically and horizontally |
| `slide--image` | For background image slides |
| `slide--quote` | Optimized for blockquotes |
| `slide--closing` | Final slide styling |

Combine as needed: `<section class="slide slide--title slide--dark">`

---

## Content Guidelines

### Text Length

- **Headlines:** 2-8 words
- **Subheadings:** 5-12 words  
- **Body paragraphs:** 1-3 sentences (25-75 words)
- **Bullet points:** 5-15 words each

### Hierarchy

Each slide should have clear visual hierarchy:

1. **One main heading** (`<h2>`) — the slide's key message
2. **Supporting content** — text, images, or data that reinforces the heading
3. **Optional secondary elements** — captions, citations, notes

### One Idea Per Slide

If you're tempted to add "and also..." — make a new slide instead.

---

## Common Patterns

### Icon + Text Rows

```html
<section class="slide">
    <h2 class="reveal">How It Works</h2>
    <div class="icon-rows">
        <div class="icon-row reveal">
            <span class="icon">📝</span>
            <div>
                <h3>Write</h3>
                <p>Create slides as simple HTML files</p>
            </div>
        </div>
        <div class="icon-row reveal">
            <span class="icon">🔨</span>
            <div>
                <h3>Build</h3>
                <p>Run one command to generate output</p>
            </div>
        </div>
        <div class="icon-row reveal">
            <span class="icon">🚀</span>
            <div>
                <h3>Present</h3>
                <p>Open in any browser and go</p>
            </div>
        </div>
    </div>
</section>
```

### Timeline / Process

```html
<section class="slide">
    <h2 class="reveal">Our Journey</h2>
    <div class="timeline">
        <div class="timeline-item reveal">
            <span class="timeline-marker">2022</span>
            <p>Founded the company</p>
        </div>
        <div class="timeline-item reveal">
            <span class="timeline-marker">2023</span>
            <p>Launched MVP</p>
        </div>
        <div class="timeline-item reveal">
            <span class="timeline-marker">2024</span>
            <p>10,000 users</p>
        </div>
    </div>
</section>
```

### Cards Grid

```html
<section class="slide">
    <h2 class="reveal">Meet the Team</h2>
    <div class="cards">
        <div class="card reveal">
            <img src="assets/alice.jpg" alt="Alice">
            <h3>Alice</h3>
            <p>CEO</p>
        </div>
        <div class="card reveal">
            <img src="assets/bob.jpg" alt="Bob">
            <h3>Bob</h3>
            <p>CTO</p>
        </div>
        <div class="card reveal">
            <img src="assets/carol.jpg" alt="Carol">
            <h3>Carol</h3>
            <p>Design Lead</p>
        </div>
    </div>
</section>
```

### AI-Generated Image Slide

For slides with concept illustrations generated via [html-slides-image/SKILL.md](../html-slides-image/SKILL.md).

**Two-column with generated image:**

```html
<!-- slides/04-automation.html -->
<section class="slide">
    <div class="columns columns--60-40">
        <div class="column reveal-left">
            <h2>Workflow Automation</h2>
            <p>Streamline your processes with intelligent automation
            that learns and adapts to your team's needs.</p>
            <ul>
                <li>Reduce manual tasks by 50%</li>
                <li>Eliminate human error</li>
                <li>Scale without adding headcount</li>
            </ul>
        </div>
        <div class="column reveal-right">
            <figure class="generated-image">
                <img src="assets/slide04-automation.png"
                     alt="Illustration of interconnected workflow steps with flowing arrows">
            </figure>
        </div>
    </div>
</section>
```

**Full-width generated image with caption:**

```html
<!-- slides/05-approach.html -->
<section class="slide">
    <h2 class="reveal">Our Approach</h2>
    <figure class="generated-image reveal">
        <img src="assets/slide05-approach.png"
             alt="Illustration showing iterative design process with feedback loops">
        <figcaption>AI-generated concept illustration</figcaption>
    </figure>
</section>
```

**Title slide with AI background:**

```html
<!-- slides/01-title.html -->
<section class="slide slide--title slide--background-image"
         style="background-image: url('assets/title-bg.png');">
    <h1 class="reveal">Transform Your Business</h1>
    <p class="reveal subtitle">A new approach to workflow automation</p>
    <p class="reveal author">Jane Smith · Q1 2025</p>
</section>
```

### AI Image Best Practices

**Do:**
- Use `.generated-image` class for consistent styling
- Write descriptive alt text that explains the concept
- Place images to balance the slide composition
- Generate images sparingly (not every slide)

**Don't:**
- Use generic alt text like "AI image" or "illustration"
- Add images to stats, code, or quote slides
- Generate multiple similar images (reuse when appropriate)
- Forget to test print output with images

---

### Chart Slide

For slides with data visualizations generated via `scripts/generate_chart.py`.

**Bar chart example:**

```html
<!-- slides/05-metrics.html -->
<section class="slide">
    <h2 class="reveal">Revenue Growth</h2>
    <figure class="chart reveal">
        <img src="assets/slide05-revenue.svg" alt="Bar chart showing Q1: $100K, Q2: $150K, Q3: $200K, Q4: $180K">
        <figcaption>Quarterly revenue in thousands</figcaption>
    </figure>
</section>
```

**Chart with explanation:**

```html
<!-- slides/06-analysis.html -->
<section class="slide">
    <div class="columns columns--60-40">
        <div class="column reveal-left">
            <figure class="chart">
                <img src="assets/slide06-distribution.svg" alt="Pie chart showing Sales 45%, Marketing 30%, R&D 25%">
            </figure>
        </div>
        <div class="column reveal-right">
            <h2>Budget Allocation</h2>
            <p>Our investment priorities reflect our growth-focused strategy:</p>
            <ul>
                <li><strong>Sales (45%)</strong> — Expanding market reach</li>
                <li><strong>Marketing (30%)</strong> — Brand awareness</li>
                <li><strong>R&D (25%)</strong> — Product innovation</li>
            </ul>
        </div>
    </div>
</section>
```

**Line chart for trends:**

```html
<!-- slides/07-growth.html -->
<section class="slide">
    <h2 class="reveal">User Growth Trend</h2>
    <figure class="chart reveal">
        <img src="assets/slide07-users.svg" alt="Line chart showing user growth from 10K in Jan to 45K in May">
    </figure>
    <p class="reveal">350% growth in active users over 5 months</p>
</section>
```

---

### Web Image Slide

For slides using downloaded images (logos, reference imagery) via `scripts/download_image.py`.

**Partner logos:**

```html
<!-- slides/08-partners.html -->
<section class="slide slide--center">
    <h2 class="reveal">Trusted By Industry Leaders</h2>
    <div class="logo-grid reveal">
        <img src="assets/partner-acme.png" alt="Acme Corp logo">
        <img src="assets/partner-globex.png" alt="Globex logo">
        <img src="assets/partner-initech.png" alt="Initech logo">
        <img src="assets/partner-umbrella.png" alt="Umbrella Corp logo">
    </div>
</section>
```

**Product screenshot with web source:**

```html
<!-- slides/09-integration.html -->
<section class="slide">
    <div class="columns columns--50-50">
        <div class="column reveal-left">
            <h2>Seamless Integration</h2>
            <p>Works with the tools you already use.</p>
            <ul>
                <li>Slack notifications</li>
                <li>GitHub sync</li>
                <li>Jira tracking</li>
            </ul>
        </div>
        <div class="column reveal-right">
            <figure class="web-image">
                <img src="assets/integration-diagram.png" alt="Diagram showing connections between our product and Slack, GitHub, Jira">
            </figure>
        </div>
    </div>
</section>
```

**Reference image with attribution:**

```html
<!-- slides/10-inspiration.html -->
<section class="slide">
    <h2 class="reveal">Design Inspiration</h2>
    <figure class="web-image reveal">
        <img src="assets/reference-design.jpg" alt="Modern dashboard interface with dark theme">
        <figcaption>Image source: Dribbble / @designer</figcaption>
    </figure>
</section>
```

---

## Accessibility

- Always include `alt` text for images
- Use semantic elements (`<h2>`, `<blockquote>`, `<figure>`, `<figcaption>`)
- Maintain heading hierarchy (h1 for title slide, h2 for other slides, h3 for subheadings)
- Ensure sufficient color contrast (defined in theme)
- Keep text readable (minimum effective size after scaling)

---

## Checklist Before Committing a Slide

- [ ] File named correctly: `NN-descriptive-name.html`
- [ ] Contains only `<section class="slide">...</section>`
- [ ] No `<head>`, `<style>`, or `<script>` tags
- [ ] Animation classes applied (`.reveal`)
- [ ] Heading hierarchy makes sense
- [ ] Images have `alt` attributes
- [ ] Text is concise (one idea per slide)
- [ ] Build still works: `./build.sh`

---

## Related Skills

- **[html-slides](../html-slides/SKILL.md)** — Project setup and workflow
- **[html-slides-style](../html-slides-style/SKILL.md)** — CSS classes, animations, theming
- **[html-slides-image](../html-slides-image/SKILL.md)** — AI-generated images
