# Model Card: <model_name>

Status: exploratory / reviewed / retired

Created: YYYY-MM-DD
Reviewed By:
Code Commit:
Dataset Fingerprint:
Environment:

## Intended Use

Describe the research question this model addresses.

This model is research context only. It must not automate account activity,
collect private records, or generate action instructions.

## Training Data

- Source ledgers:
- Feature tables:
- Date range:
- Number of rows:
- Bettors included:
- Platforms included:
- Buckets included:

## Exclusions

List excluded rows and counts by reason:

- `settlement_quality=false`:
- `external_anecdote`:
- accepted historical exception:
- missing exact line:
- missing result:
- other:

## Target

Define the prediction or scoring target.

## Features

List feature families used. Include whether friend gut metadata was used and how it was separated from model-derived features.

## Validation

- Split method:
- Time-aware validation details:
- Baseline comparison:
- Calibration result:
- Non-win coverage:
- App-level row counts:

## Results

Summarize out-of-sample behavior without converting it into live-event or
financial instructions.

## Interpretation

Include permutation importance. Add SHAP only after useful out-of-sample behavior exists.

## Limitations

Document missing losses, stale sources, small samples, app-specific line gaps, correlated slips, and survivorship bias risks.

## Approval

- Reviewed:
- Approved for human discussion:
- Approved artifact paths, if any:
