#!/usr/bin/env python3
"""Run AI-HOTDog publish-readiness checks."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SKILLS_ROOT = SKILL_DIR.parent
QUICK_VALIDATE = SKILLS_ROOT / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
REGISTRY = SKILL_DIR / "references" / "source-registry.md"
TEMPLATE = SKILL_DIR / "references" / "report-template.md"


def run(cmd: list[str], expect_ok: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if expect_ok and result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)
    if not expect_ok and result.returncode == 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit("Command unexpectedly succeeded.")
    return result


def sample_report() -> str:
    overview = """# AI-HOTDog 热点选题报告

生成时间：2026-06-13 09:00
配置主题：AI
地区范围：global, china
内容目标：自媒体选题

## 今日结论

- 今天最值得关注的变化：AI 工具链继续产品化。
- 今天更像重大新闻的方向：官方发布与开源项目更新。
- 今天更像社交热度的方向：视频平台上的工具体验讨论。
- 今日最适合做内容的角度：普通人如何筛选 AI 工具。

## 数据来源概览

本次扫描：
- 配置主题：AI
- 扫描平台：20 个
- 成功访问：18 个
- 访问受限：2 个
- 总候选内容：120 条
- 进入评分池：42 条
- 最终引用内容：15 条

来源占比：
- 官方/原始发布：20%
- 新闻媒体：20%
- 社交讨论：15%
- 视频平台：10%
- 开源/项目平台：15%
- 论文/研究：10%
- 产品/创业：5%
- 中文互联网：5%

## 热点 Top 10
"""
    hotspots = []
    for i in range(1, 11):
        hotspots.append(
            f"""### {i}. 示例热点 {i}

- 一句话摘要：这是第 {i} 条带引用的示例热点。
- 为什么重要：它展示了报告质量门需要的字段。
- 分类：产品
- 热度评分：4
- 可信度评分：5
- 选题价值评分：4
- 主要事实来源：openai_blog - https://example.com/source-{i}
- 讨论热度来源：youtube - https://example.com/discussion-{i}
- 抓取时间：2026-06-13 09:{i:02d}
- 置信度：high
"""
        )
    ideas_header = """
## 细分观察

- 全球观察：官方源贡献了主要事实。
- 中国观察：中文互联网贡献了区域讨论。
- 工具/项目/模型/论文观察：开源项目值得单独跟踪。
- 只是热闹但不宜放大的话题：缺少事实来源的社交传言。

## 自媒体选题 Top 5
"""
    ideas = []
    for i in range(1, 6):
        ideas.append(
            f"""### {i}. 示例选题 {i}

- 核心观点：把热点 {i} 转成普通人能理解的问题。
- 适合平台：视频号
- 开头钩子：今天 AI 圈最值得普通人关注的一件事。
- 内容结构：开头 -> 事实 -> 为什么重要 -> 普通人影响 -> 行动建议
- 可引用素材：热点 {i}，来源 R{i}
- 风险提醒：无明显风险
"""
        )
    footer = """
## 今日最推荐选题

- 标题：普通人如何筛选 AI 工具
- 推荐原因：事实来源清楚，表达门槛低。
- 30 秒口播结构：问题 -> 例子 -> 判断标准 -> 行动。
- 必须引用的来源：R1, R2
- 不要夸大的地方：不要声称趋势已经覆盖所有行业。

## 平台访问状态

| source_id | status | checked_at | usable_signals | notes |
| --- | --- | --- | --- | --- |
| openai_blog | available | 2026-06-13 09:00 | posts;dates | ok |

需要重新绑定的平台：
- x_twitter：login_required

## 引用与来源表

| ref_id | used_in | source_id | source_type | region | title | url | captured_at | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
"""
    refs = []
    for i in range(1, 11):
        refs.append(
            f"| R{i} | 热点 {i} | openai_blog | official | global | 示例来源 {i} | https://example.com/source-{i} | 2026-06-13 09:{i:02d} | high |"
        )
    return overview + "\n".join(hotspots) + ideas_header + "\n".join(ideas) + footer + "\n".join(refs) + "\n"


def main() -> int:
    python = sys.executable
    run([python, str(QUICK_VALIDATE), str(SKILL_DIR)])
    run([python, str(SCRIPT_DIR / "validate_source_registry.py"), str(REGISTRY)])
    run([python, str(SCRIPT_DIR / "check_report_integrity.py"), str(TEMPLATE), "--allow-template"])

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        run(
            [
                python,
                str(SCRIPT_DIR / "init_ai_hotdog.py"),
                "--workspace",
                str(tmp_path),
                "--topic",
                "AI",
                "--profile",
                "ai",
                "--core-keywords",
                "AI,large models,AI tools",
            ]
        )
        config = json.loads((tmp_path / ".ai-hotdog" / "config.json").read_text(encoding="utf-8"))
        status = json.loads((tmp_path / ".ai-hotdog" / "source-status.json").read_text(encoding="utf-8"))
        if config["report_targets"] != {"hotspots": 10, "content_ideas": 5}:
            raise SystemExit("Config report_targets are incorrect.")
        if config["automation_action"] != "daily_hotspot_report":
            raise SystemExit("Config automation_action is incorrect.")
        if config["auth_policy"] != "prompt_each_run":
            raise SystemExit("Config auth_policy is incorrect.")
        if not config["login_sources"]:
            raise SystemExit("Config login_sources should include default login-state sources.")
        if not status["sources"]:
            raise SystemExit("No sources were initialized.")
        login_statuses = [item for item in status["sources"].values() if item.get("auth_required")]
        if not login_statuses:
            raise SystemExit("No auth_required sources were initialized.")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        run(
            [
                python,
                str(SCRIPT_DIR / "init_ai_hotdog.py"),
                "--workspace",
                str(tmp_path),
                "--topic",
                "餐饮",
                "--profile",
                "general",
                "--core-keywords",
                "餐饮,咖啡,开店",
                "--content-goal",
                "industry_intelligence",
                "--automation-action",
                "industry_brief",
                "--platform-scope",
                "stable_public",
                "--auth-policy",
                "public_only",
            ]
        )
        config = json.loads((tmp_path / ".ai-hotdog" / "config.json").read_text(encoding="utf-8"))
        status = json.loads((tmp_path / ".ai-hotdog" / "source-status.json").read_text(encoding="utf-8"))
        if config["focus_topic"] != "餐饮":
            raise SystemExit("Non-AI topic initialization failed.")
        if config["automation_action"] != "industry_brief":
            raise SystemExit("Non-AI automation_action was not preserved.")
        if config["auth_policy"] != "public_only":
            raise SystemExit("Public-only auth_policy is incorrect.")
        if config["login_sources"]:
            raise SystemExit("Public-only initialization should not keep login_sources.")
        if any(item.get("auth_required") for item in status["sources"].values()):
            raise SystemExit("Public-only initialization should not mark auth_required sources.")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        run(
            [
                python,
                str(SCRIPT_DIR / "init_ai_hotdog.py"),
                "--workspace",
                str(tmp_path),
                "--topic",
                "AI",
                "--profile",
                "ai",
                "--core-keywords",
                "AI,large models",
                "--login-sources",
                "x_twitter,youtube",
            ]
        )
        config = json.loads((tmp_path / ".ai-hotdog" / "config.json").read_text(encoding="utf-8"))
        if config["login_sources"] != ["x_twitter", "youtube"]:
            raise SystemExit("Explicit login_sources were not preserved.")

        report = tmp_path / "valid-report.md"
        report.write_text(sample_report(), encoding="utf-8")
        run([python, str(SCRIPT_DIR / "check_report_integrity.py"), str(report)])

        invalid_report = tmp_path / "invalid-report.md"
        invalid_report.write_text("# AI-HOTDog 热点选题报告\n\n## 今日结论\n\n- Missing everything else.\n", encoding="utf-8")
        run([python, str(SCRIPT_DIR / "check_report_integrity.py"), str(invalid_report)], expect_ok=False)

    print("AI-HOTDog self-check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
