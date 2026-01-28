---
name: html-slides-style
description: "Theme, CSS architecture, animations, and print styles for HTML presentations. Use when creating templates, changing visual design, fixing print layout, or generating style previews."
---

# HTML Slides — Style & Theming

This skill covers the CSS architecture, animations, print styles, and JavaScript controller that power the presentation.

## Quick Reference

| Task | Section |
|------|---------|
| Create template files | [Template Structure](#template-structure) |
| Change colors/fonts | [CSS Custom Properties](#css-custom-properties) |
| Add/modify animations | [Animation Definitions](#animation-definitions) |
| Fix print issues | [Print Styles](#print-styles) |
| Generate style previews | [Style Previews](#generating-style-previews) |
| Choose a style direction | [Style Reference](#style-reference) |

---

## Template Structure

The presentation is split into two template files that wrap the slide content.

### template-header.html

Contains everything from `<!DOCTYPE>` through the opening of the slides container.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Title</title>

    <!-- Fonts -->
    <link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=satoshi@400,500,700&display=swap">

    <style>
        /* ============================================
           CSS CUSTOM PROPERTIES
           Change these to change the whole theme
           ============================================ */
        :root {
            /* Colors */
            --bg-primary: #0a0f1c;
            --bg-secondary: #111827;
            --text-primary: #ffffff;
            --text-secondary: #9ca3af;
            --accent: #00ffcc;
            --accent-glow: rgba(0, 255, 204, 0.3);

            /* Typography */
            --font-display: 'Clash Display', sans-serif;
            --font-body: 'Satoshi', sans-serif;

            /* Spacing */
            --slide-padding: clamp(2rem, 5vw, 4rem);

            /* Animation */
            --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
            --duration-normal: 0.6s;
        }

        /* ============================================
           BASE STYLES
           ============================================ */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
            scroll-snap-type: y mandatory;
        }

        body {
            font-family: var(--font-body);
            font-size: 1.125rem;
            line-height: 1.6;
            background: var(--bg-primary);
            color: var(--text-primary);
            overflow-x: hidden;
        }

        /* ============================================
           SLIDE BASE
           ============================================ */
        .slide {
            min-height: 100vh;
            padding: var(--slide-padding);
            scroll-snap-align: start;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }

        /* ============================================
           TYPOGRAPHY
           ============================================ */
        h1, h2, h3 {
            font-family: var(--font-display);
            font-weight: 600;
            line-height: 1.2;
        }

        h1 {
            font-size: clamp(2.5rem, 8vw, 5rem);
            margin-bottom: 1rem;
        }

        h2 {
            font-size: clamp(1.75rem, 5vw, 3rem);
            margin-bottom: 1.5rem;
        }

        h3 {
            font-size: clamp(1.25rem, 3vw, 1.75rem);
            margin-bottom: 0.75rem;
        }

        p {
            max-width: 65ch;
            margin-bottom: 1rem;
        }

        .subtitle {
            font-size: clamp(1.25rem, 3vw, 1.75rem);
            color: var(--text-secondary);
        }

        .author {
            font-size: 1rem;
            color: var(--text-secondary);
            margin-top: 2rem;
        }

        /* ============================================
           ANIMATION CLASSES
           ============================================ */
        .reveal {
            opacity: 0;
            transform: translateY(30px);
            transition: 
                opacity var(--duration-normal) var(--ease-out-expo),
                transform var(--duration-normal) var(--ease-out-expo);
        }

        .reveal-left {
            opacity: 0;
            transform: translateX(-50px);
            transition: 
                opacity var(--duration-normal) var(--ease-out-expo),
                transform var(--duration-normal) var(--ease-out-expo);
        }

        .reveal-right {
            opacity: 0;
            transform: translateX(50px);
            transition: 
                opacity var(--duration-normal) var(--ease-out-expo),
                transform var(--duration-normal) var(--ease-out-expo);
        }

        .reveal-scale {
            opacity: 0;
            transform: scale(0.9);
            transition: 
                opacity var(--duration-normal) var(--ease-out-expo),
                transform var(--duration-normal) var(--ease-out-expo);
        }

        .reveal-blur {
            opacity: 0;
            filter: blur(10px);
            transition: 
                opacity calc(var(--duration-normal) * 1.2) var(--ease-out-expo),
                filter calc(var(--duration-normal) * 1.2) var(--ease-out-expo);
        }

        /* Trigger animations when slide is visible */
        .slide.visible .reveal,
        .slide.visible .reveal-left,
        .slide.visible .reveal-right,
        .slide.visible .reveal-scale {
            opacity: 1;
            transform: translateY(0) translateX(0) scale(1);
        }

        .slide.visible .reveal-blur {
            opacity: 1;
            filter: blur(0);
        }

        /* Staggered delays for children */
        .reveal:nth-child(1), .reveal-left:nth-child(1), .reveal-right:nth-child(1) { transition-delay: 0.1s; }
        .reveal:nth-child(2), .reveal-left:nth-child(2), .reveal-right:nth-child(2) { transition-delay: 0.2s; }
        .reveal:nth-child(3), .reveal-left:nth-child(3), .reveal-right:nth-child(3) { transition-delay: 0.3s; }
        .reveal:nth-child(4), .reveal-left:nth-child(4), .reveal-right:nth-child(4) { transition-delay: 0.4s; }
        .reveal:nth-child(5), .reveal-left:nth-child(5), .reveal-right:nth-child(5) { transition-delay: 0.5s; }
        .reveal:nth-child(6), .reveal-left:nth-child(6), .reveal-right:nth-child(6) { transition-delay: 0.6s; }

        /* Reduced motion preference */
        @media (prefers-reduced-motion: reduce) {
            .reveal, .reveal-left, .reveal-right, .reveal-scale, .reveal-blur {
                transition: opacity 0.3s ease;
                transform: none;
                filter: none;
            }
        }

        /* ============================================
           SLIDE MODIFIERS
           ============================================ */
        .slide--title {
            text-align: center;
            align-items: center;
        }

        .slide--center {
            text-align: center;
            align-items: center;
        }

        .slide--dark {
            background: var(--bg-secondary);
        }

        .slide--light {
            background: #ffffff;
            color: #1a1a1a;
        }

        .slide--light h1,
        .slide--light h2,
        .slide--light h3 {
            color: #1a1a1a;
        }

        .slide--image {
            background-size: cover;
            background-position: center;
        }

        .slide--image .overlay {
            background: rgba(0, 0, 0, 0.6);
            padding: var(--slide-padding);
            border-radius: 0.5rem;
        }

        .slide--quote {
            align-items: center;
        }

        .slide--closing {
            text-align: center;
            align-items: center;
        }

        /* ============================================
           LAYOUT COMPONENTS
           ============================================ */
        
        /* Columns */
        .columns {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 2rem;
            width: 100%;
            margin-top: 1.5rem;
        }

        .columns--60-40 {
            grid-template-columns: 3fr 2fr;
        }

        .columns--40-60 {
            grid-template-columns: 2fr 3fr;
        }

        .columns--70-30 {
            grid-template-columns: 7fr 3fr;
        }

        .column img {
            max-width: 100%;
            height: auto;
            border-radius: 0.5rem;
        }

        /* Stats */
        .stats {
            display: flex;
            gap: 3rem;
            margin-top: 2rem;
            flex-wrap: wrap;
            justify-content: center;
        }

        .stat {
            text-align: center;
        }

        .stat-number {
            display: block;
            font-family: var(--font-display);
            font-size: clamp(2.5rem, 8vw, 4rem);
            font-weight: 700;
            color: var(--accent);
            line-height: 1;
        }

        .stat-label {
            display: block;
            font-size: 1rem;
            color: var(--text-secondary);
            margin-top: 0.5rem;
        }

        /* Comparison */
        .comparison {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 2rem;
            margin-top: 1.5rem;
        }

        .comparison-item {
            padding: 1.5rem;
            border-radius: 0.5rem;
            background: var(--bg-secondary);
        }

        .comparison-item--negative {
            border-left: 4px solid #ef4444;
        }

        .comparison-item--positive {
            border-left: 4px solid #22c55e;
        }

        .comparison-item h3 {
            margin-bottom: 1rem;
        }

        .comparison-item ul {
            list-style: none;
            padding: 0;
        }

        .comparison-item li {
            padding: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
        }

        .comparison-item li::before {
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }

        .comparison-item--negative li::before {
            background: #ef4444;
        }

        .comparison-item--positive li::before {
            background: #22c55e;
        }

        /* Blockquote */
        blockquote {
            max-width: 50ch;
            text-align: center;
        }

        blockquote p {
            font-size: clamp(1.5rem, 4vw, 2.25rem);
            font-style: italic;
            margin-bottom: 1.5rem;
        }

        blockquote footer {
            font-size: 1rem;
            color: var(--text-secondary);
        }

        blockquote cite {
            font-weight: 600;
            color: var(--text-primary);
            font-style: normal;
        }

        /* Code */
        pre {
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            margin: 1rem 0;
        }

        code {
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.9rem;
        }

        .code--small code {
            font-size: 0.75rem;
        }

        /* Lists */
        ul, ol {
            padding-left: 1.5rem;
        }

        li {
            margin-bottom: 0.75rem;
        }

        .reveal-list li {
            opacity: 0;
            transform: translateY(20px);
            transition: 
                opacity var(--duration-normal) var(--ease-out-expo),
                transform var(--duration-normal) var(--ease-out-expo);
        }

        .slide.visible .reveal-list li:nth-child(1) { opacity: 1; transform: translateY(0); transition-delay: 0.1s; }
        .slide.visible .reveal-list li:nth-child(2) { opacity: 1; transform: translateY(0); transition-delay: 0.2s; }
        .slide.visible .reveal-list li:nth-child(3) { opacity: 1; transform: translateY(0); transition-delay: 0.3s; }
        .slide.visible .reveal-list li:nth-child(4) { opacity: 1; transform: translateY(0); transition-delay: 0.4s; }
        .slide.visible .reveal-list li:nth-child(5) { opacity: 1; transform: translateY(0); transition-delay: 0.5s; }
        .slide.visible .reveal-list li:nth-child(6) { opacity: 1; transform: translateY(0); transition-delay: 0.6s; }

        /* Icon Rows */
        .icon-rows {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            margin-top: 1.5rem;
        }

        .icon-row {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
        }

        .icon-row .icon {
            font-size: 2rem;
            line-height: 1;
        }

        .icon-row h3 {
            margin-bottom: 0.25rem;
        }

        .icon-row p {
            color: var(--text-secondary);
            margin: 0;
        }

        /* Timeline */
        .timeline {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            margin-top: 1.5rem;
            padding-left: 2rem;
            border-left: 2px solid var(--accent);
        }

        .timeline-item {
            position: relative;
        }

        .timeline-marker {
            position: absolute;
            left: -2.5rem;
            font-family: var(--font-display);
            font-weight: 600;
            color: var(--accent);
        }

        .timeline-marker::before {
            content: '';
            position: absolute;
            right: -0.75rem;
            top: 50%;
            transform: translateY(-50%);
            width: 10px;
            height: 10px;
            background: var(--accent);
            border-radius: 50%;
        }

        /* Cards */
        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }

        .card {
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 0.5rem;
            text-align: center;
        }

        .card img {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 1rem;
        }

        .card h3 {
            margin-bottom: 0.25rem;
        }

        .card p {
            color: var(--text-secondary);
            margin: 0;
        }

        /* Figures */
        figure {
            margin: 1.5rem 0;
        }

        figure img {
            max-width: 100%;
            height: auto;
            border-radius: 0.5rem;
        }

        figcaption {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-top: 0.5rem;
            text-align: center;
        }

        /* ============================================
           NAVIGATION (optional)
           ============================================ */
        .nav-dots {
            position: fixed;
            right: 1.5rem;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            z-index: 100;
        }

        .nav-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--text-secondary);
            opacity: 0.3;
            cursor: pointer;
            transition: opacity 0.3s, transform 0.3s;
        }

        .nav-dot:hover {
            opacity: 0.7;
        }

        .nav-dot.active {
            opacity: 1;
            background: var(--accent);
            transform: scale(1.2);
        }

        /* Progress bar */
        .progress-bar {
            position: fixed;
            top: 0;
            left: 0;
            height: 3px;
            background: var(--accent);
            width: 0%;
            z-index: 100;
            transition: width 0.3s ease;
        }

        /* ============================================
           PRINT STYLES
           ============================================ */
        @media print {
            /* Reset scroll snap for print */
            html {
                scroll-snap-type: none;
            }

            body {
                background: white;
                color: black;
            }

            /* Each slide = one page */
            .slide {
                min-height: 100vh;
                height: 100vh;
                page-break-after: always;
                page-break-inside: avoid;
                break-after: page;
                break-inside: avoid;
                
                /* Reset flex centering for print */
                display: flex;
                flex-direction: column;
                justify-content: center;
                
                /* Ensure content fits */
                overflow: hidden;
                padding: 1.5cm;
            }

            /* Last slide shouldn't force blank page */
            .slide:last-child {
                page-break-after: auto;
                break-after: auto;
            }

            /* Make all animations visible immediately */
            .reveal, .reveal-left, .reveal-right, 
            .reveal-scale, .reveal-blur,
            .reveal-list li {
                opacity: 1 !important;
                transform: none !important;
                filter: none !important;
                transition: none !important;
            }

            /* Hide navigation elements */
            .nav-dots,
            .progress-bar {
                display: none !important;
            }

            /* Adjust colors for print */
            .slide--dark,
            .slide--light {
                background: white;
                color: black;
            }

            h1, h2, h3 {
                color: black;
            }

            .text-secondary,
            .subtitle,
            .author {
                color: #666;
            }

            /* Accent color for print */
            .stat-number {
                color: #0066cc;
            }

            /* Ensure images print */
            img {
                max-width: 100%;
                page-break-inside: avoid;
            }

            /* Code blocks */
            pre {
                background: #f5f5f5;
                border: 1px solid #ddd;
            }
        }

        /* Print-specific page setup */
        @page {
            size: 16in 9in; /* Widescreen aspect ratio */
            margin: 0;
        }

        /* ============================================
           RESPONSIVE
           ============================================ */
        @media (max-width: 768px) {
            .columns,
            .comparison {
                grid-template-columns: 1fr;
            }

            .stats {
                flex-direction: column;
                align-items: center;
            }

            .nav-dots {
                display: none;
            }

            .timeline {
                padding-left: 3rem;
            }
        }
    </style>
</head>
<body>
    <!-- Progress bar -->
    <div class="progress-bar"></div>

    <!-- Navigation dots (generated by JS) -->
    <nav class="nav-dots"></nav>

    <!-- Slides begin (inserted by build.sh) -->
```

### template-footer.html

Contains closing elements and JavaScript.

```html
    <!-- Slides end -->

    <script>
        /* ============================================
           SLIDE PRESENTATION CONTROLLER
           Handles navigation, scroll detection, and animations
           ============================================ */
        class SlidePresentation {
            constructor() {
                this.slides = document.querySelectorAll('.slide');
                this.currentSlide = 0;
                this.navDots = document.querySelector('.nav-dots');
                this.progressBar = document.querySelector('.progress-bar');

                this.init();
            }

            init() {
                this.createNavDots();
                this.setupIntersectionObserver();
                this.setupKeyboardNav();
                this.setupTouchNav();
                this.updateProgress();
            }

            /* Create navigation dots */
            createNavDots() {
                this.slides.forEach((_, index) => {
                    const dot = document.createElement('button');
                    dot.classList.add('nav-dot');
                    dot.setAttribute('aria-label', `Go to slide ${index + 1}`);
                    dot.addEventListener('click', () => this.goToSlide(index));
                    this.navDots.appendChild(dot);
                });
                this.updateNavDots();
            }

            /* Intersection Observer for scroll-based activation */
            setupIntersectionObserver() {
                const options = {
                    root: null,
                    rootMargin: '0px',
                    threshold: 0.5
                };

                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('visible');
                            this.currentSlide = Array.from(this.slides).indexOf(entry.target);
                            this.updateNavDots();
                            this.updateProgress();
                        }
                    });
                }, options);

                this.slides.forEach(slide => observer.observe(slide));
            }

            /* Keyboard navigation */
            setupKeyboardNav() {
                document.addEventListener('keydown', (e) => {
                    switch(e.key) {
                        case 'ArrowRight':
                        case 'ArrowDown':
                        case ' ':
                            e.preventDefault();
                            this.nextSlide();
                            break;
                        case 'ArrowLeft':
                        case 'ArrowUp':
                            e.preventDefault();
                            this.prevSlide();
                            break;
                        case 'Home':
                            e.preventDefault();
                            this.goToSlide(0);
                            break;
                        case 'End':
                            e.preventDefault();
                            this.goToSlide(this.slides.length - 1);
                            break;
                    }
                });
            }

            /* Touch/swipe navigation */
            setupTouchNav() {
                let touchStartY = 0;
                let touchEndY = 0;

                document.addEventListener('touchstart', (e) => {
                    touchStartY = e.changedTouches[0].screenY;
                }, { passive: true });

                document.addEventListener('touchend', (e) => {
                    touchEndY = e.changedTouches[0].screenY;
                    const diff = touchStartY - touchEndY;

                    if (Math.abs(diff) > 50) {
                        if (diff > 0) {
                            this.nextSlide();
                        } else {
                            this.prevSlide();
                        }
                    }
                }, { passive: true });
            }

            /* Navigation methods */
            nextSlide() {
                if (this.currentSlide < this.slides.length - 1) {
                    this.goToSlide(this.currentSlide + 1);
                }
            }

            prevSlide() {
                if (this.currentSlide > 0) {
                    this.goToSlide(this.currentSlide - 1);
                }
            }

            goToSlide(index) {
                this.slides[index].scrollIntoView({ behavior: 'smooth' });
            }

            /* Update UI elements */
            updateNavDots() {
                const dots = this.navDots.querySelectorAll('.nav-dot');
                dots.forEach((dot, index) => {
                    dot.classList.toggle('active', index === this.currentSlide);
                });
            }

            updateProgress() {
                const progress = ((this.currentSlide + 1) / this.slides.length) * 100;
                this.progressBar.style.width = `${progress}%`;
            }
        }

        /* Initialize when DOM is ready */
        document.addEventListener('DOMContentLoaded', () => {
            new SlidePresentation();
        });
    </script>
</body>
</html>
```

---

## CSS Custom Properties

All theme values are defined in `:root`. Change these to change the entire look.

```css
:root {
    /* === COLORS === */
    --bg-primary: #0a0f1c;          /* Main background */
    --bg-secondary: #111827;         /* Cards, code blocks */
    --text-primary: #ffffff;         /* Headings, body */
    --text-secondary: #9ca3af;       /* Subtitles, captions */
    --accent: #00ffcc;               /* Highlights, stats, links */
    --accent-glow: rgba(0, 255, 204, 0.3);  /* Glow effects */

    /* === TYPOGRAPHY === */
    --font-display: 'Clash Display', sans-serif;  /* Headings */
    --font-body: 'Satoshi', sans-serif;           /* Body text */

    /* === SPACING === */
    --slide-padding: clamp(2rem, 5vw, 4rem);

    /* === ANIMATION === */
    --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
    --duration-normal: 0.6s;
}
```

### Example Themes

**Light Professional:**
```css
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f8fafc;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --accent: #2563eb;
}
```

**Warm Editorial:**
```css
:root {
    --bg-primary: #faf7f2;
    --bg-secondary: #f5ebe0;
    --text-primary: #292524;
    --text-secondary: #78716c;
    --accent: #b45309;
    --font-display: 'Cormorant Garamond', serif;
    --font-body: 'Source Sans Pro', sans-serif;
}
```

**Neon Cyber:**
```css
:root {
    --bg-primary: #0d0d0d;
    --bg-secondary: #1a1a2e;
    --text-primary: #ffffff;
    --text-secondary: #a0a0a0;
    --accent: #ff00ff;
    --accent-glow: rgba(255, 0, 255, 0.4);
}
```

---

## Animation Definitions

### Available Classes

| Class | Transform | Use For |
|-------|-----------|---------|
| `.reveal` | translateY(30px) → 0 | Default, most content |
| `.reveal-left` | translateX(-50px) → 0 | Left column content |
| `.reveal-right` | translateX(50px) → 0 | Right column content |
| `.reveal-scale` | scale(0.9) → 1 | Images, cards |
| `.reveal-blur` | blur(10px) → 0 | Hero text, dramatic reveals |

### How It Works

1. Elements start with `opacity: 0` and a transform
2. JavaScript adds `.visible` class to the slide when it enters viewport
3. CSS transitions animate to `opacity: 1` and `transform: none`
4. Child elements stagger via `transition-delay`

### Adding Custom Animations

Add to the `<style>` in template-header.html:

```css
/* Rotate in */
.reveal-rotate {
    opacity: 0;
    transform: rotate(-10deg) scale(0.9);
    transition: 
        opacity var(--duration-normal) var(--ease-out-expo),
        transform var(--duration-normal) var(--ease-out-expo);
}

.slide.visible .reveal-rotate {
    opacity: 1;
    transform: rotate(0) scale(1);
}
```

### Easing Options

```css
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);     /* Smooth deceleration */
--ease-out-back: cubic-bezier(0.34, 1.56, 0.64, 1); /* Slight overshoot */
--ease-out-elastic: cubic-bezier(0.5, 1.5, 0.5, 1); /* Bouncy */
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);        /* Symmetric */
```

---

## Print Styles

The `@media print` block ensures proper PDF output.

### Key Print Rules

```css
@media print {
    /* Each slide on its own page */
    .slide {
        min-height: 100vh;
        height: 100vh;
        page-break-after: always;
        break-after: page;
        break-inside: avoid;
    }

    /* Don't break after last slide */
    .slide:last-child {
        page-break-after: auto;
        break-after: auto;
    }

    /* Show all animated content */
    .reveal, .reveal-left, .reveal-right, 
    .reveal-scale, .reveal-blur {
        opacity: 1 !important;
        transform: none !important;
    }

    /* Hide UI */
    .nav-dots, .progress-bar {
        display: none !important;
    }
}

/* Page size for widescreen slides */
@page {
    size: 16in 9in;
    margin: 0;
}
```

### Troubleshooting Print

| Issue | Solution |
|-------|----------|
| Multiple slides per page | Ensure `page-break-after: always` on `.slide` |
| Content cut off | Reduce `--slide-padding` in print media query |
| Blank pages appearing | Check for extra breaks, remove `page-break-after` from last slide |
| Colors not printing | Enable "Background graphics" in print dialog |
| Wrong aspect ratio | Adjust `@page { size: ... }` |

### Testing Print

1. Open presentation in browser
2. Press `Ctrl/Cmd + P`
3. Set destination to "Save as PDF"
4. Check "Background graphics" option
5. Preview each page

---

## Generating Style Previews

For style discovery, create self-contained preview files.

### Preview File Structure

```html
<!-- .claude-design/style-previews/style-a.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Style Preview: Corporate Elegant</title>
    <link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=...">
    <style>
        /* Full theme CSS here - self-contained */
        :root { ... }
        /* Base styles */
        /* One slide only */
    </style>
</head>
<body>
    <section class="slide slide--title visible">
        <h1 class="reveal" style="opacity:1;transform:none;">
            Your Presentation
        </h1>
        <p class="reveal subtitle" style="opacity:1;transform:none;">
            A compelling subtitle goes here
        </p>
    </section>
</body>
</html>
```

**Note:** Add `visible` class and inline `opacity:1;transform:none` so animations appear immediately.

---

## Style Reference

### Mood → Style Mapping

| Mood | Suggested Styles |
|------|------------------|
| Impressed/Confident | Corporate Elegant, Dark Executive, Clean Minimal |
| Excited/Energized | Neon Cyber, Bold Gradients, Kinetic Motion |
| Calm/Focused | Paper & Ink, Soft Muted, Swiss Minimal |
| Inspired/Moved | Cinematic Dark, Warm Editorial, Atmospheric |

### Font Pairings

| Style | Display Font | Body Font | Source |
|-------|--------------|-----------|--------|
| Modern Tech | Clash Display | Satoshi | Fontshare |
| Editorial | Cormorant Garamond | Source Sans Pro | Google |
| Clean Corporate | Inter | Inter | Google |
| Bold Statement | Bebas Neue | Open Sans | Google |
| Warm Friendly | DM Serif Display | DM Sans | Google |
| Minimalist | Space Grotesk | Space Grotesk | Google |

**Font URLs:**

```html
<!-- Fontshare -->
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=satoshi@400,500,700&display=swap">

<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Avoid These Patterns

- ❌ Purple gradients on white (overused)
- ❌ Default blue (#0066ff) as accent
- ❌ System fonts (Arial, Helvetica)
- ❌ Low contrast (light gray on white)
- ❌ Too many colors (stick to 3-4)
- ❌ Inconsistent spacing

---

## Background Effects

### Gradient Mesh

```css
.slide--gradient {
    background:
        radial-gradient(ellipse at 20% 80%, rgba(120, 0, 255, 0.3) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(0, 255, 200, 0.2) 0%, transparent 50%),
        var(--bg-primary);
}
```

### Subtle Grid

```css
.slide--grid {
    background-image:
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 50px 50px;
}
```

### Noise Texture

```css
.slide--noise {
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
    background-blend-mode: overlay;
}
```

---

---

## AI-Generated Background Images

For slides using AI-generated background images (see [html-slides-image/SKILL.md](../html-slides-image/SKILL.md)), use these CSS patterns.

### The `.slide--background-image` Modifier

Add to template-header.html styles:

```css
/* ============================================
   AI-GENERATED BACKGROUND IMAGES
   ============================================ */
.slide--background-image {
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: relative;
}

/* Overlay for text readability */
.slide--background-image::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(
        135deg,
        rgba(0, 0, 0, 0.7) 0%,
        rgba(0, 0, 0, 0.4) 50%,
        rgba(0, 0, 0, 0.6) 100%
    );
    z-index: 1;
}

.slide--background-image > * {
    position: relative;
    z-index: 2;
}

/* Light variant for light backgrounds */
.slide--background-image.slide--light::before {
    background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.85) 0%,
        rgba(255, 255, 255, 0.7) 50%,
        rgba(255, 255, 255, 0.8) 100%
    );
}
```

### Usage in Slides

```html
<section class="slide slide--background-image slide--title"
         style="background-image: url('assets/title-bg.png');">
    <h1 class="reveal">Presentation Title</h1>
    <p class="reveal subtitle">With atmospheric AI-generated background</p>
</section>
```

### Overlay Variations

Adjust the overlay based on content needs:

**Heavier overlay (more text):**
```css
.slide--background-image.slide--text-heavy::before {
    background: rgba(0, 0, 0, 0.75);
}
```

**Gradient from side (content on one side):**
```css
.slide--background-image.slide--gradient-left::before {
    background: linear-gradient(
        90deg,
        rgba(0, 0, 0, 0.8) 0%,
        rgba(0, 0, 0, 0.4) 50%,
        transparent 100%
    );
}
```

**No overlay (image designed for readability):**
```css
.slide--background-image.slide--no-overlay::before {
    display: none;
}
```

### Print Styles for Background Images

Add to the `@media print` section:

```css
@media print {
    /* Background images in print */
    .slide--background-image {
        /* Browsers need explicit permission to print backgrounds */
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }

    /* Simplify overlay for print */
    .slide--background-image::before {
        background: rgba(255, 255, 255, 0.3);
    }

    /* Alternative: hide background in print, keep solid color */
    .slide--background-image.print-no-bg {
        background-image: none !important;
        background-color: var(--bg-primary);
    }

    .slide--background-image.print-no-bg::before {
        display: none;
    }
}
```

### Generated Image Class

For inline AI-generated images (not backgrounds):

```css
/* AI-generated content images */
.generated-image {
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.generated-image img {
    width: 100%;
    height: auto;
    display: block;
}

/* Caption for generated images */
.generated-image figcaption {
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
    font-style: italic;
}

/* ============================================
   CHARTS (SVG)
   ============================================ */
.chart {
    margin: 1.5rem 0;
}

.chart img,
.chart svg {
    width: 100%;
    height: auto;
    max-height: 60vh;
}

.chart figcaption {
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
    text-align: center;
}

/* Print optimization for charts */
@media print {
    .chart img,
    .chart svg {
        max-height: 50vh;
        page-break-inside: avoid;
    }
}

/* ============================================
   WEB/DOWNLOADED IMAGES
   ============================================ */
.web-image {
    border-radius: 0.5rem;
}

.web-image img {
    max-width: 100%;
    height: auto;
    display: block;
}

.web-image figcaption {
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 0.5rem;
    font-style: italic;
}

/* Logo grid for partner/client logos */
.logo-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    align-items: center;
    justify-content: center;
    margin: 1.5rem 0;
}

.logo-grid img {
    max-height: 60px;
    max-width: 150px;
    object-fit: contain;
    filter: grayscale(100%);
    opacity: 0.7;
    transition: filter 0.3s, opacity 0.3s;
}

.logo-grid img:hover {
    filter: grayscale(0%);
    opacity: 1;
}

/* Color logos variant */
.logo-grid--color img {
    filter: none;
    opacity: 1;
}

@media print {
    .logo-grid img {
        filter: none;
        opacity: 1;
    }
}
```

---

## Related Skills

- **[html-slides](../html-slides/SKILL.md)** — Project setup and workflow
- **[html-slides-slide](../html-slides-slide/SKILL.md)** — Individual slide content
- **[html-slides-image](../html-slides-image/SKILL.md)** — AI-generated images
