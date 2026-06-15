# Model Card: Public Outcome Baseline Example

Status: public export example / not promoted

Created: 2026-06-15

## Intended Use

Demonstrate the model-card fields expected for source-audited public sports
prediction research.

This example is research context only. It must not automate account activity,
collect private records, issue live-event recommendations, compute financial
decisions, or generate action instructions.

## Training Data

- Dataset card: `docs/dataset_cards/public_outcome_dataset_example.md`
- Public sample: `data/research/public_outcome_dataset_sample.csv`
- Synthetic demo rows: excluded from real model training; included only to
  demonstrate export schema.
- Private ledger/account data: excluded.
- `data/slates/`: excluded.
- Raw screenshots: excluded.

## Exclusions

- Private ledger rows: excluded.
- Private account facts: excluded.
- Private transaction records: excluded.
- Synthetic demo rows: excluded from model training.
- Generated bulk datasets and model binaries: excluded from public export.

## Target

Public-only outcome target defined by a source-verified public result field.
No account-specific or transaction-specific target is allowed.

## Features

Allowed feature families must be public-source, timestamped, and source-audited.
Every source row must preserve source access status, source tier, and a
machine-parseable timestamp with timezone offset when used for current-source
refreshes.

## Validation

Required before any real public model can move beyond example status:

- chronological split;
- baseline comparison;
- calibration check such as Brier/log-loss/ECE;
- leakage audit;
- source manifest/hash validation;
- reviewed dataset card;
- reviewed model card;
- no-promotion status unless a separate promotion contract is approved.

## Results

This example card records no promoted model results. It exists to show the
public documentation contract.

## Limitations

- The public export sample is not a full training dataset.
- The example card does not validate predictive lift.
- It does not support live recommendations, financial decisions, or private-data
  training.

## Approval

- Reviewed: no
- Approved for human discussion: public documentation example only
- Approved for current workflow use: no
