# Public Release Checklist

Last updated: 2026-06-16.

Purpose: make the allowlist public export reviewable as a portfolio artifact
before any public repository publication. This checklist is repo machinery only.
It does not authorize live-event recommendations, financial calculations,
private-data training, account interaction, broad sport modeling, or model
promotion.

## Release State

Status: public proof/package prep implemented and published. The user approved
`sports-forecast-lab` as the public repo name and Apache-2.0 as the license.
The local public-repo rehearsal was reviewed with validators and local secret
scanners, then published to
`https://github.com/M-Gage-Plott42/sports-forecast-lab` on 2026-06-16.
Post-publication verification passed, and the follow-up 2026-06-16 read-only
public clone/GitHub audit found the current public tree validator-clean and
scanner-clean. GitHub UI secret-scanning/push-protection review is parked as a
manual follow-up because the user deferred that check.

Current package contents:

- generated public `README.md`;
- generated `STATUS_PUBLIC.md`;
- generated `RESEARCH_BOUNDARY.md`;
- generated `SECURITY.md`;
- generated `CONTRIBUTING.md`;
- generated `AGENTS.md`;
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
   - Do not commit `.secrets.baseline` into `sports-forecast-lab` unless the
     private exporter is changed to generate it and regenerate
     `PUBLIC_EXPORT_MANIFEST.json`; otherwise it breaks manifest/tree equality.

## Warning Disposition

Known acceptable warning class: generic policy-language references in public
governance docs. These warnings exist because the public package explains
privacy and no-automation boundaries. They are acceptable only when no exact
private records, dollar rows, user/friend identifiers, local paths, raw
screenshots, `data/slates/`, private ledgers, caches, or model binaries are
included.

Latest reviewed smoke on 2026-06-16:

- public export creator: pass;
- public export validator: pass;
- MLB adapter skeleton validator: pass;
- Gitleaks git and directory scans: pass;
- TruffleHog git and filesystem scans: pass with `--no-update`,
  `--no-verification`, and `--fail`;
- `detect-secrets`: pass after excluding only manifest hash/provenance fields
  `sha256`, `full_dataset_sha256`, and `source_git_sha`;
- file count: `29`;
- errors: `0`;
- warnings: `0`;
- publication status: public GitHub repo created, pushed, and locally
  post-publication verified;
- public repo URL: `https://github.com/M-Gage-Plott42/sports-forecast-lab`;
- public commit: moving public `main`; use GitHub history for the current
  published HEAD;
- manifest source private HEAD: recorded in `PUBLIC_EXPORT_MANIFEST.json`;
- parked manual follow-up: GitHub UI secret scanning/push-protection settings
  review where available.

Secret-scan false-positive disposition:

- `detect-secrets` raw scan flagged 35 `Hex High Entropy String` candidates in
  manifest files.
- The findings were all reviewed as manifest integrity/provenance hashes:
  SHA-256 file hashes, `full_dataset_sha256`, and `source_git_sha`.
- The accepted final check excludes only those manifest hash/provenance fields:
  `detect-secrets scan --force-use-all-plugins --exclude-lines '"(sha256|full_dataset_sha256|source_git_sha)"\s*:'`.

## Publication Decision Gate

The first public GitHub publication is complete. Before future public updates,
the user must explicitly approve:

- final public GitHub visibility;
- whether the current validated export/rehearsal is approved for GitHub;
- whether Codex should push the public GitHub repository.

After any future public GitHub push, verify:

- `git remote -v` shows the intended public `origin`;
- the pushed repository contains the same manifest-listed tracked files;
- GitHub secret scanning and push protection settings are reviewed in the
  public repository settings where available. The 2026-06-16 UI settings review
  is intentionally parked until the user chooses to do it.
