---
name: fengmian-et
description: Create or revise Eitan software covers in 16:9, 9:16, 4:3, 3:4, or 1:1 with adaptive Apple-style or frosted cards, optional identity icons, and controlled random palettes.
---

# 封面 ET Skill

Use this skill for Eitan software, plugin, CAD, SketchUp, measurement, automation, quotation, or related workflow video covers. It defines a reusable visual system, not fixed copy: take the headline, subtitle, product evidence, card labels, and identities from the current user request. Earlier cover text is style precedent only and must not be carried into a new cover unless the user asks for it.

Before producing a cover, read [references/cover-spec.md](references/cover-spec.md). It contains the current layout geometry, adaptive card choices, palette tokens, and prompt guardrails.

## Core Visual System

- Support these output ratios and nominal 2K canvas sizes: `16:9` -> `2560x1440`, `9:16` -> `1440x2560`, `4:3` -> `2048x1536`, `3:4` -> `1536x2048`, and `1:1` -> `2048x2048`.
- Honor a user-supplied ratio. If the user asks for a random ratio or gives no ratio, run `scripts/select_aspect.py --mode random`, then record the selected ratio, dimensions, seed, orientation, and recommended composition. Do not change the ratio during a palette-only revision.
- Adapt the editorial composition to orientation: use left-title/right-content for `16:9` and `4:3`, top-title/bottom-content for `9:16` and `3:4`, and choose a balanced two-column or stacked composition for `1:1`. Keep all text and cards inside safe margins.
- Set the title as one or two flat, heavy, modern Chinese sans-serif lines. It may use the established restrained editorial color contrast: brand/key word in blue, a near-black anchor word, a cool secondary color, and a muted warm accent where appropriate. Adapt the mapping to the user's actual wording; do not force every color into every title.
- Keep title lettering flat. Do not add 3D extrusion, bevels, chrome, inflated forms, heavy outlines, or dramatic shadows unless the user specifically asks.
- Add a subtitle only when the brief supplies one or it clearly improves the hierarchy. Never invent marketing copy that changes the user's product claim.
- Use premium frosted-glass material throughout: pale translucent acrylic frames, thin light rims, subtle blurred bleed-through, delicate contact shadows, and clean bright UI faces. Cards must feel light rather than opaque or bulky.
- Treat the identity rail as optional. Add product/software icons only when the user supplies them or explicitly requests them. When present, place icon-plus-label pairs in an orderly lower-left rail, preserving supplied/order-of-workflow order; if the rail becomes too wide, wrap cleanly to a restrained second row. Do not invent icons merely to fill empty space.
- Keep product icons, titles, and visual evidence authentic to the requested software. Do not invent logos, integrations, or capabilities.

## Adaptive Right-Side Layout

Choose the layout from the actual content instead of forcing a fixed grid or card count. Optimize for thumbnail scanability, truthful grouping, and balanced visual weight against the left title rail.

- Use a `1x2` layout for two broad workflows or screens, a `1x3` row for three short comparable steps, and a `2x2` grid for four compact independent features when equal tiles improve scanning. These are options, not mandatory templates.
- Use a single wide card for one supplied primary story, or a hierarchical composition when one item needs emphasis and the others are supporting details.
- For more than four items, group related items first and choose the smallest readable arrangement. If the content is uneven, prefer a balanced asymmetric or hierarchical layout over fictional symmetry.
- For one supplied primary story, use one larger right-side card rather than creating a fictional second product. For three items, use a clear hierarchy such as one wider primary card and two supporting cards only when it makes the supplied content easier to scan.
- Maintain consistent gutters and card edges, and keep the visual weight balanced against the left title zone. Do not use the retired three-panel staggered/overlapping layout unless the user explicitly asks to return to it.
- Make each card explain a real feature with appropriate visual evidence: models and dimensions for modeling/measurement, drawings and recognition for CAD, tables and exports for quotation, or equivalent evidence supplied by the user. Keep microcopy sparse and legible.

## Card Style Modes

- Use `apple-ui` when the user asks for Apple UI, Apple-like polish, or a premium system-panel look: one light translucent panel per card, restrained 8-12px corner radius, a fine hairline border, shallow diffuse shadow, precise spacing, compact status pills, and quiet separators. Keep the panel bright and light; do not add an Apple logo or unrelated Apple branding.
- Use `frosted-acrylic` when the user emphasizes glass, refraction, or a supplied frosted reference: palette-tinted acrylic, subtle blur/refraction, pale rims, and a quiet lower haze.
- Combine the two when useful: Apple-like information hierarchy inside a frosted-acrylic surface. Do not nest decorative cards inside cards; internal UI evidence may use flat sections, tabs, diff highlights, lists, and status rows.

## Controlled Background Randomization

- Preserve random color variants as a core part of the skill. When the user requests a random or new background color, run `scripts/select_palette.py --mode random` and use the returned background, glass tint, accent, haze, glow direction, and glass strength in the prompt.
- When the user names a curated palette, keep that exact palette instead of randomizing. The available names are documented in `references/cover-spec.md`; resolve one with `scripts/select_palette.py --palette <name>` when a structured palette record is needed. `--mode reference` remains the original `ice-lavender` palette, while `--mode random` now chooses across all 15 curated palettes.
- A palette randomization changes the background atmosphere, glass tint, restrained accents, and haze only. It must not silently change the requested layout, product content, title copy, hierarchy, or icon order.
- For a color-only revision, avoid choosing the immediately preceding palette. Re-run the selector with a new seed if it repeats, then note the selected palette name and seed in the working notes and final handoff.
- Keep palettes pale and low-saturation. The curated `rose-mist`, `lemon-ice`, and `coral-veil` options are controlled soft-warm exceptions; do not generalize them into saturated red, orange, beige, or brown styling. Do not introduce dark cyberpunk styling, neon, or general red accents unless the user explicitly requests a different palette family.

## Generation And Delivery

1. Treat attached artwork as visual reference only. Do not copy its text, people, logos, UI, platform counters, watermarks, or unrelated imagery.
2. Inspect the current cover and identify what the user wants preserved. For a content change, replace prior copy and cards with the new brief; for a palette-only change, preserve the composition and content.
3. Select or randomize the ratio first, then select the orientation-aware composition, adaptive card layout, card style, and palette using the rules above.
4. For a newly generated raster, use the `image2-generate` skill and its bundled Image2 script. Follow that skill's credential and output rules; never expose or substitute its credentials.
5. In the generation prompt, explicitly state: exact user-supplied text, flat title treatment, the selected orientation-aware title/content composition, the chosen layout and card style mode, the chosen palette, optional icon rail placement only when icons are requested, and the real evidence required inside each card. State that there must be no garbled text, copied reference wording, people, watermarks, platform controls, or unrelated brands.
6. Preserve the original Image2 result. Request the selected dimensions with Image2 when supported; if Image2 returns a smaller proportional result, export a separately named PNG at the selected dimensions using high-quality resampling. Never overwrite the source artwork for a color-only variant.
7. Verify the final file exists, matches the selected dimensions and ratio, and render it for visual inspection. Confirm title readability, orientation-appropriate title/content zones, optional icon rail spacing, chosen card layout, non-overlap, text safe margins, card material/style, and the requested palette change before delivery.

The bundled `scripts/update_cover.py` targets a retired cover template and is not part of the active adaptive-layout workflow. Do not use it for new covers or layout revisions.

## Supporting References

- Read [references/cover-spec.md](references/cover-spec.md) for layout geometry, adaptive composition rules, card style modes, palette tokens, and QA guardrails.
- Read [README.md](README.md) only when the user asks about installing, updating, publishing, or open-sourcing this skill.
