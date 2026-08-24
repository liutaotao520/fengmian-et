#!/usr/bin/env python3
"""Update the current Eitan cover badges and export a verified 16:9 2K PNG."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


DEFAULT_WIDTH = 2560
DEFAULT_HEIGHT = 1440


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--sketchup-label", default="SketchUp")
    parser.add_argument("--cad-label", default="CAD")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    return parser.parse_args()


def find_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        Path(r"C:\Windows\Fonts\segoeuib.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf"),
        Path(r"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    )
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def clean_text_region(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    """Rebuild a quiet background patch from clean rows above and below old text."""
    x1, y1, x2, y2 = box
    width = x2 - x1
    height = y2 - y1
    top = image.crop((x1, max(0, y1 - 6), x2, y1)).resize((width, height), Image.Resampling.BICUBIC)
    bottom = image.crop((x1, y2, x2, min(image.height, y2 + 6))).resize((width, height), Image.Resampling.BICUBIC)
    patch = Image.blend(top, bottom, 0.5)
    image.paste(patch, (x1, y1))


def draw_replaced_label(
    image: Image.Image,
    *,
    clear_box: tuple[int, int, int, int],
    x: int,
    center_y: int,
    label: str,
    font_size: int,
) -> None:
    clean_text_region(image, clear_box)
    draw = ImageDraw.Draw(image)
    font = find_font(font_size)
    draw.text((x, center_y), label, font=font, fill=(24, 24, 28, 255), anchor="lm")


def draw_badge_labels(image: Image.Image, sketchup_label: str, cad_label: str) -> None:
    # Coordinates are normalized to the current 1280x720 cover template.
    scale_x = image.width / 1280.0
    scale_y = image.height / 720.0

    def box(values: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
        return tuple(
            int(round(value * (scale_x if index % 2 == 0 else scale_y)))
            for index, value in enumerate(values)
        )  # type: ignore[return-value]

    badge_font_size = max(18, int(round(18 * scale_x)))
    draw_replaced_label(
        image,
        clear_box=box((112, 477, 207, 514)),
        x=int(round(119 * scale_x)),
        center_y=int(round(496 * scale_y)),
        label=sketchup_label,
        font_size=badge_font_size,
    )
    # Start just after the CAD badge icon so no old vertical stroke survives.
    draw_replaced_label(
        image,
        clear_box=box((291, 477, 409, 514)),
        x=int(round(300 * scale_x)),
        center_y=int(round(496 * scale_y)),
        label=cad_label,
        font_size=badge_font_size,
    )

    # The same software names appear in the two floating window headers.
    header_font_size = max(13, int(round(14 * scale_x)))
    draw_replaced_label(
        image,
        clear_box=box((637, 43, 718, 70)),
        x=int(round(642 * scale_x)),
        center_y=int(round(56 * scale_y)),
        label=sketchup_label,
        font_size=header_font_size,
    )
    draw_replaced_label(
        image,
        clear_box=box((572, 257, 660, 284)),
        x=int(round(578 * scale_x)),
        center_y=int(round(270 * scale_y)),
        label=cad_label,
        font_size=header_font_size,
    )


def main() -> int:
    args = parse_args()
    if args.width <= 0 or args.height <= 0:
        raise SystemExit("width and height must be positive")
    if not args.input.is_file():
        raise SystemExit(f"input image not found: {args.input}")
    expected_ratio = 16 / 9
    source = ImageOps.exif_transpose(Image.open(args.input)).convert("RGBA")
    source_ratio = source.width / source.height
    if abs(source_ratio - expected_ratio) > 0.02:
        raise SystemExit(f"input must be 16:9; got {source.width}x{source.height}")

    draw_badge_labels(source, args.sketchup_label, args.cad_label)
    output = source.resize((args.width, args.height), Image.Resampling.LANCZOS)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.save(args.output, format="PNG", optimize=True)

    if output.size != (args.width, args.height):
        raise SystemExit("output dimensions do not match the requested size")
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
