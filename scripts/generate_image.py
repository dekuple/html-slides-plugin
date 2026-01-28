#!/usr/bin/env python3
"""
generate_image.py - Generate images using Gemini 3 Pro Image Preview API

Usage:
    # Direct prompt
    python generate_image.py --prompt "minimalist illustration of automation" --output image.png

    # With style signature
    python generate_image.py --style-file .claude-design/image-style.json \
                             --concept "workflow automation" \
                             --output assets/workflow.png

    # Background image
    python generate_image.py --style-file .claude-design/image-style.json \
                             --type background \
                             --output assets/title-bg.png

No external dependencies required (uses Python standard library).
Requires GEMINI_API_KEY environment variable.
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


def get_api_key() -> str:
    """Get Gemini API key from environment."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        print("\nTo generate images, you need a Gemini API key:", file=sys.stderr)
        print("1. Go to https://aistudio.google.com/", file=sys.stderr)
        print("2. Sign in and create an API key", file=sys.stderr)
        print('3. Run: export GEMINI_API_KEY="your-key"', file=sys.stderr)
        sys.exit(1)
    return api_key


def load_style_signature(style_file: str) -> dict:
    """Load image style signature from JSON file."""
    try:
        with open(style_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Style file not found: {style_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in style file: {e}", file=sys.stderr)
        sys.exit(1)


def build_prompt(
    style: dict | None,
    concept: str | None,
    direct_prompt: str | None,
    image_type: str
) -> str:
    """Build the image generation prompt."""

    if direct_prompt:
        return direct_prompt

    if not style:
        print("Error: Either --prompt or --style-file with --concept required", file=sys.stderr)
        sys.exit(1)

    signature = style.get("signature", "")
    negative = style.get("negative_prompt", "")
    colors = style.get("color_palette", {})

    if image_type == "background":
        # Background images are atmospheric, no focal point
        color_desc = ""
        if colors:
            bg = colors.get("background", "")
            primary = colors.get("primary", "")
            if bg and primary:
                color_desc = f"subtle gradient from {bg} to {primary}, "

        prompt = (
            f"Abstract atmospheric background, {signature}, "
            f"{color_desc}"
            "soft texture, no focal point, no objects, no text, "
            "suitable for text overlay, professional presentation quality"
        )
    else:
        # Content images visualize concepts
        if not concept:
            print("Error: --concept required for content images when using --style-file", file=sys.stderr)
            sys.exit(1)

        color_desc = ""
        if colors:
            accent = colors.get("accent", "")
            bg = colors.get("background", "white")
            if accent:
                color_desc = f"using accent color {accent}, "
            color_desc += f"clean {bg} background, "

        prompt = (
            f"{signature}, {concept}, "
            f"{color_desc}"
            "clean composition, professional presentation quality"
        )

    # Add negative prompt if present
    if negative:
        prompt += f". Avoid: {negative}"

    return prompt


def generate_image(prompt: str, api_key: str, size: str = "1024x1024") -> bytes:
    """Generate an image using Gemini 3 Pro Image Preview API."""
    # Parse size (validated but not currently used by this API endpoint)
    try:
        width, height = map(int, size.split("x"))
    except ValueError:
        print(f"Error: Invalid size format '{size}'. Use WIDTHxHEIGHT (e.g., 1024x1024)", file=sys.stderr)
        sys.exit(1)

    # Gemini API endpoint for image generation
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }

    # Retry logic
    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            # Create request with JSON payload
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")

            with urllib.request.urlopen(req, timeout=120) as response:
                response_data = response.read().decode("utf-8")
                result = json.loads(response_data)

            # Extract image from response
            candidates = result.get("candidates", [])
            if not candidates:
                print("Error: No image generated in response", file=sys.stderr)
                sys.exit(1)

            parts = candidates[0].get("content", {}).get("parts", [])
            for part in parts:
                if "inlineData" in part:
                    image_data = part["inlineData"].get("data", "")
                    if image_data:
                        return base64.b64decode(image_data)

            print("Error: No image data found in response", file=sys.stderr)
            sys.exit(1)

        except urllib.error.HTTPError as e:
            if e.code == 429:
                # Rate limited
                wait_time = retry_delay * (attempt + 1)
                print(f"Rate limited. Waiting {wait_time}s before retry...", file=sys.stderr)
                time.sleep(wait_time)
                continue
            else:
                error_msg = e.read().decode("utf-8") if e.fp else str(e)
                try:
                    error_data = json.loads(error_msg)
                    if "error" in error_data:
                        error_msg = error_data["error"].get("message", error_msg)
                except (json.JSONDecodeError, KeyError):
                    pass
                print(f"API error ({e.code}): {error_msg}", file=sys.stderr)
                sys.exit(1)

        except urllib.error.URLError as e:
            if "timed out" in str(e.reason).lower():
                if attempt < max_retries - 1:
                    print(f"Request timed out. Retrying...", file=sys.stderr)
                    time.sleep(retry_delay)
                else:
                    print("Error: Request timed out after all retries", file=sys.stderr)
                    sys.exit(1)
            else:
                print(f"Error: Request failed: {e.reason}", file=sys.stderr)
                sys.exit(1)

        except TimeoutError:
            if attempt < max_retries - 1:
                print(f"Request timed out. Retrying...", file=sys.stderr)
                time.sleep(retry_delay)
            else:
                print("Error: Request timed out after all retries", file=sys.stderr)
                sys.exit(1)

    print("Error: Failed after all retries", file=sys.stderr)
    sys.exit(1)


def generate_alt_text(concept: str | None, image_type: str, style: dict | None) -> str:
    """Generate suggested alt text for the image."""
    if image_type == "background":
        mood = style.get("mood", "atmospheric") if style else "atmospheric"
        return f"Abstract {mood} background pattern"

    if concept:
        return f"Illustration representing {concept}"

    return "AI-generated illustration"


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Gemini 3 Pro Image Preview API"
    )

    # Input options (mutually exclusive groups)
    input_group = parser.add_argument_group("Input options")
    input_group.add_argument(
        "--prompt",
        help="Direct prompt for image generation (ignores style file)"
    )
    input_group.add_argument(
        "--style-file",
        help="Path to image-style.json for consistent styling"
    )
    input_group.add_argument(
        "--concept",
        help="Concept to illustrate (combined with style signature)"
    )

    # Output options
    output_group = parser.add_argument_group("Output options")
    output_group.add_argument(
        "--output", "-o",
        required=True,
        help="Output file path (e.g., assets/workflow.png)"
    )
    output_group.add_argument(
        "--type",
        choices=["content", "background"],
        default="content",
        help="Image type: 'content' (concept illustration) or 'background' (atmospheric)"
    )
    output_group.add_argument(
        "--size",
        default="1024x1024",
        help="Image size (default: 1024x1024). Options: 1024x1024, 1024x768, 768x1024"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.prompt and not args.style_file:
        parser.error("Either --prompt or --style-file (with --concept for content images) is required")

    if args.style_file and args.type == "content" and not args.concept:
        parser.error("--concept is required for content images when using --style-file")

    # Get API key
    api_key = get_api_key()

    # Load style if provided
    style = None
    if args.style_file:
        style = load_style_signature(args.style_file)

    # Build prompt
    prompt = build_prompt(style, args.concept, args.prompt, args.type)

    print(f"Generating image...", file=sys.stderr)
    print(f"Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}", file=sys.stderr)

    # Generate image
    image_data = generate_image(prompt, api_key, args.size)

    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save image
    with open(output_path, "wb") as f:
        f.write(image_data)

    # Generate alt text suggestion
    alt_text = generate_alt_text(args.concept, args.type, style)

    print(f"\nGenerated: {args.output}")
    print(f"Suggested alt text: \"{alt_text}\"")


if __name__ == "__main__":
    main()
