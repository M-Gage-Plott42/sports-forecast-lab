#!/usr/bin/env python3
"""Validate that tracked text files use LF line endings.

Python's csv module defaults to CRLF output for writers unless a lineterminator
is supplied. This check catches accidental CRLF rewrites before commit.
"""
from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BINARY_SUFFIXES = {
    ".bin",
    ".db",
    ".gif",
    ".gz",
    ".heic",
    ".jpeg",
    ".jpg",
    ".joblib",
    ".onnx",
    ".pdf",
    ".pickle",
    ".pkl",
    ".png",
    ".pt",
    ".pth",
    ".sqlite",
    ".tar",
    ".webp",
    ".zip",
}
SKIP_PARTS = {".git", ".venv", "__pycache__", ".mypy_cache", ".pytest_cache"}


def tracked_files() -> list[Path]:
    try:
        output = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL)
    except (OSError, subprocess.CalledProcessError):
        return [
            path.relative_to(ROOT)
            for path in ROOT.rglob("*")
            if path.is_file() and not (set(path.relative_to(ROOT).parts) & SKIP_PARTS)
        ]
    return [Path(line) for line in output.splitlines() if line.strip()]


def should_check(path: Path) -> bool:
    if set(path.parts) & SKIP_PARTS:
        return False
    if path.suffix.lower() in BINARY_SUFFIXES:
        return False
    return True


def main() -> int:
    errors: list[str] = []
    checked = 0
    for rel in tracked_files():
        if not should_check(rel):
            continue
        path = ROOT / rel
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if b"\0" in data:
            continue
        checked += 1
        if b"\r\n" in data or b"\r" in data:
            errors.append(f"{rel.as_posix()}: contains CRLF/CR line endings; normalize to LF")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"text_line_ending_files_checked: {checked}")
    print(f"errors: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
