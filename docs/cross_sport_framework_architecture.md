# Cross-Sport Framework Architecture

Last updated: 2026-06-15.

Purpose: define the reusable sports prediction research framework that can be
exported publicly without private ledger data. This is research/governance
architecture only. It does not authorize live-event recommendations, account
actions, financial calculations, private-data training, or model promotion.

## Design Goal

The public framework should show source-audited prediction research and
reproducible engineering controls, not a private transaction workflow. The NBA
season remains the motivating case study, while cross-sport adapters prove the
architecture can transfer to MLB, WNBA, NFL, and later MLS.

## Invariant Core

These components should be sport-agnostic:

- Source registry: source URL, source title, source tier, source access status,
  source timestamp with timezone offset, retrieval timestamp, and review note.
- Trust boundaries: public research data, private ledger/app truth, ignored
  generated artifacts, and synthetic public demo rows stay separate.
- Canonical entities: event, season, competition, team, participant, role,
  stat, market/stat line, source row, feature snapshot, model run, and model
  card.
- Dataset contracts: `research_only`, `no_bet_instruction`, training scope,
  label source, line source, source verification flag, source note, and
  excluded-row report.
- Validation: chronological splits, leave-entity or leave-matchup checks where
  supported, calibration checks, baseline comparison, leakage checks, and
  manifest/hash validation.
- Promotion controls: no production/latest status without a reviewed model card,
  readiness gate, stable baseline win, and explicit no-live-recommendation
  boundary.
- Export controls: allowlist-only public export, public-safe README/status,
  synthetic private-style demo rows, and validators that fail on private data.

## Adapter Interface

Each sport adapter should define:

- Schedule semantics: event IDs, start timestamps, postponements, neutral sites,
  doubleheaders or multi-game days, playoff structure, and finality rules.
- Participant model: team, player, position/role, availability/injury context,
  starter/lineup status, and roster changes.
- Stat taxonomy: supported public stats, derived stats, period/event labels,
  tie policy, and source endpoint coverage.
- Feature windows: recent form, rest, travel, venue, opponent context, role
  stability, and sport-specific recency windows.
- Outcome labels: public-only outcome labels, exact app/private labels blocked
  from public export, and sport-specific leakage risks.
- Validation split: time-aware default plus one sport-relevant robustness split,
  such as leave-team-pair, leave-player, leave-series, or leave-venue.
- Model card fields: intended use, prohibited use, data coverage, baselines,
  calibration, limitations, source-access status, and no-promotion status.

## Sport Priority

| Priority | Sport | Architecture rationale | Current implementation posture |
|---|---|---|---|
| 1 | MLB | Active daily schedule, high sample volume, official schedule/stat surfaces, strong test of postponements, probable starters, venue, and series cadence. | Fixture-only skeleton implemented; model training blocked until source rows and validation contracts are stable. |
| 2 | WNBA | Active season, basketball-adjacent schemas, smaller sample size, new teams, FIBA break, and direct transfer from NBA role/minutes concepts. | Second adapter target. |
| 3 | NFL | High resume signal and clear schedule structure, but regular season starts later and sample size is lower. | Prep lane for schema design, not active outcome modeling now. |
| 4 | MLS | Active but paused May 25-July 16 for the World Cup; soccer introduces draws, lower scoring, international absences, and lineup uncertainty. | Later adapter after MLB/WNBA. |
| Defer | NHL | 2026 Stanley Cup Final is complete as of the June 15 NHL.com update. | Not first because active runway is closing. |
| Defer | FIFA World Cup 2026 | High-profile but short tournament with special tournament dynamics. | Not first reusable-framework target. |

## Opened Implementation Order

The 2026-06-15 NE-policy planning decision opens the public proof/package and
adapter lane in this order:

1. Public proof/package prep.
2. MLB adapter skeleton.
3. WNBA adapter skeleton.
4. NFL prep lane.
5. MLS later.

Do not jump straight into broad sport modeling. The MLB skeleton now has
official-source basis, a source registry template, canonical game/team/player
schema notes, box-score/stat ingestion design, timestamp/access-status
requirements, and fixture-only smokes. It must not train models until source
rows, validation contracts, and public-export boundaries are stable.

## Public Proof Package

The reusable public proof should include:

- Prediction proof: baseline comparison, Brier/log-loss/ECE, reliability table or
  plot, chronological split, and limitations.
- Engineering proof: schema, source manifest, validators, deterministic smoke,
  run manifest, and reproducible quickstart.
- Governance proof: model card, dataset card, privacy/export policy,
  no-bet/no-automation boundary, and source-access handling.
- Transfer proof: one NBA case-study adapter plus MLB/WNBA starter adapters or
  adapter specs with synthetic fixtures.

## External Reference Basis

- GitHub README guidance supports a public README that explains what the
  project does, why it is useful, how to start, where to get help, and who
  maintains it.
- GitHub license guidance supports adding an explicit license before claiming a
  public repository is open source.
- NIST AI RMF frames trustworthiness considerations across design,
  development, use, and evaluation.
- Datasheets for Datasets motivates documenting dataset motivation,
  composition, collection, and recommended use.
- Model Cards for Model Reporting motivates documenting model performance,
  intended use, limitations, and evaluation context.
- OpenSSF Scorecard provides a security-risk check model for public
  open-source project posture.
