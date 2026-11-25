# Sample prompts (copy/paste)

Shared prompt recipes for the native `GenerateImage` tool (default; routes through the local `cursor-image` Magpie backend in Cursor) and the explicit OpenAI Images API / CLI fallback.

Use these as starting points, not as a default augmentation quota:
- Keep user-provided requirements and follow the specificity policy in [prompting.md](prompting.md).
- Do not invent extra characters, props, or story beats unless implied.
- Labeled lines (`Asset type`, `Input images`, etc.) are prompt scaffolding, not tool flags. Fallback CLI controls (`quality`, `input_fidelity`, masks, output format) live in [prompting.md](prompting.md).

## Generate

### photorealistic-natural
```text
Use case: photorealistic-natural
Primary request: candid photo of an elderly sailor on a small fishing boat adjusting a net
Scene/backdrop: coastal water with soft haze
Subject: weathered skin with wrinkles and sun texture
Style/medium: photorealistic candid photo
Composition/framing: medium close-up, eye-level
Lighting/mood: soft coastal daylight, shallow depth of field, subtle film grain
Materials/textures: real skin texture, worn fabric, salt-worn wood
Constraints: natural color balance; no heavy retouching; no glamorization; no watermark
Avoid: studio polish; staged look
```

### product-mockup
```text
Use case: product-mockup
Primary request: studio product photo of a matte black shampoo bottle with a minimal label
Scene/backdrop: clean studio gradient from light gray to white
Subject: single bottle centered with subtle reflection
Style/medium: commercial product photography
Composition/framing: centered, slight three-quarter angle, generous padding
Lighting/mood: softbox lighting, clean highlights, controlled shadows
Materials/textures: matte plastic, crisp label printing
Constraints: no logos or trademarks; no watermark
```

### illustration-story
```text
Use case: illustration-story
Primary request: 4-panel comic about a pet left alone at home
Scene/backdrop: cozy living room across panels
Subject: pet reacting to the owner leaving, then relaxing, then returning to a composed pose
Style/medium: comic illustration with clear panels
Composition/framing: 4 equal-sized vertical panels, readable actions per panel
Constraints: no text; no logos or trademarks; no watermark
```

### stylized-concept
```text
Use case: stylized-concept
Primary request: cavernous hangar interior with tall support beams and drifting fog
Scene/backdrop: industrial hangar interior, deep scale, light haze
Subject: compact shuttle parked near the center
Style/medium: cinematic concept art, industrial realism
Composition/framing: wide-angle, low-angle
Lighting/mood: volumetric light rays cutting through fog
Constraints: no logos or trademarks; no watermark
```

### ads-marketing
```text
Use case: ads-marketing
Primary request: campaign photo for a streetwear brand called Thread
Subject: group of friends hanging out together in a stylish urban setting
Style/medium: polished youth streetwear campaign photography
Composition/framing: vertical ad layout with natural poses and integrated headline space
Lighting/mood: contemporary, energetic, tasteful
Text (verbatim): "Yours to Create."
Constraints: render the tagline exactly once; clean legible typography; no extra text; no watermarks; no unrelated logos
```

### historical-scene
```text
Use case: historical-scene
Primary request: outdoor crowd scene in Bethel, New York on August 16, 1969
Scene/backdrop: open field with period-appropriate staging
Subject: crowd in period-accurate clothing, authentic environment
Style/medium: photorealistic photo
Composition/framing: wide shot, eye-level
Constraints: period-accurate details; no modern objects; no logos or trademarks; no watermark
```

## Editorial & game bitmap assets

### Editorial hero background
```text
Use case: stylized-concept
Asset type: landing page hero background
Primary request: minimal abstract background with a soft gradient and subtle paper grain
Style/medium: matte painted abstract texture
Composition/framing: wide composition with generous negative space for overlay copy
Lighting/mood: gentle studio glow
Color palette: restrained warm neutral palette
Constraints: no text; no logos; no watermark
```

### Editorial section illustration
```text
Use case: stylized-concept
Asset type: editorial section illustration
Primary request: painterly still life of brass compass, folded topographic map, and botanical specimens
Scene/backdrop: soft warm off-white paper backdrop with subtle grain
Style/medium: gouache editorial illustration; restrained contrast; crisp edges
Composition/framing: centered vignette with generous clean margins
Color palette: muted ochre, slate blue, and deep olive
Constraints: no text; no logos; no watermark
```

### Editorial blog header
```text
Use case: photorealistic-natural
Asset type: editorial header image
Primary request: overhead desk scene with linen notebook, fountain pen, and ceramic coffee cup
Scene/backdrop: warm walnut tabletop
Style/medium: photorealistic photo
Composition/framing: wide crop with clean negative space along one side
Lighting/mood: soft morning window light
Constraints: no text; no logos; no watermark
```

### Game character concept
```text
Use case: stylized-concept
Asset type: game character concept
Primary request: desert scout character with layered travel gear
Subject: weathered coat, leather satchel, practical travel clothing
Style/medium: character concept render; stylized realism
Composition/framing: neutral three-quarter hero pose on a plain backdrop
Constraints: no logos or trademarks; no watermark
```

### Painted game item sprite (transparent cutout)
```text
Use case: game-asset
Asset type: painted game item sprite
Primary request: round bronze shield with worn patina and subtle engraved rim
Scene/backdrop: genuinely transparent background
Style/medium: hand-painted RPG item artwork
Composition/framing: centered object; generous padding; crisp silhouette
Constraints: preserve alpha transparency; no text; no ground shadow; no watermark
```

### Tileable game texture
```text
Use case: game-asset
Asset type: tileable game texture
Primary request: worn sandstone blocks with shallow mortar seams
Scene/backdrop: flat neutral lighting reference only
Style/medium: seamless tileable albedo texture; realistic PBR material look
Constraints: seamless edges on all four sides; no focal landmarks; no text; no watermark
```

## Edit

### text-localization
```text
Use case: text-localization
Input images: Image 1: coffee bag packaging photo
Primary request: replace "Single Origin", "Dark Roast", and "Whole Bean" with "Origen Único", "Tueste Oscuro", and "Grano Entero"
Constraints: change only the printed label text; preserve bag geometry, lighting, typography, spacing, and hierarchy; no extra words; do not alter imagery
```

### identity-preserve
```text
Use case: identity-preserve
Input images: Image 1: person photo; Image 2..N: clothing references
Primary request: replace only the clothing with the provided garments
Constraints: preserve face, body shape, pose, hair, expression, and identity; match lighting and shadows; keep the background unchanged; no accessories or text
```

### precise-object-edit
```text
Use case: precise-object-edit
Input images: Image 1: room photo
Primary request: replace only the white chairs with wooden chairs
Constraints: preserve camera angle, room lighting, floor shadows, and surrounding objects; keep all other aspects unchanged
```

### lighting-weather
```text
Use case: lighting-weather
Input images: Image 1: original photo
Primary request: make it look like a winter evening with gentle snowfall
Constraints: preserve subject identity, geometry, camera angle, and composition; change only lighting, atmosphere, and weather
```

### background-extraction
```text
Use case: background-extraction
Input images: Image 1: studio product photo
Primary request: isolate the ceramic vase onto a genuinely transparent background
Constraints: preserve exact object edges, surface speculars, and glaze color; no white halo; no restyling or extra elements
```

### style-transfer
```text
Use case: style-transfer
Input images: Image 1: style reference
Primary request: apply Image 1's visual style to a rider on a vintage motorcycle against a plain off-white backdrop
Constraints: preserve palette, texture, and brushwork; no extra elements
```

### compositing
```text
Use case: compositing
Input images: Image 1: base scene; Image 2: subject to insert
Primary request: place the subject from Image 2 next to the person in Image 1
Constraints: match lighting, perspective, and scale; keep the base framing unchanged; no extra elements
```

### character consistency workflow
```text
Use case: identity-preserve
Input images: Image 1: previous character anchor illustration
Primary request: continue the story with the same character in a new scene and action
Scene/backdrop: snowy forest after a winter storm
Subject: same young forest hero gently helping a frightened squirrel out of a fallen tree
Style/medium: same children's book watercolor illustration style as Image 1
Constraints: do not redesign the character; preserve facial features, proportions, outfit, color palette, and personality; no text; no watermark
```

### sketch-to-render
```text
Use case: sketch-to-render
Input images: Image 1: drawing
Primary request: turn the drawing into a photorealistic image
Constraints: preserve layout, proportions, and perspective; choose realistic materials and lighting; do not add new elements or text
```
