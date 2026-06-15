# Public Repo Export Spec

Last updated: 2026-06-15.

Purpose: define an allowlist-only public export for a resume-facing sports
prediction research framework. Do not sanitize this private repository in
place. Do not publish private ledger rows, private app/slate data, screenshots,
private transaction records, account/platform details, friend/user identifiers,
secrets, caches, generated bulk, or local model artifacts.

Public repository target: `sports-forecast-lab`.

Approved license: Apache-2.0.

Publication path: local public-repo rehearsal first; no public GitHub push until
the exported repo is reviewed.

## Public Export Goals

- Present a reusable sports prediction research framework.
- Include public-only real samples and synthetic private-style demo rows.
- Show reproducible source-audited data flow, validators, model/dataset cards,
  and no-promotion governance.
- Provide a public-safe README, public-safe status, quickstart, and smoke tests.
- Keep the private operational repo, private ledger, app evidence, and ignored
  generated artifacts out of the public package.

## Non-Goals

- No live recommendation workflow.
- No financial calculator.
- No app automation.
- No private account/platform interaction.
- No private-data model training.
- No raw screenshots.
- No public release of private transaction amounts, platform settlement prose,
  private transaction IDs, user/friend identifiers, or private account state.

## Allowlist Classes

The first exporter may include only these classes:

- Public-safe generated files created by the exporter:
  `README.md`, `STATUS_PUBLIC.md`, `RESEARCH_BOUNDARY.md`, `SECURITY.md`,
  `CONTRIBUTING.md`, `LICENSE`,
  `data/research/public_outcome_dataset_manifest.json`,
  `data/research/public_outcome_dataset_sample.csv`,
  `data/schemas/public_research_schema.json`,
  `data/demo/PUBLIC_SAMPLE_MANIFEST.json`, and
  `PUBLIC_EXPORT_MANIFEST.json`.
- Reusable policy/spec docs:
  `docs/cross_sport_framework_architecture.md`,
  `docs/public_release_checklist.md`, and
  `docs/public_repo_export_spec.md`.
- Public model/dataset documentation templates:
  `docs/model_cards/README.md`, `docs/model_cards/template.md`,
  `docs/model_cards/public_outcome_baseline_example.md`,
  `docs/dataset_cards/README.md`, and
  `docs/dataset_cards/public_outcome_dataset_example.md`.
- Fixture-only sport adapter scaffolding:
  `docs/sport_adapters/mlb_adapter_skeleton.md`,
  `data/research/mlb_source_registry_template.csv`,
  `scripts/fixtures/mlb_adapter/`, and
  `scripts/validate_mlb_adapter_skeleton.py`.
- Public schema and public sample evidence generated from reviewed source
  material with private/internal columns removed.
- Reusable validators and small helper scripts that are public-safe after
  validator scan.
- Synthetic demo rows generated specifically for the public export.

## Denylist Classes

The exporter and validator must fail on:

- `data/ledgers/`, `data/slates/`, `data/raw/`, `reports/slates/`,
  `reports/gpt_context/current/`, `reports/gpt_context/archive/`.
- `models/`, `mlruns/`, `reports/ml_runs/`, `reports/models/`,
  `reports/smokes/`, `reports/experiments/`, and generated bulk datasets.
- `syncthing/`, `exploratory/`, `.git/`, virtual environments, caches,
  `__pycache__`, and local temp/build directories.
- Raw screenshots/images, archives, databases, pickle/joblib/cloudpickle,
  PyTorch/ONNX/model binaries, and unrecognized binary suffixes.
- Secrets, API keys, platform credentials, paid-data credentials, tokens,
  private account state, precise location data, or local filesystem paths.
- Private transaction IDs, exact private dollar/amount rows, app-platform
  settlement details, friend/user identifiers, and private-leg result phrasing.
  Generic private-app policy terms in exported docs may warn for manual review;
  they must not include concrete private records or dollar rows.

## Public README / Status Requirements

The exporter must generate a public-safe README/status instead of copying root
`README.md` or `STATUS.md` blindly. The public surfaces should state:

- research-only and no-bet-instruction;
- source-audited public data and synthetic demo data only;
- no app automation and no private account interaction;
- quickstart commands that run only public-safe validators/smokes;
- limitations, known non-promotions, and data coverage;
- license placeholder or explicit operator decision before publication.

## Manifest Requirements

`PUBLIC_EXPORT_MANIFEST.json` must include:

- `mode=public_repo_export`;
- `public_repository_name=sports-forecast-lab`;
- `license=Apache-2.0`;
- creation timestamp;
- source repository commit SHA;
- allowlist policy version;
- generated public-safe surfaces;
- copied file list with SHA-256;
- synthetic file list with SHA-256;
- excluded classes;
- validation command, result, warning/error counts, and warning disposition;
- `research_only=yes`;
- `no_bet_instruction=yes`;
- `private_data_included=no`;
- `data_slates_included=no`;
- `raw_screenshots_included=no`;
- `generated_bulk_included=no`;
- `model_binaries_included=no`;
- `root_status_md_included=no`;
- `public_safe_status_included=yes`;
- `secrets_included=no`.

## Minimal Tooling Contract

The initial implementation should add:

- `scripts/create_public_repo_export.py`
  - requires `--output-dir`;
  - copies only the allowlist;
  - writes public-safe README/status/manifest;
  - supports `--dry-run`;
  - never writes into the private repo root by default.
- `scripts/validate_public_repo_export.py`
  - requires `--export-root`;
  - validates manifest, required public surfaces, path denylist, suffix denylist,
    secret patterns, private transaction/dollar/app-settlement patterns, and local
    path leakage;
  - exits nonzero on any error.

Implementation status: the exporter and validator are implemented. The
validator exits nonzero for concrete private/generated material. The exporter
now avoids copying private operational policy docs into the public package and
uses generated public-facing boundary text instead.

## Public Proof Package Next Step

Opened under NE policy on 2026-06-15: public proof/package prep is implemented
for the private repo package step. The package is reviewable as a portfolio
artifact and remains public-source only.

The package now includes:

- Public release checklist: reviewer steps, command sequence, expected
  validator output, warning review, license decision gate, secret-scan gate,
  and no-private-data signoff.
- Public README polish: what the framework does, why it is useful, quickstart,
  public-only data boundary, synthetic-demo boundary, limitations, and no
  financial-guidance/app-automation boundary.
- `STATUS_PUBLIC.md` polish: current public dataset/sample state, no-promotion
  status, research-only scope, and reproducible smoke commands.
- Public sample manifest: source-public rows, synthetic private-style rows,
  hashes, generated timestamp, source-access status fields, and excluded
  private classes.
- Model-card example: intended use, prohibited use, data coverage, baseline
  comparison, calibration, limitations, and no-promotion status.
- Dataset-card example: motivation, composition, collection/source process,
  access status, maintenance, exclusions, and recommended/non-recommended use.
- Security/license notes: `SECURITY.md`, dependency/security posture notes,
  OpenSSF Scorecard-oriented checklist, and Apache-2.0 license file.
- MLB adapter skeleton: official-source basis, source registry template,
  canonical game/team/player/stat shape, public box-score/stat ingestion design,
  source timestamp/access-status contract, and fixture-only smoke validator.

Acceptance criteria for that patch:

1. `python3 scripts/create_public_repo_export.py --output-dir <DIR>` succeeds.
2. `python3 scripts/validate_public_repo_export.py --export-root <DIR>` has no
   errors. Warnings must be reviewed and either resolved or recorded as generic
   policy-language warnings.
3. `PUBLIC_EXPORT_MANIFEST.json` records `private_data_included=no`,
   `root_status_md_included=no`, `research_only=yes`, and
   `no_bet_instruction=yes`.
4. The export contains no private ledger rows, `data/slates/`, raw screenshots,
   local paths, private transaction records, dollar rows, user/friend identifiers,
   model binaries, caches, or generated bulk datasets.
5. The docs clearly say no live recommendations, no financial calculations, no
   private account facts, no private-data training, no account interaction, and
   no model promotion.
6. `python3 scripts/validate_mlb_adapter_skeleton.py` succeeds without network,
   account, financial-calculation, live-recommendation, or model-training
   behavior.

Latest reviewed smoke on 2026-06-15:

- public export creator: pass;
- public export validator: pass;
- MLB adapter skeleton validator: pass;
- file count: `28`;
- errors: `0`;
- warnings: `0`;
- publication status: local public-repo rehearsal approved first; public GitHub
  push still requires final review.

## Publication Gate

Before any public repo creation or push:

1. Run the exporter into a disposable output directory.
2. Run `python3 scripts/validate_public_repo_export.py --export-root <DIR>`.
3. Review `PUBLIC_EXPORT_MANIFEST.json`.
4. Confirm Apache-2.0 is present as `LICENSE`.
5. Run a secret scan and rely on GitHub push protection where available.
6. Confirm the public README/status do not reference private app records or local
   paths.
