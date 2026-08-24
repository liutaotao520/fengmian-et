# Eitan Adaptive Cover Specification

This reference defines the current reusable Eitan cover direction. It preserves a visual language and decision rules, not the copy from any earlier cover.

## Canvas And Zones

Supported ratios and nominal 2K canvas sizes:

| Ratio | Canvas | Orientation | Default composition |
| --- | --- | --- | --- |
| `16:9` | `2560x1440` | landscape | left title rail + right content |
| `9:16` | `1440x2560` | portrait | top title zone + bottom content |
| `4:3` | `2048x1536` | landscape | left title rail + right content, with tighter gutters |
| `3:4` | `1536x2048` | portrait | top title zone + bottom content |
| `1:1` | `2048x2048` | square | balanced two-column or stacked composition |

Honor a user-supplied ratio. When the user requests a random ratio or leaves it unspecified, run `scripts/select_aspect.py --mode random` and record the returned ratio, dimensions, seed, orientation, and composition. A palette-only revision keeps the existing ratio.

- Landscape (`16:9`, `4:3`): use an airy left title zone and a dedicated right content zone. A fine vertical divider may separate them when it improves scanning.
- Portrait (`9:16`, `3:4`): move the title to the upper zone and stack content below it. Use a fine horizontal divider only when it helps; never squeeze a landscape rail into the narrow canvas.
- Square (`1:1`): choose two columns or a stacked title/content arrangement based on the number and width of cards. Keep the title large enough for thumbnail recognition.
- Bottom treatment: use a broad translucent haze or quiet refractive sweep that supports the glass effect. It is not a solid footer, landscape scene, or decorative illustration.

## Title And Identity Rail

- Headline: use the exact user-supplied title, split into one or two lines for balanced reading. Size it for immediate thumbnail recognition while leaving the lower-left rail clear.
- Typography: flat, bold, contemporary Chinese sans-serif. No 3D extrusion, bevel, outline, chrome, or inflated lettering by default.
- Default color logic: use a cobalt/blue brand or lead word, a near-black anchor, a cool green/teal support word, and a muted ochre-gold emphasis word when the title naturally supports multiple terms. Use fewer colors when that better suits the copy.
- Subtitle: only use text supplied by the user or a clearly requested supporting phrase. Keep it quieter than the headline.
- Identity rail: optional. Add app, product, or file-format icons only when the user supplies them or explicitly asks for them. When present, place pairs at the lower left in supplied/order-of-workflow order, using one consistent optical icon size and short labels only when needed. Wrap cleanly to a second row if necessary; never place invented icons inside right-side cards merely to fill space.

## Adaptive Card Selection

| Content shape | Right-side treatment | Rule |
| --- | --- | --- |
| Two broad screens or workflows | `1x2` wide cards | Use one row and two columns when each story needs horizontal breathing room. |
| Three short, comparable features or steps | `1x3` cards | Use one row and three columns only when labels and evidence remain legible at thumbnail size. |
| Four independent, compact features | `2x2` equal cards | Use four aligned cards when equal tiles improve scanning; this is an option, not a fixed requirement. |
| One supplied primary screen or feature | One large primary card | Do not invent a second product just to fill a grid. |
| Three supplied features | Hierarchical three-card layout | Use one wider primary card plus two supporting cards only if the content benefits from hierarchy; otherwise prioritize legibility over symmetry. |

Cards must remain simple rectangular surfaces with aligned edges and stable gutters. Choose the smallest composition that leaves content legible and balanced. Do not nest decorative cards inside cards. The current default is adaptive flat-grid or hierarchical composition, not the older three-window staggered overlap.

## Card Evidence

Show the actual function described by the brief. Examples:

- Modeling/measurement: model geometry, dimension lines, materials, area/length/quantity results, export evidence.
- CAD automation: floor plans, blocks, doors/windows, annotations, recognition, batch controls, or drawing output.
- Quotation: item/material/quantity/unit/price mapping, totals, and requested PDF/Excel export evidence.
- Plugin suites: one card per real plugin if there are four distinct compact modules.

Avoid unsupported claims. Keep UI microcopy sparse and readable; the product label and visual evidence matter more than dense invented interface text.

## Card Style Modes

- `apple-ui`: light translucent system panels, restrained 8-12px radius, fine hairline border, shallow diffuse shadow, precise spacing, compact status pills, and quiet separators. Keep each card as one surface; internal evidence can use flat sections and lists. Do not add an Apple logo or unrelated Apple branding.
- `frosted-acrylic`: palette-tinted acrylic, gentle blur/refraction, pale rims, delicate contact shadows, and a quiet lower haze.
- Hybrid: use Apple-like hierarchy inside frosted acrylic when both are requested. Keep the result light, precise, and free of bulky opaque panels.

## Glass Material

- Frames: milky translucent white or palette-tinted acrylic with thin pale highlight rims.
- Surfaces: gentle background blur/refraction and a subtle depth shadow, while the internal UI remains bright and clear.
- Weight: light and precise. Avoid chunky opaque white panels, heavy drop shadows, dark glazing, or decorative gradients inside every card.
- Background: continuous pale gradient with diffuse glow and restrained lower haze. Never add bokeh/orb decorations.

## Curated Palette Variants

Use `scripts/select_palette.py` to choose one of these variants when randomization is requested. Record the returned palette and seed whenever producing a color variant.

| Name | Background | Glass tint | Accent | Use |
| --- | --- | --- | --- | --- |
| ice-lavender | `#F0F0FF` | `#DCDFF0` | `#635BDB` | Cool lavender-white, closest to the original reference mood. |
| glacier-blue | `#EEF7FF` | `#D8E9FF` | `#1677FF` | Clear technical ice-blue glass. |
| mint-glass | `#EFFAF7` | `#D7F1EA` | `#0F9D8A` | Fresh low-saturation mint glass. |
| mist-silver | `#F4F5F7` | `#E1E4EA` | `#667085` | Neutral cloud-silver enterprise glass. |
| violet-gray | `#F5F2FA` | `#E7DFFF` | `#7657D9` | Soft violet-gray, slightly stronger reference accent. |

Randomization may vary glow direction, haze strength, glass tint, and restrained accent use within the selected palette. It must not alter content, card count, grid choice, icon rail, or the title's reading order. Keep body text and title anchors near `#1D1D1F` unless contrast requires another accessible value. Use red only for an actual CAD identity badge, never as a general visual accent.

## Prompt And QA Guardrails

State the following in every raster-generation prompt:

- exact user-supplied text and required labels;
- flat 2D title with the left-title/right-card composition;
- selected palette tokens and premium frosted acrylic material;
- the selected adaptive composition (`1x2`, `1x3`, `2x2`, or an intentional single/asymmetric/hierarchical arrangement);
- optional identity icons grouped at lower left only when supplied or requested;
- bright, legible software UI faces and real product evidence;
- no copied reference text/imagery, people, watermarks, platform counters, play buttons, unrelated logos, or garbled prominent text.

Before delivery, verify the selected 2K dimensions and ratio, then visually inspect for title overflow, orientation-appropriate divider alignment, optional icon collisions, card overlap, unreadable labels, unbalanced whitespace, correct card style, and a palette that is visibly different when the brief requested a color-only variant.
