# AI-HOTDog Report Template

Use this template for daily or weekly hotspot reports. Keep the report short enough to read, but strict enough to audit.

```markdown
# AI-HOTDog 热点选题报告

生成时间：YYYY-MM-DD HH:mm
配置主题：<topic>
地区范围：<global/china/custom>
内容目标：<自媒体选题/行业情报/产品机会/竞品监控>

## 今日结论

- 今天最值得关注的变化：...
- 今天更像重大新闻的方向：...
- 今天更像社交热度的方向：...
- 今日最适合做内容的角度：...

## 数据来源概览

本次扫描：
- 配置主题：<topic>
- 扫描平台：N 个
- 成功访问：N 个
- 访问受限：N 个
- 总候选内容：N 条
- 进入评分池：N 条
- 最终引用内容：N 条

来源占比：
- 官方/原始发布：X%
- 新闻媒体：X%
- 社交讨论：X%
- 视频平台：X%
- 开源/项目平台：X%
- 论文/研究：X%
- 产品/创业：X%
- 中文互联网：X%

## 热点 Top 10

### 1. <热点标题>

- 一句话摘要：...
- 为什么重要：...
- 分类：模型 / 产品 / 公司 / 论文 / 开源 / 政策 / 投融资 / 社交讨论 / 其他
- 热度评分：1-5
- 可信度评分：1-5
- 选题价值评分：1-5
- 主要事实来源：<source_id> - <url>
- 讨论热度来源：<source_id> - <url or 未使用>
- 抓取时间：YYYY-MM-DD HH:mm
- 置信度：high / medium / low

## 细分观察

- 全球观察：...
- 中国观察：...
- 工具/项目/模型/论文观察：...
- 只是热闹但不宜放大的话题：...

## 自媒体选题 Top 5

### 1. <选题标题>

- 核心观点：...
- 适合平台：视频号 / 小红书 / B站 / 抖音 / 公众号 / LinkedIn / X
- 开头钩子：...
- 内容结构：开头 -> 事实 -> 为什么重要 -> 普通人/行业影响 -> 结尾行动
- 可引用素材：热点 1、热点 3、来源 <source_id>
- 风险提醒：事实未确认 / 数据不足 / 争议较大 / 平台热度偏差 / 无明显风险

## 今日最推荐选题

- 标题：...
- 推荐原因：...
- 30 秒口播结构：...
- 必须引用的来源：...
- 不要夸大的地方：...

## 平台访问状态

| source_id | status | checked_at | usable_signals | notes |
| --- | --- | --- | --- | --- |
| example_source | available | YYYY-MM-DD HH:mm | search;detail | ok |

需要重新绑定的平台：
- <source_id>：<reason>

## 引用与来源表

| ref_id | used_in | source_id | source_type | region | title | url | captured_at | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | 热点 1 | openai_blog | official | global | Example title | https://example.com | YYYY-MM-DD HH:mm | high |
```

## Strict Report Rules

- Use exactly 10 hotspot entries unless there are fewer than 10 strictly cited candidates. If fewer, state the reason in `今日结论`.
- Use exactly 5 content ideas.
- Each Top 10 item must include `一句话摘要`, `为什么重要`, `分类`, `热度评分`, `可信度评分`, `选题价值评分`, `主要事实来源`, `讨论热度来源`, `抓取时间`, and `置信度`.
- Each Top 5 idea must include `核心观点`, `适合平台`, `开头钩子`, `内容结构`, `可引用素材`, and `风险提醒`.
- Do not list a social-only rumor as a factual hotspot.
- Add source ids consistently so the reader can trace each claim.
- Mark platform failures in `平台访问状态` and include them in the source count.
- If a claim depends on a source that may have changed after capture, say so.
