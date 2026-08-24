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
    palette = PALETTES[0] if args.mode == "reference" else rng.choice(PALETTES)
    result = {
        "mode": args.mode,
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
