# MLB Adapter Skeleton

Last updated: 2026-06-15.

Purpose: define the first cross-sport adapter scaffold after public
proof/package prep. This is public-source architecture and fixture validation
only. It does not authorize live-event recommendations, financial calculations,
private account facts, private-data training, account action, broad sport
modeling, or model training.

## Same-Turn Source Verification

Checked on 2026-06-15:

- MLB schedule: `https://www.mlb.com/schedule`
- MLB 2026 schedule release:
  `https://www.mlb.com/news/mlb-2026-schedule-released`
- MLB probable pitchers: `https://www.mlb.com/probable-pitchers`
- Baseball Savant Statcast CSV documentation:
  `https://baseballsavant.mlb.com/csv-docs`

Planning conclusion: MLB is active on 2026-06-15, has a daily public schedule,
and has official public schedule/probable-pitcher/stat surfaces that can support
the first adapter proof after the public export package is reviewable.

## Source Registry Contract

Each MLB source row must preserve:

- `source_id`;
- `source_title`;
- `source_url`;
- `source_tier`;
- `source_access_status`;
- `retrieved_at`;
- `source_timestamp`;
- `timezone`;
- `adapter_use`;
- `review_note`.

Blocked, paywalled, geofenced, login-required, anti-bot, or inaccessible pages
cannot support extracted values. They may be logged only as inaccessible or
partial source context.

## Canonical Entities

The adapter should normalize:

- game: `game_pk`, `season`, `game_type`, `game_date`, `scheduled_start`,
  `status`, `venue`, `neutral_site`, `doubleheader`, `source_event_url`;
- team: `team_id`, `team_name`, `team_abbreviation`, `league`, `division`;
- player: `player_id`, `player_name`, `team_id`, `position`, `handedness`;
- role: probable starter, batting order slot, pitcher role, defensive
  position, active/inactive status;
- stat row: `game_pk`, `player_id`, `team_id`, `stat_group`, `stat_name`,
  `stat_value`, `source_id`, `source_timestamp`.

## Ingestion Design

Initial implementation should be fixture-first:

1. Validate official schedule fixture shape.
2. Validate source registry fields and access statuses.
3. Validate a minimal public box-score/stat fixture shape.
4. Emit no model dataset and no latest/production status.

Future fetchers may be added only after same-turn source verification and must
write source-audited rows with access status and timestamps.

## Validation Contract

The skeleton validator is `scripts/validate_mlb_adapter_skeleton.py`. It checks
only checked-in fixtures and templates:

- source registry required columns;
- accepted access statuses;
- schedule game IDs, timestamps, teams, status, and source IDs;
- box-score game/player/team/stat references;
- research-only and no-bet-instruction flags.

No network call, model training, account-specific lookup, or financial
calculation is part of this skeleton.

## Promotion Boundary

MLB adapter work cannot move from skeleton to modeling until:

- official source rows are fetched or transcribed with source/access status;
- fixture validator passes;
- public export validator passes;
- dataset card is drafted;
- time-aware validation design is documented;
- leakage checks and baseline comparisons are specified.
