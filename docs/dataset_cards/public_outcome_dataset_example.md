# Dataset Card: Public Outcome Sample

Status: public export example

Created: 2026-06-15

## Intended Use

Demonstrate the repository's public-source outcome data contract, manifest
discipline, hash tracking, and export boundary for a portfolio review.

This dataset card is research context only. It must not be used for live-event
recommendations, financial decisions, account actions, or private-data
training.

## Composition

- Public manifest: `data/research/public_outcome_dataset_manifest.json`
- Public sample: `data/research/public_outcome_dataset_sample.csv`
- Synthetic demo rows: `data/demo/synthetic_private_style_rows.csv`
- Full generated public-outcome CSV: local/ignored, not included in public
  export.

The public export includes only the tracked public sample and synthetic demo
rows. It excludes private ledgers, `data/slates/`, raw screenshots, private
transaction records, account facts, model binaries, caches, and generated bulk
datasets.

## Source And Access Status

The tracked public outcome manifest records the source verification status for
the public sample. Exported synthetic rows are labeled
`source_verified=synthetic` and are not real account or transaction data.

## Collection Process

The private repo builds public outcome data through source-verified, audited
research scripts. Public export tooling copies only the tracked public manifest
and sample, then generates synthetic demo rows and a public sample manifest.

## Recommended Use

- Review schema and manifest discipline.
- Review source-boundary and privacy controls.
- Run public validators and smoke checks.
- Use as a small example for documentation and code review.

## Non-Recommended Use

- Do not treat the sample as a complete training dataset.
- Do not infer private account records or transaction outcomes from it.
- Do not use it for live-event decisions.
- Do not use it to claim private-data model readiness or model promotion.

## Maintenance

Refresh the public sample only after source-verified public outcome data are
rebuilt and the public export validator passes. Public release remains blocked
until the license and publication gates are explicitly approved.
