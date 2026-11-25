# Legacy Strict CSV Validators (`v1` Compatibility)

Read-only standard-library validators retained in `scripts/` so historical
receipts (`MBT`, `Shelford`, `ngTubeEQ`, `SPL PQ 1540/1544`, `Neumann W492`)
remain reproducible without retroactive schema migration. New EQ fits follow the
streamlined `fit-receipt.json` contract in
[training-contract.md](training-contract.md).

## Scope & Boundaries

- `validate_inference_fit.py` enforces the closed `pigora-inference-validation-v1`
  manifest/CSV schema (`0.2 dB` inclusive at `<= 48 kHz`, optional
  `sample-rate-engineering-0.5` above `48 kHz` bound to a passing `48 kHz`
  decision, explicit `at-or-above-declared-nyquist` rows, and re-hashing of all
  bound files before emitting pass).
- Passing status proves **strict numeric CSV verification only**. It cannot
  adjudicate `fallback-0.5` at `48 kHz`, objective smoothness, compiled C++
  audio agreement, runtime safety, deployment, or product selectability, and it
  never upgrades `public_fit_state`.

## Commands

```bash
# Legacy inference manifest verification (externally recorded SHA-256 required)
python3 scripts/validate_inference_fit.py \
  --manifest-sha256 <lowercase-sha256-of-reviewed-manifest> \
  /absolute/path/to/inference-validation-manifest.json

# Legacy public-fit & withheld-point CSV checks
python3 scripts/validate_public_fit.py --help
python3 scripts/validate_withheld_points.py --help
```

## Regression Tests

Run after any edit to the legacy validators:

```bash
python3 scripts/test_validate_inference_fit.py
python3 scripts/test_withheld_empty_scope.py
```
