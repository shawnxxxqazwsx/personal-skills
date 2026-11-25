---
name: immersive-audio
description: Analyze and plan spatial-audio formats, conventions, recording, rendering, evaluation, delivery, standards, papers, and datasets across channel-, object-, scene-, and sound-field-based systems. Use when a request has a spatial or immersive audio component; do not trigger for generic audio work or general paper searches.
---

# Immersive Audio

Keep paradigms separate, make signal conventions explicit, and support changeable claims with current primary sources.

## Scope boundary

- **In scope:** spatial-audio paradigms (channel/object/scene/WFS), acoustics and psychoacoustics, binaural and loudspeaker rendering DSP, studio room and monitoring calibration, spatial codecs/metadata/delivery standards, and spatial-audio papers and corpora.
- **Out of scope:** generic non-spatial audio development, live DAW UI/session control, plug-in rescanning or reloading, and host project bounce/export execution.

## Route the request

Read this file first, then read each relevant reference file completely. Select only the files needed for the request.

| Need | Read |
|---|---|
| Books, surveys, foundational papers, reading path | [references/papers.md](references/papers.md) |
| Codec, bitstream, ADM, S-ADM, IAB, IAMF, Atmos, Auro, DTS, 360RA, SOFA, MPEG-I standards | [references/specs.md](references/specs.md) |
| Open recordings, array comparisons, IRs, SELD corpora | [references/corpora.md](references/corpora.md) |
| Psychoacoustics, binaural concepts, WFS, evaluation, arrays, DirAC/COMPASS, MPEG-I 6DoF | [references/research.md](references/research.md) |
| Practical format choices, MIMO IR matrix validation, production/DSP tools, game engines | [references/reference.md](references/reference.md) |
| Loudspeaker geometry (BS.775 / BS.2051 / 7.1.4 / 9.1.6 / 22.2), Atmos room norms, SPL/LFE/bass-management calibration, ESS & room EQ | [references/calibration-and-monitoring.md](references/calibration-and-monitoring.md) |
| SOFA (AES69), ITD/ILD & HRIR interpolation, MagLS/BiMagLS, DFEQ/HpTF/BRIR, speaker panning & HOA decoders (VBAP..AllRAD2, Max-rE) | [references/binaural-and-rendering-dsp.md](references/binaural-and-rendering-dsp.md) |
| ADM XML hierarchy, S-ADM (AES3/ST 2110-41), IAB, AOM IAMF, Atmos ADM BWF gates, Binaural Render Mode vs. Apple Spatial Audio, BS.1770 loudness | [references/delivery-and-authoring.md](references/delivery-and-authoring.md) |

## Live verification (`web-research`) and knowledge-base updates

1. **When to invoke `web-research`:** Trigger whenever local `references/` cannot answer the task or may be stale—updated standards/editions (ITU-R, ISO/IEC, SMPTE, ETSI, AES, AOM IAMF), changed vendor renderer or platform delivery gates (Dolby, Apple, MPEG-H/I, game engines), new DSP toolkits/SOFA conventions, or recent papers/datasets. Prefer primary sources (normative standard pages, official manuals, DOIs, official repositories); treat vendor white papers as workflow evidence rather than neutral comparisons, and label paywalled material honestly.
2. **Closed-loop write-back (after task verification succeeds):** Merge verified, reusable incremental facts into the matching `references/<topic>.md` in place (replacing outdated rows rather than appending chronological logs), attaching the primary-source URL and verification date (`YYYY-MM-DD`). Create a new kebab-case `references/<topic>.md` only for a genuinely uncovered major domain, updating the **Route the request** table in the same edit.
3. **Anti-pollution guardrails:** Persist only reusable facts/workflows (standard revisions, delivery limits, verified tool capabilities, DOIs). Never write one-off session logs, local user paths, unverified guesses, unread paywalled claims, or cross-file duplicates (cross-link instead). Keep mutable software/platform limits separate from stable mathematics and acoustics.

## Resolve the paradigm first

| Paradigm | Representation | Typical examples |
|---|---|---|
| Channel-based | Signals are bound to a reproduction layout | 5.1, 7.1.4, classic Auro layers |
| Object-based | Audio essence plus rendering metadata such as position, extent, and gain | Dolby Atmos objects, 360RA objects |
| Scene-based | A sound field represented with spherical-harmonic coefficients | Ambisonics / HOA |
| Sound-field synthesis | A physical field is reconstructed with distributed secondary sources | WFS research systems |

Do not treat an object as necessarily dry, HOA as a fixed speaker layout, or WFS as another Atmos brand.

## Core invariants and cautions

1. A complete three-dimensional Ambisonic order `N` has `(N + 1)^2` channels; FOA has four.
2. Modern AmbiX interchange means ACN channel order plus SN3D normalization. Confirm ordering, normalization, coordinate system, handedness, and channel count before combining files from different tools.
3. Convert FuMa, N3D, SID, or other conventions explicitly. Never silently mix them.
4. AllRAD is a strong loudspeaker-decoder baseline and MagLS is a strong binaural baseline, not a universal mandate. Choose a decoder from the array geometry, order, listening region, HRTF set, latency, and evaluation goal.
5. Dolby Atmos supports channel beds and audio objects. Objects do not have a discrete LFE channel; low-frequency energy in an object can still reach subwoofers through bass management. Distinguish the production master from consumer delivery.
6. Home Atmos may use E-AC-3 with JOC, but TrueHD and AC-4 are also relevant delivery paths. State the platform and deliverable.
7. MPEG-H 3D Audio carries channels, objects, and HOA. MPEG-I Immersive Audio adds a six-degree-of-freedom interactive scene and renderer model; ordinary MPEG-H music is not thereby 6DoF.
8. ADM, S-ADM, IAB, and IAMF occupy different authoring, streaming, and distribution layers. Name the exact recommendation or standard and the carriage context.
9. In multichannel calibration, LFE `+10 dB` is an **in-band** acoustic gain (verified via RTA/FFT or matched narrowband noise), not a `+10 dBC` broadband SPL delta on full-band pink noise; in ITU-R BS.1770 loudness, LFE is excluded (`0`) and height channels (`|φ| ≥ 30°`) use unity weight (`1.00`), not the `+1.5 dB` (`1.41`) horizontal side-surround weight.
10. Spaced channel arrays (such as ESMA-3D) are not freely rotatable like an Ambisonic scene, and a generic HRTF render is not equivalent to a personalized BRIR.

## Work method

1. State the playback target: loudspeakers, headphones, engine, broadcast chain, cinema, or 3DoF/6DoF XR.
2. Name the representation and convention: channel/object/scene/WFS, then AmbiX, ADM profile, Atmos master, or other concrete format.
3. Trace capture or authoring, exchange, rendering, and delivery as separate stages.
4. Identify the fragile assumptions: coordinate system, normalization, array order, decoder, HRTF/BRIR, head tracking, seat, room, or codec profile.
5. Recommend a reproducible pipeline or research anchor and include verification steps.
6. Cite current primary sources for mutable facts and foundational papers for theory.

## Evaluation discipline

- Specify the perceptual attribute instead of saying only "more immersive": localization, externalization, source width, listener envelopment, coloration, timbre, or quality impairment.
- Specify loudspeaker versus headphone playback, listener position, head tracking, room, and population.
- Use BS.1116 for subtle impairments and BS.1534/MUSHRA for intermediate-quality comparisons only when the test design fits their assumptions. See [references/research.md](references/research.md).
- Do not rank microphone arrays from a single metric. Combine controlled listening with relevant objective descriptors.
- Before sample-level objective comparison of original, reference, and candidate renders, freeze representation, channel convention, decoder/renderer, HRTF, routing, and output format so residuals reflect only the variable under test.

## Response shape

Lead with the format and feasibility conclusion. Then give the recommended chain, convention checks, risks, and cited evidence. Match the user's language; define specialist abbreviations on first use.
