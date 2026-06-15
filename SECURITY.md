# Security Policy

This public export is research-only and contains no private account data,
secrets, screenshots, private ledgers, app/slate records, model binaries, or
generated bulk artifacts by design.

## Supported Surface

Report issues with public validators, documentation, schemas, sample manifests,
and fixture-only adapter code.

## Not Supported

Do not submit private account records, screenshots, transaction details,
credentials, API keys, location data, or app-specific evidence. Do not request
account automation, live recommendations, financial guidance, or private-data
training through this public package.

## Maintainer Checklist

- Run `python3 scripts/validate_public_repo_export.py --export-root .`.
- Run `python3 scripts/validate_mlb_adapter_skeleton.py`.
- Run a secret scan before publication.
- Use GitHub push protection and secret scanning where available.
- Keep Apache-2.0 in place before claiming open-source reuse.
