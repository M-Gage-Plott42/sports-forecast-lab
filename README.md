# Sports Forecast Lab

Sports Forecast Lab is a public, research-only demonstration of a
source-audited sports prediction framework. It shows how to keep public data,
model documentation, validation checks, and sport-specific adapters organized
without exposing private records.

It is not a transaction tool. It does not automate account activity, submit
entries, or provide instructions for financial decisions. The package excludes
private ledgers, app/slate records, screenshots, private transaction details,
account/platform details, caches, generated bulk artifacts, model binaries, and
secrets.

## What Is Included

- Public outcome sample data and its source manifest.
- Synthetic demo rows that imitate schema shape without using private records.
- A public sample manifest with hashes and source/access-status notes.
- Public-safe model-card and dataset-card examples.
- Cross-sport framework architecture.
- MLB adapter skeleton docs, fixtures, and fixture-only validator.
- Public export validator, research boundary, security notes, and release
  checklist.

## Quickstart

```bash
python3 scripts/validate_public_repo_export.py --export-root .
python3 scripts/validate_mlb_adapter_skeleton.py
python3 scripts/validate_text_line_endings.py
```

## Boundaries

- Research only.
- No financial guidance.
- No account or app automation.
- No private account interaction.
- No model promotion without a reviewed model card, dataset card, baseline
  comparison, calibration checks, and explicit promotion contract.
- No broad sport modeling until source rows and validation contracts are
  stable.

## Review Path

Start with `docs/public_release_checklist.md`, then inspect
`PUBLIC_EXPORT_MANIFEST.json` and `data/demo/PUBLIC_SAMPLE_MANIFEST.json`.

## License

Apache-2.0.
