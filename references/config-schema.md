# AI-HOTDog Config Schema

Use this reference when initializing or troubleshooting `.ai-hotdog/` workspace state. Store only non-secret configuration and source status. Never store passwords, OTPs, cookies, browser storage, tokens, or personal account identifiers.

## Workspace Layout

```text
.ai-hotdog/
├── config.json
├── source-status.json
└── reports/
```

## config.json

Required fields:

```json
{
  "schema_version": 1,
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "display_name": "AI-HOTDog",
  "focus_topic": "AI",
  "profile": "ai",
  "core_keywords": ["AI", "large models"],
  "exclude_keywords": [],
  "entity_keywords": [],
  "regions": ["global", "china"],
  "content_goal": "content_ideas",
  "platform_scope": "login_supplement",
  "frequency": "manual",
  "output_language": "zh-CN",
  "strict_citation": true,
  "report_targets": {
    "hotspots": 10,
    "content_ideas": 5
  },
  "selected_sources": ["google_news", "openai_blog"],
  "source_registry_path": "references/source-registry.md"
}
```

Allowed values:

| field | allowed values |
| --- | --- |
| profile | `ai`, `general`, `custom` |
| regions | `global`, `china`, `both`, custom region labels |
| content_goal | `content_ideas`, `industry_intelligence`, `product_opportunities`, `competitor_monitoring`, `custom` |
| platform_scope | `stable_public`, `login_supplement`, `all` |
| frequency | `manual`, `daily`, `weekly` |

## source-status.json

Required shape:

```json
{
  "schema_version": 1,
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "sources": {
    "google_news": {
      "status": "unchecked",
      "last_checked_at": null,
      "checked_by": "init",
      "access_mode": "public",
      "priority": "secondary",
      "evidence_url": "https://news.google.com/search?q=AI",
      "usable_signals": [],
      "notes": "Initialized from source registry."
    }
  }
}
```

Allowed status values:

| status | meaning |
| --- | --- |
| unchecked | Source selected but not checked in this workspace yet. |
| available | Source can search and open usable result details. |
| login_required | Platform is reachable but asks for login. |
| manual_required | CAPTCHA, risk control, paywall, or permission step blocks access. |
| limited | Some content can be read, but signals are incomplete. |
| unavailable | Platform cannot be reached or fails repeatedly. |
| disabled | Source exists in the registry but is not selected for this workspace. |

## Initialization Defaults

- `profile=ai` selects general stable sources plus the default AI vertical sources.
- `profile=general` selects general stable sources only.
- `profile=custom` selects general stable sources, then expects the user to add vertical sources or custom source ids.
- `platform_scope=stable_public` selects only `access_mode=public`.
- `platform_scope=login_supplement` selects `public`, `chrome_login`, and `manual`; login-state sources start as `login_required` or `manual_required`.
- `platform_scope=all` selects every registry source.

## Automation Contract

Recurring automations should load `config.json` and `source-status.json`, then generate a report. They must not perform first-time login or credential entry. If a selected login-state source is not `available` or `limited`, add it to `需要重新绑定的平台` and continue with stable sources.
