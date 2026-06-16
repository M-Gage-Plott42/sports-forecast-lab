#!/usr/bin/env python3
"""Validate an allowlist-only public repo export package."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


TEXT_SUFFIXES = {".csv", ".json", ".md", ".py", ".sh", ".txt", ".yml", ".yaml", ".in"}
TEXT_FILENAMES = {"LICENSE"}
MANIFEST_PATH = "PUBLIC_EXPORT_MANIFEST.json"
MANIFEST_SELF_SHA256 = "self-referential"
BANNED_PREFIXES = {
    "data/ledgers/",
    "data/slates/",
    "data/raw/",
    "reports/slates/",
    "reports/gpt_context/current/",
    "reports/gpt_context/archive/",
    "reports/models/",
    "reports/ml_runs/",
    "reports/smokes/",
    "reports/experiments/",
    "models/",
    "mlruns/",
    "syncthing/",
    "exploratory/",
}
BANNED_PATH_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "cache",
}
IGNORED_SCAN_PATH_PARTS = {
    ".git",
}
BANNED_FILENAMES = {
    "STATUS.md",
    "ledger.sqlite",
    "ledger.db",
    "ledger.sqlite3",
}
BANNED_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".heic",
    ".zip",
    ".7z",
    ".rar",
    ".gz",
    ".zst",
    ".tar",
    ".pkl",
    ".pickle",
    ".joblib",
    ".cloudpickle",
    ".pt",
    ".pth",
    ".onnx",
    ".bin",
    ".sqlite",
    ".db",
}
REQUIRED_FILES = {
    "AGENTS.md",
    "README.md",
    "STATUS_PUBLIC.md",
    "RESEARCH_BOUNDARY.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "PUBLIC_EXPORT_MANIFEST.json",
    "data/demo/PUBLIC_SAMPLE_MANIFEST.json",
    "data/demo/synthetic_private_style_rows.csv",
    "data/schemas/public_research_schema.json",
    "docs/public_release_checklist.md",
    "docs/dataset_cards/public_outcome_dataset_example.md",
    "docs/model_cards/public_outcome_baseline_example.md",
    "docs/sport_adapters/mlb_adapter_skeleton.md",
    "scripts/validate_mlb_adapter_skeleton.py",
}
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
]
PRIVATE_ERROR_PATTERNS = [
    re.compile(r"\b20\d{6}-PP-[A-Z0-9][A-Z0-9_-]*\b"),
    re.compile(r"(?i)\b(entry fee|to win|paid|payout|stake|entry_amount|payout_preview|payout_display)\b[^\n\r]{0,80}\$\s*\d"),
    re.compile(r"(?i)\$\s*\d[^\n\r]{0,80}\b(entry fee|to win|paid|payout|stake)\b"),
    re.compile(r"(?i)\b(?:hit|missed)\s+at\s+\d+(?:\.\d+)?\b"),
]
PRIVATE_REVIEW_PATTERNS = [
    re.compile(r"(?i)\b(entry submitted|submitted-entry|settlement-quality exact)\b"),
    re.compile(r"(?i)\b(payout preview|payout display|paid amount|private ticket)\b"),
]
LOCAL_PATH_PATTERNS = [
    re.compile(r"/home/[A-Za-z0-9_.-]+/"),
    re.compile(r"/mnt/[a-z]/Users/[^/\s]+/", re.IGNORECASE),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export-root", required=True, help="Export root to validate.")
    return parser.parse_args()


def rel_path(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def read_manifest(path: Path) -> dict[str, object]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: invalid PUBLIC_EXPORT_MANIFEST.json: {exc}") from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def actual_export_files(root: Path) -> list[str]:
    if (root / ".git").exists():
        try:
            output = subprocess.check_output(
                ["git", "ls-files"],
                cwd=root,
                text=True,
                stderr=subprocess.DEVNULL,
            )
        except (OSError, subprocess.CalledProcessError):
            pass
        else:
            return sorted(line.strip() for line in output.splitlines() if line.strip())
    files: list[str] = []
    for path in root.rglob("*"):
        if path.is_dir() or should_skip_scan(root, path):
            continue
        files.append(rel_path(root, path))
    return sorted(files)


def validate_manifest_file_set(root: Path, manifest: dict[str, object], errors: list[str]) -> None:
    file_entries = manifest.get("files")
    if not isinstance(file_entries, list) or not file_entries:
        errors.append("PUBLIC_EXPORT_MANIFEST.json files must be a nonempty list")
        return

    actual_files = actual_export_files(root)
    actual_file_set = set(actual_files)
    if manifest.get("file_count") != len(actual_files):
        errors.append(
            "PUBLIC_EXPORT_MANIFEST.json file_count must match actual exported file count "
            f"({len(actual_files)})"
        )

    manifest_paths: list[str] = []
    copied_count = 0
    generated_count = 0
    for index, entry in enumerate(file_entries):
        if not isinstance(entry, dict):
            errors.append(f"PUBLIC_EXPORT_MANIFEST.json files[{index}] must be an object")
            continue
        path = entry.get("path")
        if not isinstance(path, str) or not path:
            errors.append(f"PUBLIC_EXPORT_MANIFEST.json files[{index}] missing path")
            continue
        manifest_paths.append(path)
        generated = entry.get("generated")
        if generated is True:
            generated_count += 1
        elif generated is False:
            copied_count += 1
        else:
            errors.append(f"{path}: manifest generated must be true or false")
            continue

        target = root / path
        if path not in actual_file_set:
            errors.append(f"{path}: manifest entry missing from actual exported tree")
            continue
        actual_size = target.stat().st_size
        if entry.get("size_bytes") != actual_size:
            errors.append(f"{path}: manifest size_bytes must be {actual_size}")
        if path == MANIFEST_PATH:
            if entry.get("sha256") != MANIFEST_SELF_SHA256:
                errors.append(f"{path}: manifest sha256 must be {MANIFEST_SELF_SHA256}")
            if not entry.get("hash_note"):
                errors.append(f"{path}: manifest self-entry must include hash_note")
        else:
            actual_sha = sha256_file(target)
            if entry.get("sha256") != actual_sha:
                errors.append(f"{path}: manifest sha256 must be {actual_sha}")

    duplicate_paths = sorted({path for path in manifest_paths if manifest_paths.count(path) > 1})
    for path in duplicate_paths:
        errors.append(f"{path}: duplicate PUBLIC_EXPORT_MANIFEST.json file entry")

    manifest_file_set = set(manifest_paths)
    extra_manifest_paths = sorted(manifest_file_set - actual_file_set)
    missing_manifest_paths = sorted(actual_file_set - manifest_file_set)
    for path in extra_manifest_paths:
        errors.append(f"{path}: manifest lists file not present in actual exported tree")
    for path in missing_manifest_paths:
        errors.append(f"{path}: tracked/exported file missing from PUBLIC_EXPORT_MANIFEST.json")

    if manifest.get("copied_file_count") != copied_count:
        errors.append(f"PUBLIC_EXPORT_MANIFEST.json copied_file_count must be {copied_count}")
    if manifest.get("generated_file_count") != generated_count:
        errors.append(f"PUBLIC_EXPORT_MANIFEST.json generated_file_count must be {generated_count}")


def validate_manifest(root: Path, errors: list[str]) -> None:
    manifest_path = root / MANIFEST_PATH
    if not manifest_path.exists():
        errors.append("missing PUBLIC_EXPORT_MANIFEST.json")
        return
    manifest = read_manifest(manifest_path)
    if manifest.get("mode") != "public_repo_export":
        errors.append("PUBLIC_EXPORT_MANIFEST.json mode must be public_repo_export")
    if manifest.get("public_repository_name") != "sports-forecast-lab":
        errors.append("PUBLIC_EXPORT_MANIFEST.json public_repository_name must be sports-forecast-lab")
    if manifest.get("license") != "Apache-2.0":
        errors.append("PUBLIC_EXPORT_MANIFEST.json license must be Apache-2.0")
    required_flags = {
        "research_only": "yes",
        "no_bet_instruction": "yes",
        "private_data_included": "no",
        "data_slates_included": "no",
        "raw_screenshots_included": "no",
        "generated_bulk_included": "no",
        "model_binaries_included": "no",
        "secrets_included": "no",
        "root_status_md_included": "no",
        "public_safe_status_included": "yes",
    }
    for key, expected in required_flags.items():
        if str(manifest.get(key, "")).strip().lower() != expected:
            errors.append(f"PUBLIC_EXPORT_MANIFEST.json {key} must be {expected}")
    validate_manifest_file_set(root, manifest, errors)
    if manifest.get("validation_result") not in {"pass", "not_run"}:
        errors.append("PUBLIC_EXPORT_MANIFEST.json validation_result must be pass or not_run")
    if "validation_warning_disposition" not in manifest:
        errors.append("PUBLIC_EXPORT_MANIFEST.json must record validation_warning_disposition")


def validate_path(root: Path, path: Path, errors: list[str], warnings: list[str]) -> None:
    rel = rel_path(root, path)
    parts = set(Path(rel).parts)
    if any(rel.startswith(prefix) for prefix in BANNED_PREFIXES):
        errors.append(f"{rel}: banned private/generated prefix")
    if parts & BANNED_PATH_PARTS:
        errors.append(f"{rel}: banned path component")
    if path.name in BANNED_FILENAMES:
        errors.append(f"{rel}: banned filename")
    suffix = path.suffix.lower()
    if suffix in BANNED_SUFFIXES:
        errors.append(f"{rel}: banned suffix")
    if suffix not in TEXT_SUFFIXES and path.name not in TEXT_FILENAMES:
        warnings.append(f"{rel}: non-text suffix; verify public-export allowlist")
        return
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"{rel}: text file is not UTF-8 decodable")
        return
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"{rel}: possible secret/token pattern")
            break
    for pattern in LOCAL_PATH_PATTERNS:
        if pattern.search(text):
            errors.append(f"{rel}: local filesystem path pattern")
            break
    for pattern in PRIVATE_ERROR_PATTERNS:
        if pattern.search(text):
            errors.append(f"{rel}: private ticket/app payout/settlement pattern")
            break
    if rel.startswith("scripts/"):
        return
    for pattern in PRIVATE_REVIEW_PATTERNS:
        if pattern.search(text):
            warnings.append(f"{rel}: generic private-app policy term; manually review public framing")
            break


def should_skip_scan(root: Path, path: Path) -> bool:
    rel = rel_path(root, path)
    return bool(set(Path(rel).parts) & IGNORED_SCAN_PATH_PARTS)


def validate_tree(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"ERROR: missing export root {root}")
    for required in sorted(REQUIRED_FILES):
        if not (root / required).exists():
            errors.append(f"missing required public export file: {required}")
    validate_manifest(root, errors)
    for path in sorted(root.rglob("*")):
        if path.is_dir():
            continue
        if should_skip_scan(root, path):
            continue
        validate_path(root, path, errors, warnings)
    return errors, warnings


def main() -> int:
    args = parse_args()
    errors, warnings = validate_tree(Path(args.export_root))
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"errors: {len(errors)}")
    print(f"warnings: {len(warnings)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
