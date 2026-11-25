---
name: imagegen
description: >-
  Generate or edit standalone raster bitmap assets (.png, .jpg, .webp) such as
  photographic visuals, illustrations, concept art, game textures/sprites,
  product renders, and transparent-background cutouts via the native
  GenerateImage tool. Use only when the user explicitly asks to create a new
  bitmap image or transform/restyle an image with references. Do not use for
  icons, logo systems, geometric graphics, UI wireframes/mockups, or web
  components achievable in HTML/CSS/SVG/Canvas; do not use for quantitative
  charts, plots, infographics, slides, or tables; never generate unrequested AI
  images to impersonate real client products or storefront photography.
---

# Image Generation

Generate or edit standalone raster bitmap assets (`.png` / `.jpg` / `.webp`) for photography-style visuals, editorial or story illustrations, concept art, product renders, game sprites/textures, and transparent-background cutouts.

## Scope and boundaries

- **Use when** the user explicitly asks to generate a new bitmap image, derive style/composition variants from reference images, or edit/restyle an existing image by reference.
- **Do not use when:**
  - The visual can be authored cleanly in HTML/CSS/SVG/Canvas (icons, vector logo systems, geometric shapes, UI mockups, wireframes, web components, or edits to existing native vector/code assets).
  - The request is a quantitative chart, plot, table, slide deck, or structured infographic diagram.
  - The user did not explicitly request AI image generation — never fabricate AI photos to impersonate a client's real product, team, or storefront.

## Execution modes

1. **Native `GenerateImage` tool (default, cross-host):**
   - Use the host's native `GenerateImage` tool (discover schema with `GetDynamicTools` and invoke via `CallDynamicTool` when exposed as a dynamic tool). Does not require `OPENAI_API_KEY`.
   - In Cursor, `GenerateImage` automatically routes through the local `cursor-image` service (`127.0.0.1:3431`, launchd `com.<user>.cursor-image`), mapping model id `grok-imagine-image-2.0` to a signed-in Magpie drawer (xAI `grok/grok-imagine-image` when signed in, else Settings `imageGen`, then `codex/gpt-image-2`). Never route image generation to a chat model id.
2. **OpenAI Images API / CLI fallback (explicit request only):**
   - Use only when the user explicitly asks for an OpenAI Images API/CLI path (e.g., filesystem-path masks or API-only flags) and confirms `OPENAI_API_KEY` usage.
   - If native `GenerateImage` fails, inform the user the CLI/API fallback exists and requires `OPENAI_API_KEY`; proceed only after explicit confirmation. Do not invent a one-off SDK runner or treat `batch` as permission to switch to CLI (`scripts/image_gen.py` is not bundled here).

## Parameters, editing, and save policy

- **Arguments:** pass `description`, optional basename-only `filename` (`hero.png`, never a directory path), `aspect_ratio` (`1:1`, `4:3`, `3:4`, `16:9`, `9:16`), and `reference_image_paths`.
- **Transparency & display:** request a genuinely transparent background in `description` and preserve generated alpha. Do not repeat generated images as Markdown when the client already displays them.
- **Generate vs. edit:** no inputs or style/composition-only references → **generate**; modifying an existing image while preserving parts → **edit** (pass the source in `reference_image_paths` and state the exact changed region and invariants in `description`, as `GenerateImage` does not expose masks or `input_fidelity`). For multiple assets/variants, call `GenerateImage` once per requested asset.
- **Save path:** copy the selected output to the user's named path or into the project workspace for project-bound assets; leave preview-only results as tool output. Never overwrite an existing file unless explicitly asked — create a sibling versioned filename instead.

## Workflow

1. Confirm the user explicitly asked for a raster bitmap asset and gather prompt intent, verbatim text, constraints, aspect ratio, and reference paths.
2. Shape the prompt with [references/prompting.md](references/prompting.md).
3. Call native `GenerateImage` with the structured `description` and arguments.
4. Inspect subject, style, composition, text accuracy, and invariants; iterate with one targeted change per pass.
5. Copy project-bound assets into the workspace and report the final path.

## Shared prompt schema

```text
Use case: <taxonomy slug>
Asset type: <where the asset will be used>
Primary request: <user's main prompt>
Input images: <Image 1: role; Image 2: role> (optional)
Scene/backdrop: <environment>
Subject: <main subject>
Style/medium: <photo/illustration/3D/etc>
Composition/framing: <wide/close/top-down; placement>
Lighting/mood: <lighting + mood>
Color palette: <palette notes>
Materials/textures: <surface details>
Text (verbatim): "<exact text>"
Constraints: <must keep/must avoid>
Avoid: <negative constraints>
```

Copy/paste recipes: [references/sample-prompts.md](references/sample-prompts.md).
