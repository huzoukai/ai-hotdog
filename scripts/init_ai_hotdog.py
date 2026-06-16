#!/usr/bin/env python3
"""Initialize non-secret AI-HOTDog workspace state."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_REGISTRY = SKILL_DIR / "references" / "source-registry.md"
sys.path.insert(0, str(SCRIPT_DIR))

from validate_source_registry import parse_source_rows, validate  # noqa: E402


CONTENT_GOALS = {
    "content_ideas",
    "industry_intelligence",
    "product_opportunities",
    "competitor_monitoring",
    "custom",
}

AUTOMATION_ACTIONS = {
    "daily_hotspot_report",
    "content_ideas",
    "competitor_monitoring",
    "industry_brief",
    "custom",
}

PLATFORM_SCOPES = {"stable_public", "login_supplement", "all"}
PROFILES = {"ai", "general", "custom"}
FREQUENCIES = {"manual", "daily", "weekly"}
AUTH_POLICIES = {"prompt_each_run", "skip_when_unavailable", "public_only"}


def csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def source_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        return ""
    next_start = text.find("\n## ", start + len(marker))
    return text[start:] if next_start < 0 else text[start:next_start]


def select_sources(rows: list[dict[str, str]], registry_text: str, profile: str, regions: set[str], platform_scope: str) -> list[dict[str, str]]:
    general_ids = {row["source_id"] for row in parse_source_rows(source_section(registry_text, "General Stable Sources"))}
    general_ids.update(row["source_id"] for row in parse_source_rows(source_section(registry_text, "China Stable Sources")))
    ai_ids = {row["source_id"] for row in parse_source_rows(source_section(registry_text, "Default AI Vertical Sources"))}
    row_by_id = {row["source_id"]: row for row in rows}

    selected_ids = set(general_ids)
    if profile == "ai":
        selected_ids.update(ai_ids)

    selected: list[dict[str, str]] = []
    for sid in sorted(selected_ids):
        row = row_by_id[sid]
        if row["region"] not in regions and row["region"] != "both":
            continue
        if platform_scope == "stable_public" and row["access_mode"] != "public":
            continue
        if platform_scope == "login_supplement" and row["access_mode"] not in {"public", "chrome_login", "manual"}:
            continue
        selected.append(row)
    return selected


def initial_status(row: dict[str, str]) -> str:
    if row["access_mode"] == "public":
        return "unchecked"
    if row["access_mode"] == "chrome_login":
        return "login_required"
    return "manual_required"


def selected_login_sources(rows: list[dict[str, str]], explicit: str) -> list[str]:
    selected_ids = {row["source_id"] for row in rows}
    if explicit.strip():
        requested = csv(explicit)
        unknown = sorted(set(requested) - selected_ids)
        if unknown:
            raise ValueError(f"login sources are not selected or do not exist: {', '.join(unknown)}")
        return requested
    return [row["source_id"] for row in rows if row["access_mode"] in {"chrome_login", "manual"}]


def default_auth_policy(platform_scope: str) -> str:
    return "public_only" if platform_scope == "stable_public" else "prompt_each_run"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True, help="Workspace where .ai-hotdog/ should be created")
    parser.add_argument("--topic", required=True, help="Focus topic, such as AI, finance, education, or a custom domain")
    parser.add_argument("--profile", choices=sorted(PROFILES), default="ai")
    parser.add_argument("--core-keywords", required=True, help="Comma-separated core keywords")
    parser.add_argument("--exclude-keywords", default="", help="Comma-separated exclude keywords")
    parser.add_argument("--entity-keywords", default="", help="Comma-separated brands, people, products, or companies")
    parser.add_argument("--regions", default="global,china", help="Comma-separated regions")
    parser.add_argument("--content-goal", choices=sorted(CONTENT_GOALS), default="content_ideas")
    parser.add_argument("--automation-action", choices=sorted(AUTOMATION_ACTIONS), default="daily_hotspot_report")
    parser.add_argument("--automation-schedule", default="manual", help="Human-readable schedule; Codex automation stores the actual schedule")
    parser.add_argument("--platform-scope", choices=sorted(PLATFORM_SCOPES), default="login_supplement")
    parser.add_argument("--login-sources", default="", help="Comma-separated login-state source ids to check before scans")
    parser.add_argument("--auth-policy", choices=sorted(AUTH_POLICIES), default=None)
    parser.add_argument("--frequency", choices=sorted(FREQUENCIES), default="manual")
    parser.add_argument("--output-language", default="zh-CN")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--force", action="store_true", help="Overwrite existing config and status files")
    args = parser.parse_args()

    registry_text = args.registry.read_text(encoding="utf-8")
    rows = parse_source_rows(registry_text)
    errors, _summary = validate(rows)
    if errors:
        for error in errors:
            print(f"registry error: {error}", file=sys.stderr)
        return 1

    regions = set(csv(args.regions) or ["global", "china"])
    selected = select_sources(rows, registry_text, args.profile, regions, args.platform_scope)
    if not selected:
        print("No sources selected. Check profile, regions, and platform scope.", file=sys.stderr)
        return 1

    state_dir = args.workspace / ".ai-hotdog"
    reports_dir = state_dir / "reports"
    config_path = state_dir / "config.json"
    status_path = state_dir / "source-status.json"

    if not args.force and (config_path.exists() or status_path.exists()):
        print(f"Refusing to overwrite existing state in {state_dir}. Use --force to replace it.", file=sys.stderr)
        return 2

    timestamp = now_iso()
    auth_policy = args.auth_policy or default_auth_policy(args.platform_scope)
    try:
        login_sources = selected_login_sources(selected, args.login_sources)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if auth_policy == "public_only":
        login_sources = []
    state_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    config = {
        "schema_version": 1,
        "created_at": timestamp,
        "updated_at": timestamp,
        "display_name": "AI-HOTDog",
        "focus_topic": args.topic,
        "profile": args.profile,
        "core_keywords": csv(args.core_keywords),
        "exclude_keywords": csv(args.exclude_keywords),
        "entity_keywords": csv(args.entity_keywords),
        "regions": sorted(regions),
        "content_goal": args.content_goal,
        "automation_action": args.automation_action,
        "automation_schedule": args.automation_schedule,
        "platform_scope": args.platform_scope,
        "login_sources": login_sources,
        "auth_policy": auth_policy,
        "frequency": args.frequency,
        "output_language": args.output_language,
        "strict_citation": True,
        "report_targets": {"hotspots": 10, "content_ideas": 5},
        "selected_sources": [row["source_id"] for row in selected],
        "source_registry_path": str(args.registry),
    }

    status = {
        "schema_version": 1,
        "updated_at": timestamp,
        "sources": {
            row["source_id"]: {
                "status": initial_status(row),
                "last_checked_at": None,
                "checked_by": "init",
                "access_mode": row["access_mode"],
                "priority": row["priority"],
                "auth_required": row["source_id"] in login_sources,
                "evidence_url": row["url_or_query"].replace("{keywords}", args.topic),
                "usable_signals": [],
                "notes": "Initialized from source registry.",
            }
            for row in selected
        },
    }

    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "state_dir": str(state_dir), "selected_sources": len(selected), "login_sources": login_sources, "auth_policy": auth_policy}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
