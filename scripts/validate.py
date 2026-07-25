#!/usr/bin/env python3
"""Validate dataset/*/info.json and tile images against the documented schema."""

import json
import sys
from pathlib import Path

DATASET_DIR = Path(__file__).resolve().parent.parent / "dataset"
VALID_TILE_COUNTS = {9, 16}


def validate_challenge(folder: Path) -> list[str]:
    errors = []

    info_path = folder / "info.json"
    if not info_path.exists():
        return [f"missing info.json"]

    try:
        info = json.loads(info_path.read_text())
    except json.JSONDecodeError as e:
        return [f"invalid JSON in info.json: {e}"]

    for field, expected_type in (("instruction", str), ("keyword", str), ("correct_answers", list)):
        if field not in info:
            errors.append(f"info.json missing field '{field}'")
        elif not isinstance(info[field], expected_type):
            errors.append(f"info.json field '{field}' should be {expected_type.__name__}")

    tile_files = sorted(folder.glob("tile_*.png"))
    tile_count = len(tile_files)
    if tile_count not in VALID_TILE_COUNTS:
        errors.append(f"unexpected tile count {tile_count} (expected 9 or 16)")
    else:
        expected_names = {f"tile_{i}.png" for i in range(tile_count)}
        actual_names = {f.name for f in tile_files}
        if expected_names != actual_names:
            missing = expected_names - actual_names
            extra = actual_names - expected_names
            if missing:
                errors.append(f"missing tile files: {sorted(missing)}")
            if extra:
                errors.append(f"unexpected tile files: {sorted(extra)}")

    if isinstance(info.get("correct_answers"), list) and tile_count in VALID_TILE_COUNTS:
        for idx in info["correct_answers"]:
            if not isinstance(idx, int) or not (0 <= idx < tile_count):
                errors.append(f"correct_answers index {idx!r} out of range for {tile_count} tiles")

    return errors


def main() -> int:
    if not DATASET_DIR.exists():
        print(f"dataset directory not found: {DATASET_DIR}", file=sys.stderr)
        return 1

    folders = sorted(p for p in DATASET_DIR.iterdir() if p.is_dir())
    type_a_count = 0
    type_b_count = 0
    total_errors = 0

    for folder in folders:
        errors = validate_challenge(folder)
        if errors:
            total_errors += len(errors)
            print(f"{folder.name}:")
            for err in errors:
                print(f"  - {err}")
            continue

        tile_count = len(list(folder.glob("tile_*.png")))
        if tile_count == 9:
            type_a_count += 1
        elif tile_count == 16:
            type_b_count += 1

    print()
    print(f"Checked {len(folders)} challenges")
    print(f"  Type A (3x3): {type_a_count}")
    print(f"  Type B (4x4): {type_b_count}")
    print(f"  Errors: {total_errors}")

    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
