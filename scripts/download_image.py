#!/usr/bin/env python3
"""
download_image.py - Download images from URLs for presentations

Usage:
    # Basic download
    python download_image.py --url "https://example.com/logo.png" --output assets/logo.png

    # With resize limit
    python download_image.py --url "https://example.com/large.jpg" --output assets/image.jpg --max-size 2048

    # With custom timeout
    python download_image.py --url "https://example.com/slow.png" --output assets/image.png --timeout 60

No external dependencies required (uses Python standard library).
Optional: Install Pillow for --max-size resize support: pip install Pillow
"""

import argparse
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


def download_image(url: str, output_path: str, max_size: int | None, timeout: int) -> None:
    """Download an image from URL with retry logic."""
    # Retry logic
    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            # Create request with user agent to avoid blocks
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; html-slides-plugin/1.0)"}
            )

            with urllib.request.urlopen(req, timeout=timeout) as response:
                # Check content type
                content_type = response.headers.get("Content-Type", "").lower()
                valid_types = ["image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp", "image/svg+xml"]
                if not any(vt in content_type for vt in valid_types):
                    print(f"Warning: Content-Type '{content_type}' may not be an image", file=sys.stderr)

                # Read image data
                image_data = response.read()

            # Resize if needed (requires PIL)
            if max_size:
                image_data = resize_if_needed(image_data, max_size, output_path)

            # Ensure output directory exists
            output = Path(output_path)
            output.parent.mkdir(parents=True, exist_ok=True)

            # Save image
            with open(output, "wb") as f:
                f.write(image_data)

            return

        except urllib.error.HTTPError as e:
            if e.code == 429:
                # Rate limited
                wait_time = retry_delay * (attempt + 1)
                print(f"Rate limited. Waiting {wait_time}s before retry...", file=sys.stderr)
                time.sleep(wait_time)
                continue
            else:
                print(f"Error: HTTP {e.code} when fetching {url}", file=sys.stderr)
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


def resize_if_needed(image_data: bytes, max_size: int, output_path: str) -> bytes:
    """Resize image if larger than max_size. Returns original if PIL unavailable or SVG."""
    # Skip SVG files
    if output_path.lower().endswith(".svg"):
        return image_data

    try:
        from PIL import Image
        import io
    except ImportError:
        print("Note: Pillow not installed, skipping resize. Install with: pip install Pillow", file=sys.stderr)
        return image_data

    try:
        img = Image.open(io.BytesIO(image_data))
        width, height = img.size

        # Check if resize needed
        if width <= max_size and height <= max_size:
            return image_data

        # Calculate new size maintaining aspect ratio
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))

        print(f"Resizing from {width}x{height} to {new_width}x{new_height}", file=sys.stderr)

        # Resize
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Save to bytes
        output_buffer = io.BytesIO()
        # Determine format from extension
        ext = Path(output_path).suffix.lower()
        format_map = {
            ".png": "PNG",
            ".jpg": "JPEG",
            ".jpeg": "JPEG",
            ".gif": "GIF",
            ".webp": "WEBP"
        }
        img_format = format_map.get(ext, "PNG")

        # Handle RGBA for JPEG
        if img_format == "JPEG" and img.mode == "RGBA":
            img = img.convert("RGB")

        img.save(output_buffer, format=img_format, quality=90)
        return output_buffer.getvalue()

    except Exception as e:
        print(f"Warning: Could not resize image: {e}", file=sys.stderr)
        return image_data


def generate_alt_text(url: str) -> str:
    """Generate suggested alt text from URL."""
    # Extract filename from URL
    path = url.split("?")[0].split("#")[0]  # Remove query params
    filename = Path(path).stem

    # Clean up filename
    alt = filename.replace("-", " ").replace("_", " ")
    alt = " ".join(word.capitalize() for word in alt.split())

    if alt:
        return f"Image: {alt}"
    return "Downloaded image"


def main():
    parser = argparse.ArgumentParser(
        description="Download images from URLs for presentations"
    )

    parser.add_argument(
        "--url", "-u",
        required=True,
        help="URL of the image to download"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output file path (e.g., assets/logo.png)"
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=None,
        help="Maximum dimension in pixels. Resize if larger (requires Pillow)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)"
    )

    args = parser.parse_args()

    print(f"Downloading: {args.url}", file=sys.stderr)

    download_image(args.url, args.output, args.max_size, args.timeout)

    # Generate alt text suggestion
    alt_text = generate_alt_text(args.url)

    print(f"\nDownloaded: {args.output}")
    print(f"Suggested alt text: \"{alt_text}\"")


if __name__ == "__main__":
    main()
