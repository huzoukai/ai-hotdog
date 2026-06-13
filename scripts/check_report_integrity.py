#!/usr/bin/env python3
"""Check an AI-HOTDog report for required sections, counts, and citations."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_SECTIONS = [
    "今日结论",
    "数据来源概览",
    "热点 Top 10",
    "细分观察",
    "自媒体选题 Top 5",
    "今日最推荐选题",
    "平台访问状态",
    "引用与来源表",
]

HOTSPOT_FIELDS = [
    "一句话摘要",
    "为什么重要",
    "分类",
    "热度评分",
    "可信度评分",
    "选题价值评分",
    "主要事实来源",
    "讨论热度来源",
    "抓取时间",
    "置信度",
]

IDEA_FIELDS = [
    "核心观点",
    "适合平台",
    "开头钩子",
    "内容结构",
    "可引用素材",
    "风险提醒",
]

OVERVIEW_METRICS = [
    "扫描平台",
    "成功访问",
    "访问受限",
    "总候选内容",
    "进入评分池",
    "最终引用内容",
]

SOURCE_SHARE_LABELS = [
    "官方/原始发布",
    "新闻媒体",
    "社交讨论",
    "视频平台",
    "开源/项目平台",
    "论文/研究",
    "产品/创业",
    "中文互联网",
]


def section_text(text: str, section: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(section)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    next_match = re.search(r"^##\s+", text[match.end() :], re.MULTILINE)
    if not next_match:
        return text[match.end() :]
    return text[match.end() : match.end() + next_match.start()]


def count_ranked_entries(block: str) -> int:
    heading_count = len(re.findall(r"^###\s+\d+[.\uff0e、)]\s+", block, re.MULTILINE))
    if heading_count:
        return heading_count
    return len(re.findall(r"^\s*\d+[.\uff0e、)]\s+\S+", block, re.MULTILINE))


def ranked_sections(block: str) -> list[tuple[int, str]]:
    pattern = re.compile(r"^###\s+(\d+)[.\uff0e、)]\s+.*$", re.MULTILINE)
    matches = list(pattern.finditer(block))
    sections: list[tuple[int, str]] = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(block)
        sections.append((int(match.group(1)), block[start:end]))
    return sections


def citation_rows(block: str) -> list[str]:
    rows = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped or "ref_id" in stripped:
            continue
        if "http://" in stripped or "https://" in stripped:
            rows.append(stripped)
    return rows


def contains_placeholder(text: str) -> bool:
    placeholders = ["<topic>", "<热点标题>", "<选题标题>", "<source_id>", "<reason>", "YYYY-MM-DD", "..."]
    return any(item in text for item in placeholders)


def validate_report(text: str, allow_template: bool = False) -> tuple[list[str], dict[str, object]]:
    errors: list[str] = []
    missing_sections = [section for section in REQUIRED_SECTIONS if not section_text(text, section)]
    for section in missing_sections:
        errors.append(f"Missing required section: {section}")

    top_block = section_text(text, "热点 Top 10")
    idea_block = section_text(text, "自媒体选题 Top 5")
    overview_block = section_text(text, "数据来源概览")
    citations_block = section_text(text, "引用与来源表")

    top_count = count_ranked_entries(top_block)
    idea_count = count_ranked_entries(idea_block)
    citations = citation_rows(citations_block)
    hotspot_sections = ranked_sections(top_block)
    idea_sections = ranked_sections(idea_block)

    if not allow_template:
        if contains_placeholder(text):
            errors.append("Report still contains template placeholders.")
        if top_count < 10:
            errors.append(f"热点 Top 10 has {top_count} ranked entries; expected at least 10.")
        if idea_count < 5:
            errors.append(f"自媒体选题 Top 5 has {idea_count} ranked entries; expected at least 5.")
        if len(citations) < 10:
            errors.append(f"引用与来源表 has {len(citations)} URL citation rows; expected at least 10.")
        for label in OVERVIEW_METRICS:
            if label not in overview_block:
                errors.append(f"数据来源概览 missing metric: {label}")
        for label in SOURCE_SHARE_LABELS:
            if not re.search(rf"{re.escape(label)}[：:]\s*\d+(?:\.\d+)?%", overview_block):
                errors.append(f"来源占比 missing percentage for: {label}")
        for number, entry in hotspot_sections[:10]:
            for field in HOTSPOT_FIELDS:
                if f"{field}：" not in entry and f"{field}:" not in entry:
                    errors.append(f"热点 {number} missing field: {field}")
            if "http://" not in entry and "https://" not in entry:
                errors.append(f"热点 {number} missing URL in source fields.")
            if not re.search(r"\d{4}-\d{2}-\d{2}", entry):
                errors.append(f"热点 {number} missing concrete capture date.")
        for number, entry in idea_sections[:5]:
            for field in IDEA_FIELDS:
                if f"{field}：" not in entry and f"{field}:" not in entry:
                    errors.append(f"选题 {number} missing field: {field}")

    summary = {
        "top_count": top_count,
        "idea_count": idea_count,
        "citation_rows": len(citations),
        "hotspot_sections": len(hotspot_sections),
        "idea_sections": len(idea_sections),
        "missing_sections": missing_sections,
        "template_mode": allow_template,
    }
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="Path to an AI-HOTDog report markdown file")
    parser.add_argument("--allow-template", action="store_true", help="Only check that required template sections exist")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    text = args.report.read_text(encoding="utf-8")
    errors, summary = validate_report(text, allow_template=args.allow_template)

    if args.format == "json":
        print(json.dumps({"ok": not errors, "errors": errors, "summary": summary}, ensure_ascii=False, indent=2))
    else:
        if errors:
            print("Report integrity check failed:")
            for error in errors:
                print(f"- {error}")
        else:
            print("Report integrity check passed.")
        print(
            f"Top entries: {summary['top_count']}; "
            f"Ideas: {summary['idea_count']}; "
            f"Citation rows: {summary['citation_rows']}"
        )

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
