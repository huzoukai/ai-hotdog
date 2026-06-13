# AI-HOTDog

Configurable hot-topic radar for Codex. Turn media, search, social discussion, and vertical communities into cited content ideas.

[中文说明](./README.md)

[![Skill](https://img.shields.io/badge/Codex-Skill-black)](./SKILL.md)
[![Version](https://img.shields.io/badge/version-v0.1.2-blue)](https://github.com/huzoukai/ai-hotdog/releases)
[![Self Check](https://img.shields.io/badge/self--check-passing-brightgreen)](./scripts/self_check.py)

AI-HOTDog is a Codex Skill that helps you build a repeatable hotspot workflow: choose a topic, define sources, check account access, scan public and login-state platforms, and generate a Top 10 hotspot report with Top 5 content ideas.

The default profile monitors AI news, models, tools, open-source projects, papers, and Chinese AI discussion. The underlying workflow is topic-agnostic, so it can also track finance, education, food service, gaming, real estate, parenting, or a custom niche.

## Why This Exists

Most trend workflows fail in the same place: sources get messy. AI-HOTDog makes the source layer explicit.

- Every selected source has an id, type, region, access mode, priority, required signal, and failure policy.
- Every report must show source counts, candidate counts, scored counts, cited counts, and source-share percentages.
- Login-state platforms are treated as supplemental discussion signals unless they point to an official or original source.
- Blocked platforms are disclosed instead of silently skipped.

## What It Produces

Each report follows this structure:

```text
# AI-HOTDog 热点选题报告

## 今日结论
## 数据来源概览
## 热点 Top 10
## 细分观察
## 自媒体选题 Top 5
## 今日最推荐选题
## 平台访问状态
## 引用与来源表
```

Each hotspot must include:

```text
标题
一句话摘要
为什么重要
分类
热度评分
可信度评分
选题价值评分
主要事实来源
讨论热度来源
抓取时间
置信度
```

## Install

Clone the skill into your Codex skills folder:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/huzoukai/ai-hotdog.git ~/.codex/skills/ai-hotdog
```

Restart Codex so the skill metadata is picked up.

You can then invoke it with:

```text
Use $ai-hotdog to initialize an AI hotspot radar.
```

## Quick Start

Initialize the default AI profile in a workspace:

```bash
~/.codex/skills/ai-hotdog/scripts/init_ai_hotdog.py \
  --workspace /path/to/workspace \
  --topic "AI" \
  --profile ai \
  --core-keywords "AI,large models,AI tools,AI startups"
```

This creates non-secret workspace state:

```text
.ai-hotdog/
├── config.json
├── source-status.json
└── reports/
```

Then ask Codex:

```text
Use $ai-hotdog to generate today's AI-HOTDog hotspot report.
```

## Common Commands

```text
初始化 AI-HOTDog
```

Create or update the topic configuration.

```text
绑定 AI-HOTDog 账号
```

Open selected login-state platforms in Chrome so the user can manually log in or handle verification. The skill checks visible access state after the user finishes.

```text
重新绑定 AI-HOTDog 账号：X
```

Recheck a single blocked platform without changing other platform states.

```text
生成今日 AI-HOTDog 热点报告
```

Run the configured radar and generate a cited report.

```text
创建 AI-HOTDog 每日自动化
```

Create a Codex automation that runs the existing configuration on a schedule. Automations do not enter credentials or perform first-time login.

## Source Strategy

AI-HOTDog ships with 59 default sources across:

- official/original sources
- news and search
- social discussion
- video platforms
- code/project platforms
- papers/research
- product/startup platforms
- Chinese internet sources

The default AI source pack includes OpenAI, Anthropic, Google DeepMind, Meta AI, Microsoft AI, NVIDIA, xAI, Mistral, Hugging Face, GitHub, arXiv, Papers with Code, Semantic Scholar, OpenReview, Machine Heart, QbitAI, InfoQ China, and other public sources.

See [references/source-registry.md](./references/source-registry.md) for the full registry.

## Account Access Model

AI-HOTDog can use Chrome login state for platforms such as X, YouTube, Zhihu, Weibo, Bilibili, Xiaohongshu, Reddit, and LinkedIn.

It does not:

- save usernames or passwords
- read cookies, local storage, session storage, saved passwords, or raw tokens
- bypass CAPTCHA, paywalls, risk-control flows, or platform restrictions
- post, like, comment, follow, subscribe, message, upload, or change account settings

When a platform is blocked, the report lists it under `需要重新绑定的平台`.

See [references/login-and-access.md](./references/login-and-access.md).

## Quality Checks

Run the full publish-readiness check:

```bash
~/.codex/skills/ai-hotdog/scripts/self_check.py
```

Run individual checks:

```bash
~/.codex/skills/ai-hotdog/scripts/validate_source_registry.py \
  ~/.codex/skills/ai-hotdog/references/source-registry.md

~/.codex/skills/ai-hotdog/scripts/check_report_integrity.py \
  /path/to/report.md
```

The report checker verifies required sections, Top 10 count, Top 5 count, source-share percentages, citation rows, per-hotspot fields, and placeholder leakage.

## Repository Layout

```text
ai-hotdog/
├── SKILL.md                         # Skill trigger metadata and workflow router
├── README.md                        # Chinese README
├── README.en.md                     # English README
├── agents/
│   └── openai.yaml                  # Codex UI metadata
├── references/
│   ├── config-schema.md             # Workspace state schema
│   ├── login-and-access.md          # Login/rebinding rules
│   ├── report-template.md           # Report format and strict rules
│   └── source-registry.md           # Default source registry
└── scripts/
    ├── check_report_integrity.py    # Report quality gate
    ├── init_ai_hotdog.py            # Workspace initializer
    ├── self_check.py                # Publish-readiness check
    └── validate_source_registry.py  # Source registry validator
```

## Design Notes

AI-HOTDog follows common agent-skill packaging patterns:

- `SKILL.md` stays lean and routing-oriented.
- `references/` holds detailed policies and templates.
- `scripts/` contains deterministic checks and setup helpers.
- `agents/openai.yaml` provides Codex-specific UI metadata.

This keeps the runtime skill focused while still giving GitHub readers enough context to evaluate, install, and extend it.

## Roadmap

- Add optional vertical source packs for finance, education, food service, gaming, and real estate.
- Add sample generated reports under `examples/`.
- Add CI for `scripts/self_check.py`.
- Add a license after the reuse policy is decided.

## License

No license has been selected yet. Until a license is added, all rights are reserved by default.
