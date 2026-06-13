---
name: ai-hotdog
description: Configurable hot-topic and content-idea radar for AI-HOTDog. Use when Codex needs to initialize a user-selected topic radar, bind or rebind logged-in platform access through Chrome, scan public and social/media sources for trending topics, generate a cited Top 10 hotspot report with Top 5 content ideas, or create a Codex automation that runs the configured radar on a schedule.
---

# AI-HOTDog

AI-HOTDog is a configurable hotspot radar for turning media, search, social discussion, and vertical communities into cited content ideas. AI is the default profile, but the workflow must support any user-selected domain such as finance, education, food service, real estate, gaming, parenting, or a custom topic.

## Operating Principles

- Treat the user's chosen topic as configuration, not as hardcoded AI coverage.
- Prefer stable public sources for the main evidence chain. Use Chrome or Computer Use login-state platforms only as supplemental discussion signals unless a source is an official/original page.
- Never save passwords, OTPs, cookies, local storage, session stores, or browser profile data.
- When login, CAPTCHA, risk control, payment wall, or permission prompts block access, hand off to the user and mark the platform status. Do not bypass restrictions.
- Do not put any item into `热点 Top 10` unless it has a primary source URL, source type, capture time, and confidence label.
- Do not use social discussion as the only evidence for a major factual claim. Pair it with an official, original, media, code, paper, or search/news source.
- Every report must show scanned source counts, usable source counts, candidate counts, scored counts, final cited counts, and source-share percentages.

## Command Router

### 初始化 AI-HOTDog

Create or update the workspace radar configuration. Default state directory: `.ai-hotdog/` in the current workspace unless the user provides another path.

Ask for missing high-impact configuration in a compact way:

- `focus_topic`: topic/domain to monitor. Default to the AI profile only when the user asks for AI or accepts the default.
- `core_keywords`: required search terms.
- `exclude_keywords`: terms to filter out.
- `entity_keywords`: brands, companies, people, products, or communities to track.
- `regions`: global, China, or specific countries/regions.
- `content_goal`: content ideas, industry intelligence, product opportunities, competitor monitoring, or custom.
- `platform_scope`: stable public sources, login-state platforms, or both.
- `frequency`: manual, daily, or weekly.
- `output_language`: default to the user's language.

Use `references/source-registry.md` to build the default source set and source mix buckets. Save only non-secret configuration, source choices, and status metadata.

For deterministic setup, run:

```bash
python3 scripts/init_ai_hotdog.py --workspace <workspace> --topic "<topic>" --profile ai --core-keywords "<keywords>"
```

Read `references/config-schema.md` before creating or editing `.ai-hotdog/config.json` or `.ai-hotdog/source-status.json`.

### 绑定 AI-HOTDog 账号

Use this when the user wants to connect logged-in platforms such as X, YouTube, Zhihu, Weibo, Bilibili, Xiaohongshu, Reddit, or LinkedIn.

Read `references/login-and-access.md` before using browser tools. Open each requested platform in Chrome, let the user perform login or verification, then check whether the platform can search, open result details, and expose usable public URLs or visible titles. Record the platform status in `.ai-hotdog/source-status.json` or the user's configured status file.

### 重新绑定 AI-HOTDog 账号

Use this when a platform is `login_required`, `manual_required`, `limited`, or `unavailable`. If the user names a platform, only rebind that platform. If they do not, list the blocked platforms and ask which one to rebind.

Do not change unrelated platform statuses except for a timestamped recheck if the user asks for a full health check.

### 生成今日 AI-HOTDog 热点报告

Run the configured radar:

1. Load the workspace configuration and source status.
2. Recheck stable public sources first.
3. Use accessible login-state platforms for discussion signals.
4. Collect candidates with title, URL, source id, source type, region, capture time, and matched keywords.
5. Score candidates for freshness, credibility, discussion, impact, and content value.
6. Deduplicate related reports into coherent hotspot clusters.
7. Generate `热点 Top 10`, `自媒体选题 Top 5`, one strongest recommendation, platform status, source-share stats, and a citation table.

Read `references/report-template.md` before writing the report. Run `scripts/check_report_integrity.py` on saved reports when a file is produced.

### 创建 AI-HOTDog 每日自动化

When the user asks for a recurring run, use the Codex automation tool if available. The automation prompt must describe only the task, not the schedule:

```text
Use $ai-hotdog to load the existing AI-HOTDog configuration in this workspace, generate today's cited hotspot report, include source-share statistics, Top 10 hotspots, Top 5 content ideas, platform access status, and any platforms that need rebinding.
```

The automation job must not perform first-time login or enter credentials. If a platform loses access during an unattended run, the report must list it under `需要重新绑定的平台`.

## Data Quality Gate

Before considering a report complete, confirm all of the following:

- `数据来源概览` includes scanned platforms, successful platforms, limited/blocked platforms, total candidates, scored candidates, final cited items, and source-share percentages.
- `热点 Top 10` contains exactly 10 ranked items unless the report explicitly says that strict citations left fewer than 10 valid items.
- `自媒体选题 Top 5` contains 5 ideas, each with a title, core point, platform fit, hook, structure, source material, and risk note.
- Each hotspot has a primary fact source, optional discussion sources, capture time, and confidence label.
- Every citation in `引用与来源表` maps to a visible hotspot, content idea, or source-status note.
- Any failed or limited source is disclosed in `平台访问状态` and never silently omitted from the source count.

## Resource Routing

- Read `references/source-registry.md` during initialization, source customization, source-share calculation, or source-list debugging.
- Read `references/config-schema.md` before creating, editing, or troubleshooting workspace state.
- Read `references/login-and-access.md` before binding, rebinding, browser checks, or explaining account-access limits.
- Read `references/report-template.md` before generating or revising a report.
- Use `scripts/init_ai_hotdog.py --workspace <workspace> ...` to create deterministic non-secret workspace state.
- Use `scripts/validate_source_registry.py <source-registry.md>` after editing a source registry.
- Use `scripts/check_report_integrity.py <report.md>` before treating a saved report as finished.
- Use `scripts/self_check.py` before publishing the skill package.

## Default AI Profile

If the user wants the default AI setup, initialize:

- `focus_topic`: AI, large models, AI tools, AI startups, AI content opportunities.
- `regions`: global and China.
- `content_goal`: content ideas.
- `report_target`: Top 10 AI hotspots and Top 5 content ideas.
- `source_strategy`: stable public sources first, login-state sources as supplemental discussion signals.
- `strict_citation`: true.
