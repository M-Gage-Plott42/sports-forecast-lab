# Public Release Checklist

Last updated: 2026-06-15.

Purpose: make the allowlist public export reviewable as a portfolio artifact
before any public repository publication. This checklist is repo machinery only.
It does not authorize live-event recommendations, financial calculations,
private-data training, account interaction, broad sport modeling, or model
promotion.

## Release State

Status: public proof/package prep implemented in the private repo. The user has
approved `sports-forecast-lab` as the public repo name, Apache-2.0 as the
license, and a local public-repo rehearsal as the next publication step. Public
GitHub publication remains blocked until the local repo is reviewed.

Current package contents:

- generated public `README.md`;
- generated `STATUS_PUBLIC.md`;
- generated `RESEARCH_BOUNDARY.md`;
- generated `SECURITY.md`;
- generated `CONTRIBUTING.md`;
- generated Apache-2.0 `LICENSE`;
- `PUBLIC_EXPORT_MANIFEST.json`;
- `data/demo/PUBLIC_SAMPLE_MANIFEST.json`;
- generated `data/schemas/public_research_schema.json`;
- synthetic demo rows;
- public-safe outcome manifest/sample generated from reviewed source material;
- public-safe model-card and dataset-card examples;
- cross-sport architecture and MLB adapter skeleton docs;
- public-export and MLB-skeleton validators.

## Review Steps

1. Generate a fresh export into a disposable directory.
   - Command: `python3 scripts/create_public_repo_export.py --output-dir <DIR>`
2. Validate the export.
   - Command: `python3 scripts/validate_public_repo_export.py --export-root <DIR>`
3. Inspect `PUBLIC_EXPORT_MANIFEST.json`.
   - Confirm `private_data_included=no`.
   - Confirm `data_slates_included=no`.
   - Confirm `raw_screenshots_included=no`.
   - Confirm `model_binaries_included=no`.
   - Confirm `root_status_md_included=no`.
   - Confirm `research_only=yes`.
   - Confirm `no_bet_instruction=yes`.
4. Inspect `data/demo/PUBLIC_SAMPLE_MANIFEST.json`.
   - Confirm only public sample data and synthetic demo rows are listed.
   - Confirm every source row has a source/access-status note.
5. Review validator warnings.
   - Any concrete private transaction record, dollar row, local path,
     screenshot, slate, ledger, model binary, cache, or secret finding is a
     release blocker.
   - Target warning count is `0` after excluding private operational policy
     docs and replacing them with generated public boundary text.
6. Confirm the license before publication.
   - Apache-2.0 is the approved license for `sports-forecast-lab`.
7. Run secret scanning before public push.
   - Local validators are necessary but not sufficient; GitHub push protection
     and secret scanning remain operator gates where available.

## Warning Disposition

Known acceptable warning class: generic policy-language references in public
governance docs. These warnings exist because the public package explains
privacy and no-automation boundaries. They are acceptable only when no exact
private records, dollar rows, user/friend identifiers, local paths, raw
screenshots, `data/slates/`, private ledgers, caches, or model binaries are
included.

Latest reviewed smoke on 2026-06-15:

- public export creator: pass;
- public export validator: pass;
- MLB adapter skeleton validator: pass;
- file count: `28`;
- errors: `0`;
- warnings: `0`;
- publication status: local public-repo rehearsal approved; public GitHub push
  pending review.

## Publication Decision Gate

Before creating or updating a public GitHub repository, the user must explicitly
approve:

- final public GitHub visibility;
- whether the current validated local rehearsal is approved for GitHub;
- whether Codex should create and push the public GitHub repository.
