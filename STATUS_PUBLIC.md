# Public Export Status

- repository_name: sports-forecast-lab
- export_status: public_safe_review_required
- research_only: yes
- no_bet_instruction: yes
- private_data_included: no
- raw_screenshots_included: no
- private_ledgers_included: no
- data_slates_included: no
- model_binaries_included: no
- generated_bulk_included: no
- secrets_included: no
- public_proof_package: included
- mlb_adapter_skeleton: fixture_only
- license: Apache-2.0
- publication_status: local_rehearsal_first

This export is a public framework/demo package. It is not the private operator
status surface and must not be used for account activity, current-event
recommendations, financial decisions, or model-promotion claims.

## Smoke Commands

```bash
python3 scripts/validate_public_repo_export.py --export-root .
python3 scripts/validate_mlb_adapter_skeleton.py
python3 scripts/validate_text_line_endings.py
```
