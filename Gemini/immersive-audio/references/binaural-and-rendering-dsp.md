# Binaural Rendering and Spatial Audio DSP

Use this reference for SOFA container engineering, HRTF preprocessing and interpolation, Ambisonic-to-binaural algorithms (MagLS / BiMagLS), headphone compensation and BRIR externalization, and loudspeaker panning/decoding mathematics. Keep stable signal-processing mathematics separate from version-specific software or runtime limits.

## Contents

- SOFA (AES69) container format and conventions
- HRTF decomposition, time-aligned interpolation, and SH truncation
- MagLS and BiMagLS binaural Ambisonics
- Diffuse-field EQ, headphone compensation, and BRIR externalization
- Loudspeaker panning and Ambisonic decoder mathematics

## SOFA (AES69) container format and conventions

**SOFA (Spatially Oriented Format for Acoustics)** is standardized under **AES69** (**AES69-2022 / SOFA 2.1**, built on netCDF-4 / HDF5). A SOFA file is strictly governed by its declared **Convention**, which defines mandatory variables, array dimensions, coordinate systems, and measurement geometry. Verify the current convention registry at [sofaconventions.org](https://www.sofaconventions.org/).

### Core dimensions and metadata to inspect first

- **Array dimensions:** `M` (measurements), `R` (receivers, e.g., 2 ears or `Q` mic capsules), `E` (emitters/sources), `N` (impulse samples, frequency bins, or filter coefficients), `C = 3` (spatial coordinates), `I = 1`.
- **Coordinates:** Check `SourcePosition:Type` and `ListenerPosition:Type` (`spherical` in `[azimuth°, elevation°, radius m]` vs. `cartesian` in `[x, y, z m]`), plus `ListenerView` and `ListenerUp` vectors (which define front and up axes).
- **Separate delay variable:** Inspect `Data.Delay` (size `[I, R]` or `[M, R]`, in samples). Some HRTF datasets store onset delays in `Data.Delay` while keeping `Data.IR` time-aligned; ignoring `Data.Delay` destroys ITD.
- **Sampling rate:** Always check `Data.SamplingRate` and resample `Data.IR` (and scale `Data.Delay`) explicitly when matching an engine sample rate.

### Common SOFA conventions

| Convention | `DataType` | Acoustic scope | Engineering notes |
|---|---|---|---|
| `SimpleFreeFieldHRIR` | `FIR` | Single listener at origin, omnidirectional source moving in free field, 2 ear receivers | Most widely supported convention across research and real-time renderers (`libmysofa`, SPARTA, Steam Audio) |
| `SimpleFreeFieldHRSOS` *(formerly/informally `SimpleFreeFieldSOS`)* | `SOS` | Free-field HRTFs parameterized as cascaded second-order IIR sections (`biquads`) + broadband `Data.Delay` | Low-CPU real-time HRTF rendering; check exact convention string (`SimpleFreeFieldHRSOS` in AES69-2022) |
| `SingleRoomSRIR` *(evolved from `SingleRoomDRIR`)* | `FIR` | Single-room spatial/directional room impulse responses (e.g., spherical microphone array captures) | `SingleRoomSRIR` updates legacy `SingleRoomDRIR` naming; SOFA 2.1 also defines `SingleRoomMIMOSRIR` for multi-emitter/multi-receiver rooms |
| `MultiSpeakerBRIR` | `FIR` | Binaural room impulse responses from multiple fixed loudspeakers (`E` emitters) to one listener (`R=2`) across head orientations (`M`) | Standard container for virtual control-room / headphone monitoring auralization |
| `GeneralFIR` | `FIR` | Unconstrained geometry and orientations for arbitrary FIR acoustic datasets | Useful for custom measurements, but rarely accepted out-of-the-box by strict real-time HRTF engines |

## HRTF decomposition, time-aligned interpolation, and SH truncation

### ITD / ILD separation and minimum-phase + pure-delay modeling

Any causal free-field HRIR $h(\Omega, t)$ at direction $\Omega = (\theta, \phi)$ can be factored into a **minimum-phase** component $h_{\min}(\Omega, t)$ and an **all-pass excess-phase** component $h_{\text{ap}}(\Omega, t)$:

$$H(\Omega, \omega) = H_{\min}(\Omega, \omega) \cdot H_{\text{ap}}(\Omega, \omega) \approx H_{\min}(\Omega, \omega) \cdot e^{-j\omega \tau(\Omega)}$$

- $H_{\min}(\Omega, \omega)$ is uniquely determined from $\ln |H(\Omega, \omega)|$ via the discrete Hilbert transform (real cepstrum) and carries the full magnitude response (ILD and pinna/head/torso spectral cues).
- For free-field HRTFs, the excess phase is closely approximated by a direction-dependent pure propagation delay $\tau(\Omega)$, so the broadband interaural time difference is $\text{ITD}(\Omega) = \tau_R(\Omega) - \tau_L(\Omega)$.
- **Practical benefit:** Separating $H_{\min}$ and $\tau(\Omega)$ simplifies fractional-delay interpolation, prevents comb filtering during crossfades, and enables independent ITD scaling (e.g., matching head radius without altering pinna spectra).

### Time-aligned HRIR interpolation

Directly interpolating raw HRIRs between two measured directions ($\Omega_1, \Omega_2$) sums two impulses arriving at different ITDs, creating severe high-frequency comb notches and broadened localization.

Standard artifact-free workflow:

1. Estimate and remove per-ear propagation delay $\tau(\Omega)$ (via minimum-phase excess delay, leading-edge threshold, cross-correlation, or a spherical-head Woodworth/TOA model).
2. Interpolate the **time-aligned** HRIRs (barycentric weights on a Delaunay/convex-hull triangulation of the measurement grid, or spherical spline / SH interpolation on the aligned set).
3. Interpolate the scalar delays $\tau(\Omega)$ independently and re-apply them via fractional-delay filters (e.g., Lagrange, Thiran all-pass, or Farrow structures) or phase-aligned FFT synthesis.

### Spherical-harmonic (SH) domain HRIR truncation error

Representing an HRTF set in spherical harmonics up to Ambisonic order $N$ acts as a spatial low-pass filter on the sphere. For a head of radius $a \approx 8.75\text{ cm}$, the spatial wave-number product $ka = 2\pi f a / c$ dictates the order required to capture complex HRTF phase oscillations accurately:

$$N_{\text{req}}(f) \approx \lceil k a \rceil = \left\lceil \frac{2\pi f a}{c} \right\rceil$$

- At `1 kHz`, $ka \approx 1.6$ (order `2` suffices).
- At `4 kHz`, $ka \approx 6.4$; at `16 kHz`, $ka \approx 25.6$.
- Truncating unaligned complex HRTFs to low Ambisonic orders (`N = 1..5`) averages rapidly oscillating high-frequency phase across the sphere, causing **severe high-frequency magnitude roll-off**, collapsed ILDs, smoothed pinna notches, and dull/colored timbre.
- **Ear-aligned / phase-removed SH projection:** Removing the geometric propagation phase $e^{-j k a \cos\alpha}$ per ear before projecting onto spherical harmonics dramatically compresses the HRTF's spatial bandwidth, reducing truncation error before any binaural decoder optimization.

## MagLS and BiMagLS binaural Ambisonics

### MagLS (Magnitude Least Squares)

Introduced by Schörkhuber, Zaunschirm, and Höldrich (2018), **MagLS** resolves high-frequency spectral coloration in order-limited Ambisonic binaural decoding by changing the optimization objective across frequency:

- **Below the transition / cutoff frequency $f_c$:** Uses standard complex least-squares SH matching, preserving accurate low-frequency ITDs and interaural phase differences where fine-structure phase cues dominate human lateralization.
- **Above $f_c$:** Exploits the psychoacoustic reduced sensitivity to high-frequency carrier interaural phase (duplex theory; ILD and envelope cues dominate) and solves a **magnitude-only least-squares** problem, freeing target phase while keeping phase progression smooth across frequency (typically via iterative phase updates from low to high bins so group delay stays well-behaved).
- **Cutoff frequency ($f_c$) scaling:** Scales roughly with Ambisonic order $N$ and head radius $a$, around the spatial-aliasing boundary $f_c \approx \frac{N c}{2\pi a}$ (commonly `~1.0–1.5 kHz` for FOA `N=1`, `~2–3 kHz` for 3OA, `~3–4 kHz` for 5OA, tuned with a smooth transition band and optional diffuse-field covariance constraint).
- **Accuracy caveat:** Do **not** summarize MagLS as "discarding HRTF phase." Its formulation relaxes high-frequency complex-phase constraints in the decoder objective while preserving low-frequency complex phase and maintaining coherent filter behavior across frequency.

### BiMagLS (Bilateral Magnitude Least Squares)

**BiMagLS** (Engel, Goodman, and Picinali) combines **Bilateral Ambisonics** (translating the Ambisonic representation to two ear-centered reference points using ear-aligned HRTFs, which aligns interaural propagation phase before order truncation) with **MagLS** magnitude fitting above the remaining order-limited cutoff.

- **Advantage over head-centered MagLS:** At low orders (`N = 1..3`), ear alignment preserves broadband ITD accuracy much more faithfully while MagLS maintains high-frequency ILD and spectral accuracy—yielding lower power-spectral-density error, cleaner ILD, and reduced spatial blur than either standard LS or head-centered MagLS alone.
- **Tradeoff:** Requires ear-aligned HRTF preprocessing (explicit head-radius / ear-offset modeling) and slightly more design care when combining with arbitrary dynamic rotation, though rotation remains straightforward in the SH domain prior to the bilateral decoding matrix.

## Diffuse-field EQ, headphone compensation, and BRIR externalization

### Diffuse-field equalization (DFEQ)

The **Common Transfer Function (CTF)** is the solid-angle-weighted RMS power average of an HRTF set over the full sphere; dividing each HRTF by the CTF yields the **Directional Transfer Function (DTF)**.

- **Why DFEQ matters:** Raw HRTFs embed ear-canal and pinna diffuse-field resonances. Applying raw HRTFs over headphones already tuned toward a diffuse-field or Harman curve causes severe double-filtering (typically an excess `2–4 kHz` peak and harshness).
- In Ambisonic binaural decoders, applying **diffuse-field covariance / order-truncation equalization** restores neutral diffuse-field spectral balance when truncated orders attenuate high frequencies, though EQ alone cannot recover lost spatial resolution.

### Headphone transfer function (HpTF) compensation

- Headphone coupling to individual pinnae and ear canals varies strongly across models and across re-seatings of the same headphone (`3–10 kHz` notches can shift by hundreds of Hz with a few millimeters of movement).
- **Safe inverse-filter rules:**
  - Average measurements across multiple headphone seatings (or dummy-head placements) before inverting.
  - Use **regularized minimum-phase inversion** (e.g., Tikhonov / Kirkeby regularization with tighter regularization above `~6–8 kHz`, capping boost on narrow notches to avoid sharp ringing and fragile seating dependence).
  - Match the target reference curve consistently: an **HRTF + HpTF** chain must cancel the headphone's own coloration against the same reference field (free-field vs. diffuse-field) used by the HRTF dataset.

### Externalization and hybrid BRIR rendering

Anechoic HRTFs frequently trigger **in-head localization (IHL)**. Externalization depends on multiple interacting cues: dynamic head tracking (3DoF/6DoF), spectral naturalness (HRTF + HpTF match), early room reflections, visual/contextual congruence, and listener adaptation.

To achieve convincing externalization in real time without prohibitive convolution cost, production engines use a **hybrid early/late BRIR architecture**:

1. **Direct sound + discrete early reflections (`0` to `~30–80 ms`):** Rendered with full directional HRTFs (via image-source / ray tracing or truncated directional BRIR taps) and updated dynamically with head rotation/translation. Early reflections provide primary room-size, distance (`DRR`), and externalization cues.
2. **Diffuse late reverberation tail (after mixing time `t_m ≈ 50–100 ms`):** Rendered with a low-cost isotropic binaural tail (partitioned stereo/FOA/HOA BRIR convolution or a binaural FDN) whose **interaural coherence (IC)** follows the physical diffuse-field curve ($\text{IC}(f) \approx \text{sinc}(2\pi f d_{\text{ear}} / c)$, transitioning from correlated at very low frequencies to decorrelated above `~500–700 Hz`).
3. **Transition hygiene:** Match energy decay curve (EDC), spectral tilt, and level seamlessly across `t_m` so no audible "gap" or timbre jump occurs between early reflections and late tail.

## Loudspeaker panning and Ambisonic decoder mathematics

### Panning and decoder comparison

| Method | Mathematical basis | Best geometry / use | Strengths | Limitations / failure modes |
|---|---|---|---|---|
| **VBAP** (Pulkki) | Active 2D pair or 3D convex-hull triplet: $\mathbf{g} = \mathbf{L}^{-1}\mathbf{p}$, power-normalized $\|\mathbf{g}\|_2 = 1$ | Discrete objects/beds on irregular 2D/3D rigs with central listening zone | Maximum localization sharpness; zero bleed outside active pair/triplet; simple | Apparent source width varies between speaker vertex (1 speaker) and triangle centroid (3 speakers); fails across large angular holes without virtual speakers |
| **MDAP** (Pulkki) | Superposes VBAP gains across multiple spread virtual directions around the target | Objects requiring controlled extent / uniform source width | Stabilizes apparent source width across speaker gaps | Requires tuning spread count/angle to avoid coloration |
| **DBAP** (Lossius) | Inverse-distance gain law $g_i \propto (d_i^2 + r_s^2)^{-a/2}$, normalized to constant power | Non-convex, open, asymmetric, or walk-around installations with no sweet spot | Geometry-agnostic; no triangulation or listener-center assumption | Broader, less razor-sharp phantom imaging at a single sweet spot |
| **SAD** (Sampling) | $D = \frac{1}{L} \mathbf{Y}^T$ (or quadrature-weighted transpose) | Regular / spherical $t$-design arrays only | Trivial closed form; exact on uniform spherical designs | Severe energy imbalance and localization bias on irregular or hemispheric studio layouts |
| **MMAD** (Mode-Matching) | Moore-Penrose pseudo-inverse $D = \mathbf{Y}^\dagger = \mathbf{Y}^T(\mathbf{Y}\mathbf{Y}^T)^{-1}$ (+ regularization) | Well-conditioned spherical/circular layouts with $L \ge (N+1)^2$ | Exact low-frequency SH reconstruction inside sweet spot | Ill-conditioned on irregular/partial-sphere layouts; extreme positive/negative speaker gains and poor headroom |
| **EPAD** (Energy-Preserving) | SVD of speaker SH matrix $\mathbf{Y} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^T \Rightarrow D = \mathbf{V}\mathbf{U}^T$ | Moderately irregular full-sphere layouts | Guarantees uniform total energy across all source directions | Localization still pulls toward denser speaker clusters |
| **AllRAD** (Zotter & Frank) | Two-stage: decode HOA to dense virtual regular $t$-design, then map virtual speakers to real layout via VBAP (plus imaginary speakers closing holes) | **Strong baseline for irregular & hemispheric studio layouts** (5.1.4, 7.1.4, 9.1.6) | Smooth panning, stable energy, handles missing bottom hemisphere cleanly via imaginary speaker discard/redistribution | On small, strongly asymmetric rigs (dense front, sparse rear), linear superposition can introduce ~2–3 dB rear loudness dips |
| **AllRAD2** (Zotter & Frank) | Energy-domain composition: sums *squared* virtual Ambisonic and VBAP panning functions, then derives equivalent linear decoder from square root | Small, strongly asymmetric irregular studio layouts | Achieves **panning-invariant loudness** even when front/rear speaker density differs sharply | Slightly more involved design step than classic AllRAD |

### Velocity/energy vectors, Max-$r_E$ weighting, and dual-band decoding

Ambisonic loudspeaker decoding balances two psychoacoustic regimes (Gerzon's Makita/velocity and energy vectors):

- **Basic (unweighted) decoding:** Maximizes velocity vector $\|\vec{r}_V\| = 1$. Best for **low frequencies** where wavelength exceeds head size and physical wave-front reconstruction governs ITD localization.
- **Max-$r_E$ weighting:** Multiplies each spherical-harmonic order $n \in [0, N]$ by order-dependent weights $a_n$ (3D approximation: $a_n \approx P_n\!\left(\cos\frac{137.9^\circ}{N + 1.51}\right)$, where $P_n$ is the Legendre polynomial). Maximizes energy vector $\|\vec{r}_E\|$, suppresses opposite-side out-of-phase speaker sidelobes, widens the usable sweet spot, and stabilizes high-frequency ILD localization.
- **In-phase weighting:** Forces all loudspeaker gains strictly non-negative (`≥ 0`), avoiding out-of-phase cancellation for wide audiences or reverberant venues, at the expense of noticeably wider source width.
- **Dual-band decoding (Basic + Max-$r_E$):**
  - Splits the Ambisonic bus with a phase-matched crossover (typically `LR4` 24 dB/oct or linear-phase FIR) around $f_c \approx 400–800\text{ Hz}$ for FOA (scaling upward with order $N$ and inversely with desired listening radius).
  - Applies **Basic** decoding below $f_c$ and **Max-$r_E$** decoding above $f_c$.
  - **Energy-matching gain compensation:** Max-$r_E$ weighting reduces total energy relative to Basic decoding by a known order-dependent factor; apply the exact broadband gain compensation ($\sqrt{\sum (2n+1) / \sum (2n+1) a_n^2}$ for 3D diffuse energy matching, or plane-wave energy matching per decoder convention) to prevent a tonal shelf step across $f_c$.

For open-source and research spatial DSP toolkits (`IEM Plug-in Suite`, `SPARTA`/`SAF`, `libmysofa`, `ear`/`libear`, `HOAlib`, `AmbiX`/`libambix`, `pyfar`, `sofar`), see [reference.md](reference.md).
