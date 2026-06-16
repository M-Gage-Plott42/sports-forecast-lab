# Repository Guidelines

## Project Structure & Module Organization

This repository is a public, research-only sports forecasting framework demo.
Top-level policy and status files (`README.md`, `CONTRIBUTING.md`,
`RESEARCH_BOUNDARY.md`, `SECURITY.md`, `STATUS_PUBLIC.md`) define the public
export boundary. `docs/` contains architecture notes, release checklists, model
cards, dataset cards, and sport-adapter documentation. `data/research/` and
`data/demo/` contain public-safe sample data and manifests; `data/schemas/`
contains JSON schema definitions. `scripts/` contains validation utilities, and
`scripts/fixtures/mlb_adapter/` holds fixture-only MLB adapter examples.

## Build, Test, and Development Commands

There is no package build step. Use the validators as the development contract:

```bash
python3 scripts/validate_public_repo_export.py --export-root .
python3 scripts/validate_mlb_adapter_skeleton.py
python3 scripts/validate_text_line_endings.py
```

`validate_public_repo_export.py` checks required files, public-safety flags,
banned private/generated paths, secrets, and text encodings. The MLB validator
checks the fixture registry, schedule, and boxscore shapes without network or
model execution. The line-ending validator ensures tracked text files use LF.

## Coding Style & Naming Conventions

Python scripts use standard-library dependencies only, `from __future__ import
annotations`, type hints, `Path` for filesystem work, and small validation
functions that collect errors instead of failing on the first issue. Keep
indentation at 4 spaces. Store JSON and CSV fixtures with descriptive,
lowercase, underscore-separated names such as `public_boxscore_fixture.json`.
Markdown should be direct, policy-aware, and wrapped to readable line lengths.

## Testing Guidelines

Add or update validators when changing data contracts, manifests, fixture
schemas, or public-export policy. New fixture files should be covered by a
script under `scripts/` and referenced from the relevant docs. Before opening a
pull request, run all three validator commands above from the repository root.

## Commit & Pull Request Guidelines

Recent history uses short imperative subjects, for example `Refresh public
export validator metadata`. Keep commits focused on one contract, fixture, or
documentation change. Pull requests should describe the public-safe scope,
list validators run, and call out any manifest, schema, model-card, or
dataset-card changes.

## Security & Public Boundary

Never add private ledgers, app/slate records, screenshots, account details,
transaction details, model binaries, generated bulk artifacts, caches, or
secrets. Preserve `source_access_status`, source URLs, timestamps, and
research/no-bet flags on public data rows.
