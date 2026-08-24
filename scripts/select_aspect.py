#!/usr/bin/env python3
"""Select a supported cover aspect ratio and its nominal 2K dimensions."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import secrets
from typing import Any


ASPECTS: tuple[dict[str, Any], ...] = (
    {
        "aspect_ratio": "16:9",
        "width": 2560,
        "height": 1440,
        "orientation": "landscape",
        "composition": "left-title-right-content",
    },
    {
        "aspect_ratio": "9:16",
        "width": 1440,
        "height": 2560,
        "orientation": "portrait",
        "composition": "top-title-bottom-content",
    },
    {
        "aspect_ratio": "4:3",
        "width": 2048,
        "height": 1536,
        "orientation": "landscape",
        "composition": "left-title-right-content-tight",
    },
    {
        "aspect_ratio": "3:4",
        "width": 1536,
        "height": 2048,
        "orientation": "portrait",
        "composition": "top-title-bottom-content",
    },
    {
        "aspect_ratio": "1:1",
        "width": 2048,
        "height": 2048,
        "orientation": "square",
        "composition": "balanced-two-column-or-stacked",
    },
)

SUPPORTED_RATIOS = tuple(item["aspect_ratio"] for item in ASPECTS)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("manual", "random"),
        default="manual",
        help="Use --ratio or choose one of the supported ratios randomly.",
    )
    parser.add_argument(
        "--ratio",
        choices=SUPPORTED_RATIOS,
        default="16:9",
        help="Requested ratio when --mode manual is used.",
    )
    parser.add_argument(
        "--seed",
        help="Optional text seed for reproducible random selection.",
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
    if args.mode == "random":
        rng, resolved_seed = seeded_rng(args.seed)
        selected = rng.choice(ASPECTS)
    else:
        resolved_seed = args.seed or "manual"
        selected = next(item for item in ASPECTS if item["aspect_ratio"] == args.ratio)

    result = {
        "mode": args.mode,
        "seed": resolved_seed,
        **selected,
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
