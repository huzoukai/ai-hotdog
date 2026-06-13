#!/usr/bin/env python3
"""Validate AI-HOTDog markdown source registry tables."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_COLUMNS = {
    "source_id",
    "name",
    "region",
    "type",
    "access_mode",
    "priority",
    "url_or_query",
    "required_signals",
    "failure_policy",
}

ALLOWED = {
    "region": {"global", "china", "both", "custom"},
    "type": {
        "official",
        "code",
        "paper",
        "media",
        "search",
        "social",
        "video",
        "product",
        "appstore",
        "government",
        "community",
    },
    "access_mode": {"public", "chrome_login", "manual"},
    "priority": {"primary", "secondary", "supplemental"},
    "failure_policy": {"skip", "manual_required", "limited_note"},
}


def split_md_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def parse_source_rows(text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    rows: list[dict[str, str]] = []
    i = 0
    while i < len(lines) - 1:
        line = lines[i].strip()
        next_line = lines[i + 1].strip()
        if not (line.startswith("|") and next_line.startswith("|")):
            i += 1
            continue

        header = split_md_row(line)
        separator = split_md_row(next_line)
        if "source_id" not in header or not is_separator(separator):
            i += 1
            continue

        j = i + 2
        while j < len(lines) and lines[j].strip().startswith("|"):
            cells = split_md_row(lines[j])
            if len(cells) == len(header):
                rows.append(dict(zip(header, cells)))
            j += 1
        i = j
    return rows


def validate(rows: list[dict[str, str]]) -> tuple[list[str], dict[str, object]]:
    errors: list[str] = []
    seen: set[str] = set()
    type_counts: dict[str, int] = {}
    region_counts: dict[str, int] = {}

    if not rows:
        errors.append("No source registry table with a source_id column was found.")
        return errors, {"source_count": 0}

    for idx, row in enumerate(rows, start=1):
        missing = sorted(col for col in REQUIRED_COLUMNS if col not in row)
        if missing:
            errors.append(f"row {idx}: missing columns: {', '.join(missing)}")
            continue

        sid = row["source_id"].strip()
        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", sid):
            errors.append(f"row {idx}: invalid source_id {sid!r}")
        if sid in seen:
            errors.append(f"row {idx}: duplicate source_id {sid!r}")
        seen.add(sid)

        for field, allowed_values in ALLOWED.items():
            value = row[field].strip()
            if value not in allowed_values:
                errors.append(
                    f"row {idx} ({sid}): invalid {field} {value!r}; "
                    f"expected one of {', '.join(sorted(allowed_values))}"
                )

        if not row["url_or_query"].strip():
            errors.append(f"row {idx} ({sid}): url_or_query is blank")
        if not row["required_signals"].strip():
            errors.append(f"row {idx} ({sid}): required_signals is blank")

        type_counts[row.get("type", "").strip()] = type_counts.get(row.get("type", "").strip(), 0) + 1
        region_counts[row.get("region", "").strip()] = region_counts.get(row.get("region", "").strip(), 0) + 1

    summary = {
        "source_count": len(rows),
        "type_counts": type_counts,
        "region_counts": region_counts,
    }
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path, help="Path to source-registry.md")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    text = args.registry.read_text(encoding="utf-8")
    rows = parse_source_rows(text)
    errors, summary = validate(rows)

    if args.format == "json":
        print(json.dumps({"ok": not errors, "errors": errors, "summary": summary}, ensure_ascii=False, indent=2))
    else:
        if errors:
            print("Source registry validation failed:")
            for error in errors:
                print(f"- {error}")
        else:
            print("Source registry is valid.")
        print(f"Sources: {summary.get('source_count', 0)}")
        for key, counts in (("Types", summary.get("type_counts", {})), ("Regions", summary.get("region_counts", {}))):
            printable = ", ".join(f"{name}={count}" for name, count in sorted(counts.items()))
            print(f"{key}: {printable}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
