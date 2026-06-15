#!/usr/bin/env python3
"""Validate fixture-only MLB adapter skeleton files."""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE_ROOT = ROOT / "scripts" / "fixtures" / "mlb_adapter"
SOURCE_REGISTRY_COLUMNS = [
    "source_id",
    "source_title",
    "source_url",
    "source_tier",
    "source_access_status",
    "retrieved_at",
    "source_timestamp",
    "timezone",
    "adapter_use",
    "review_note",
]
ALLOWED_ACCESS_STATUSES = {
    "accessible",
    "partial",
    "blocked",
    "paywalled",
    "geofenced",
    "login_required",
    "anti_bot",
    "inaccessible",
}
RFC3339_WITH_OFFSET = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture-root",
        default=str(DEFAULT_FIXTURE_ROOT),
        help="Directory containing MLB adapter fixture files.",
    )
    return parser.parse_args()


def load_json(path: Path, errors: list[str]) -> dict[str, object]:
    if not path.exists():
        errors.append(f"{path}: missing fixture")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return {}


def validate_timestamp(value: str, label: str, errors: list[str]) -> None:
    if not RFC3339_WITH_OFFSET.match(value):
        errors.append(f"{label}: expected RFC3339 timestamp with timezone offset")


def validate_source_registry(path: Path, errors: list[str]) -> set[str]:
    if not path.exists():
        errors.append(f"{path}: missing source registry fixture")
        return set()
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != SOURCE_REGISTRY_COLUMNS:
            errors.append(f"{path}: unexpected columns {reader.fieldnames}")
            return set()
        source_ids: set[str] = set()
        for line_number, row in enumerate(reader, start=2):
            source_id = (row.get("source_id") or "").strip()
            if not source_id:
                errors.append(f"{path}:{line_number}: missing source_id")
            if source_id in source_ids:
                errors.append(f"{path}:{line_number}: duplicate source_id {source_id}")
            source_ids.add(source_id)
            if not (row.get("source_url") or "").startswith("https://"):
                errors.append(f"{path}:{line_number}: source_url must be https")
            if row.get("source_tier") != "official":
                errors.append(f"{path}:{line_number}: source_tier must be official")
            if row.get("source_access_status") not in ALLOWED_ACCESS_STATUSES:
                errors.append(f"{path}:{line_number}: invalid source_access_status")
            validate_timestamp(row.get("retrieved_at", ""), f"{path}:{line_number}: retrieved_at", errors)
            validate_timestamp(row.get("source_timestamp", ""), f"{path}:{line_number}: source_timestamp", errors)
            if not row.get("adapter_use"):
                errors.append(f"{path}:{line_number}: missing adapter_use")
        if not source_ids:
            errors.append(f"{path}: source registry must have at least one row")
        return source_ids


def validate_schedule(data: dict[str, object], source_ids: set[str], errors: list[str]) -> set[int]:
    if data.get("mode") != "mlb_adapter_schedule_fixture":
        errors.append("official_schedule_fixture.json: mode must be mlb_adapter_schedule_fixture")
    if data.get("research_only") != "yes" or data.get("no_bet_instruction") != "yes":
        errors.append("official_schedule_fixture.json: research/no-bet flags must be yes")
    games = data.get("games")
    if not isinstance(games, list) or not games:
        errors.append("official_schedule_fixture.json: games must be a nonempty list")
        return set()
    game_pks: set[int] = set()
    for index, game in enumerate(games):
        if not isinstance(game, dict):
            errors.append(f"official_schedule_fixture.json: game {index} must be an object")
            continue
        game_pk = game.get("game_pk")
        if not isinstance(game_pk, int):
            errors.append(f"official_schedule_fixture.json: game {index} missing integer game_pk")
        else:
            game_pks.add(game_pk)
        if game.get("game_type") not in {"R", "P", "S"}:
            errors.append(f"official_schedule_fixture.json: game {index} invalid game_type")
        validate_timestamp(str(game.get("scheduled_start", "")), f"official_schedule_fixture.json: game {index} scheduled_start", errors)
        if game.get("source_id") not in source_ids:
            errors.append(f"official_schedule_fixture.json: game {index} source_id not in registry")
        for side in ("away_team", "home_team"):
            team = game.get(side)
            if not isinstance(team, dict):
                errors.append(f"official_schedule_fixture.json: game {index} missing {side}")
                continue
            if not isinstance(team.get("team_id"), int):
                errors.append(f"official_schedule_fixture.json: game {index} {side} missing team_id")
            if not team.get("team_name") or not team.get("team_abbreviation"):
                errors.append(f"official_schedule_fixture.json: game {index} {side} missing names")
    return game_pks


def validate_boxscore(data: dict[str, object], game_pks: set[int], source_ids: set[str], errors: list[str]) -> None:
    if data.get("mode") != "mlb_adapter_boxscore_fixture":
        errors.append("public_boxscore_fixture.json: mode must be mlb_adapter_boxscore_fixture")
    if data.get("research_only") != "yes" or data.get("no_bet_instruction") != "yes":
        errors.append("public_boxscore_fixture.json: research/no-bet flags must be yes")
    if data.get("game_pk") not in game_pks:
        errors.append("public_boxscore_fixture.json: game_pk must reference schedule fixture")
    player_stats = data.get("player_stats")
    if not isinstance(player_stats, list) or not player_stats:
        errors.append("public_boxscore_fixture.json: player_stats must be a nonempty list")
        return
    for index, row in enumerate(player_stats):
        if not isinstance(row, dict):
            errors.append(f"public_boxscore_fixture.json: player_stats {index} must be an object")
            continue
        for key in ("player_id", "player_name", "team_id", "team_abbreviation", "stat_group", "stats", "source_id"):
            if key not in row:
                errors.append(f"public_boxscore_fixture.json: row {index} missing {key}")
        if row.get("source_id") not in source_ids:
            errors.append(f"public_boxscore_fixture.json: row {index} source_id not in registry")
        if not isinstance(row.get("stats"), dict) or not row.get("stats"):
            errors.append(f"public_boxscore_fixture.json: row {index} stats must be nonempty object")


def validate_fixture_root(root: Path) -> list[str]:
    errors: list[str] = []
    source_ids = validate_source_registry(root / "source_registry_fixture.csv", errors)
    schedule = load_json(root / "official_schedule_fixture.json", errors)
    game_pks = validate_schedule(schedule, source_ids, errors) if schedule else set()
    boxscore = load_json(root / "public_boxscore_fixture.json", errors)
    if boxscore:
        validate_boxscore(boxscore, game_pks, source_ids, errors)
    return errors


def main() -> int:
    args = parse_args()
    errors = validate_fixture_root(Path(args.fixture_root))
    for error in errors:
        print(f"ERROR: {error}")
    print(f"errors: {len(errors)}")
    if not errors:
        print("OK: MLB adapter skeleton fixtures validate; no network/model/app workflow performed.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
