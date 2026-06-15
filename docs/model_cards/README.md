# Model Cards

Model cards are required before any model output is treated as more than exploratory context.

Use `template.md` for each reviewed model or baseline. Do not create a model card for scratch experiments that remain under `exploratory/`.

Required before a card can be marked reviewed:

- `scripts/check_model_readiness.py` passes.
- Training rows are `settlement_quality=true`.
- External anecdotes, accepted historical exceptions, and `settlement_quality=false` rows are excluded by default.
- Time-aware validation is documented.
- Calibration and baseline comparisons are documented.
- Package versions and dataset fingerprint are recorded.
- No raw screenshots, private app data, credentials, bet reference IDs, balances, account IDs, or precise location data are included.

Model cards are for research governance. They are not live-event or financial
instructions.
