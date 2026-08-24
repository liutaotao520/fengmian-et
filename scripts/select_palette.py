#!/usr/bin/env python3
"""Select a restrained Eitan cover palette deterministically or randomly."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import secrets
from typing import Any


PALETTES: tuple[dict[str, Any], ...] = (
    {
        "name": "ice-lavender",
        "background": "#F0F0FF",
        "glass_tint": "#DCDFF0",
        "accent": "#635BDB",
        "haze": "#BFC5DC",
        "description": "cool lavender-white reference-like glassmorphism",
    },
    {
        "name": "glacier-blue",
        "background": "#EEF7FF",
        "glass_tint": "#D8E9FF",
        "accent": "#1677FF",
        "haze": "#B8CADF",
        "description": "clear technical ice-blue glassmorphism",
    },
    {
        "name": "mint-glass",
        "background": "#EFFAF7",
        "glass_tint": "#D7F1EA",
        "accent": "#0F9D8A",
        "haze": "#B7D5CE",
        "description": "fresh low-saturation mint glassmorphism",
    },
    {
        "name": "mist-silver",
        "background": "#F4F5F7",
        "glass_tint": "#E1E4EA",
        "accent": "#667085",
        "haze": "#C5C9D2",
        "description": "neutral enterprise silver glassmorphism",
    },
    {
        "name": "violet-gray",
        "background": "#F5F2FA",
        "glass_tint": "#E7DFFF",
        "accent": "#7657D9",
        "haze": "#C8C1D8",
        "description": "slightly stronger violet reference variant",
    },
    {
        "name": "aqua-frost",
        "background": "#F0FBFF",
        "glass_tint": "#D8F1F6",
        "accent": "#148EA8",
        "haze": "#B9DDE5",
        "description": "clear aqua frost with a calm technical accent",
    },
    {
        "name": "sage-ice",
        "background": "#F2F9F5",
        "glass_tint": "#DCEEE4",
        "accent": "#3F8A68",
        "haze": "#C0D9C9",
        "description": "quiet sage-green glass with a natural software feel",
    },
    {
        "name": "rose-mist",
        "background": "#FFF4F7",
        "glass_tint": "#F6E1E8",
        "accent": "#BE5F7A",
        "haze": "#E4C6D0",
        "description": "soft rose mist with a restrained editorial accent",
    },
    {
        "name": "periwinkle-air",
        "background": "#F3F5FF",
        "glass_tint": "#E0E6FA",
        "accent": "#536FC7",
        "haze": "#C6D0E8",
        "description": "airy periwinkle with a precise blue-violet accent",
    },
    {
        "name": "lemon-ice",
        "background": "#FFFCF1",
        "glass_tint": "#F3EFCF",
        "accent": "#9A852D",
        "haze": "#E3D9B2",
        "description": "pale lemon ice with a muted mineral-gold accent",
    },
    {
        "name": "teal-porcelain",
        "background": "#F0FAFA",
        "glass_tint": "#D8EEEE",
        "accent": "#2F8F91",
        "haze": "#B8D6D7",
        "description": "clean teal porcelain with a balanced cyan accent",
    },
    {
        "name": "eucalyptus-cloud",
        "background": "#F3F9F1",
        "glass_tint": "#DCEBD7",
        "accent": "#5C8D63",
        "haze": "#C1D7BE",
        "description": "soft eucalyptus cloud with a calm green accent",
    },
    {
        "name": "coral-veil",
        "background": "#FFF6F3",
        "glass_tint": "#F5E2DA",
        "accent": "#C46F5B",
        "haze": "#E3C6BD",
        "description": "light coral veil with a restrained warm accent",
    },
    {
        "name": "cornflower-mist",
        "background": "#F1F6FF",
        "glass_tint": "#DCE7F7",
        "accent": "#4C78B8",
        "haze": "#C0D1E5",
        "description": "clear cornflower mist with a practical blue accent",
    },
    {
        "name": "pistachio-haze",
        "background": "#F7FBEF",
        "glass_tint": "#E8F0D0",
        "accent": "#7C963C",
        "haze": "#D4DFB1",
        "description": "pale pistachio haze with a muted olive accent",
    },
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("reference", "random"),
        default="reference",
        help="Use the reference palette or choose a curated palette.",
    )
    parser.add_argument(
        "--palette",
        choices=tuple(str(palette["name"]) for palette in PALETTES),
        help="Select an exact curated palette by name; overrides --mode.",
    )
    parser.add_argument(
        "--seed",
        help="Optional integer or text seed. The selected result is reproducible.",
    )
    return parser.parse_args()


def seeded_rng(seed: str | None) -> tuple[random.Random, str]:
    if seed is None:
        generated = secrets.token_hex(8)
        return random.Random(int(generated, 16)), generated
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return random.Random(int(digest, 16)), seed


def main() -> int:
    args = parse_args()
    rng, resolved_seed = seeded_rng(args.seed)
    if args.palette:
        palette = next(item for item in PALETTES if item["name"] == args.palette)
    else:
        palette = PALETTES[0] if args.mode == "reference" else rng.choice(PALETTES)
    result = {
        "mode": args.mode,
        "selection": "named" if args.palette else args.mode,
        "seed": resolved_seed,
        "palette": palette,
        "gradient_direction": rng.choice(("top-right", "right", "bottom-right")),
        "glow_position": rng.choice(("behind-panels", "upper-right", "center-right")),
        "glass_strength": rng.choice(("subtle", "medium")),
        "title_color": "#1D1D1F",
        "cad_badge_color": "#D9274B",
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
