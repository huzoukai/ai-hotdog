# AI-HOTDog

面向 Codex 的可配置热点选题雷达。把媒体、搜索、社交讨论和垂直社区里的信息，整理成带引用、可复盘、可直接用于内容创作的选题报告。

[English](./README.en.md)

[![Skill](https://img.shields.io/badge/Codex-Skill-black)](./SKILL.md)
[![Version](https://img.shields.io/badge/version-v0.1.2-blue)](https://github.com/huzoukai/ai-hotdog/releases)
[![Self Check](https://img.shields.io/badge/self--check-passing-brightgreen)](./scripts/self_check.py)

AI-HOTDog 是一个 Codex Skill。它的目标不是“让 AI 随便搜一圈”，而是帮你搭建一套可长期运行的信息工作流：选择关注主题、定义数据源、检查账号登录状态、扫描公开平台和登录态平台，然后生成一份 `热点 Top 10 + 自媒体选题 Top 5` 的报告。

默认配置关注 AI 新闻、大模型、AI 工具、开源项目、论文和中文互联网讨论。但它本质上不是只服务 AI，你也可以用它追踪财经、教育、餐饮、游戏、房产、母婴或任何自定义领域。

## 为什么做这个

很多热点追踪工作流真正容易乱的地方，不是“能不能总结”，而是“数据源从哪里来、哪些可信、哪些只是热闹”。

AI-HOTDog 把数据源层显式管理起来：

- 每个数据源都有 `source_id`、类型、地区、访问方式、优先级、必需信号和失败处理规则。
- 每份报告必须展示扫描平台数、候选内容数、进入评分池数量、最终引用数量和来源占比。
- X、YouTube、知乎、微博等登录态平台默认只作为讨论热度补充，不能单独支撑重大事实判断。
- 登录失败、验证码、风控、平台受限不会被悄悄跳过，而是写入平台访问状态。

## 最终输出

每份报告使用固定结构：

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

每条热点必须包含：

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

每个选题必须包含：

```text
选题标题
核心观点
适合平台
开头钩子
内容结构
可引用素材
风险提醒
```

## 安装

把 Skill 克隆到 Codex 的 skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/huzoukai/ai-hotdog.git ~/.codex/skills/ai-hotdog
```

然后重启 Codex，让它重新加载 Skill 元数据。

之后可以这样调用：

```text
使用 $ai-hotdog 初始化 AI-HOTDog
```

## 快速开始

在某个工作区初始化默认 AI 主题：

```bash
~/.codex/skills/ai-hotdog/scripts/init_ai_hotdog.py \
  --workspace /path/to/workspace \
  --topic "AI" \
  --profile ai \
  --core-keywords "AI,large models,AI tools,AI startups"
```

这会创建一份不含账号密码和敏感凭据的工作区状态：

```text
.ai-hotdog/
├── config.json
├── source-status.json
└── reports/
```

然后对 Codex 说：

```text
使用 $ai-hotdog 生成今日 AI-HOTDog 热点报告
```

## 常用指令

```text
初始化 AI-HOTDog
```

创建或更新关注主题、关键词、地区、平台范围和报告目标。

```text
绑定 AI-HOTDog 账号
```

用 Chrome 打开需要登录的平台，让用户自己完成登录、验证码或权限确认。AI-HOTDog 只检查页面是否能搜索、打开结果、读取公开可见信息。

```text
重新绑定 AI-HOTDog 账号：X
```

只重新检查一个失效平台，不影响其他平台状态。

```text
生成今日 AI-HOTDog 热点报告
```

基于当前配置执行扫描、评分、归类、引用校验和报告生成。

```text
创建 AI-HOTDog 每日自动化
```

创建 Codex 自动化，让它每天定时运行已初始化的配置。自动化不会输入账号密码，也不会处理首次登录。

## 数据源策略

AI-HOTDog 当前内置 59 个默认数据源，覆盖：

- 官方/原始发布
- 新闻媒体与搜索
- 社交讨论
- 视频平台
- 代码/项目平台
- 论文/研究
- 产品/创业平台
- 中文互联网来源

默认 AI 数据源包含 OpenAI、Anthropic、Google DeepMind、Meta AI、Microsoft AI、NVIDIA、xAI、Mistral、Hugging Face、GitHub、arXiv、Papers with Code、Semantic Scholar、OpenReview、机器之心、量子位、InfoQ 中文等公开来源。

完整数据源清单见 [references/source-registry.md](./references/source-registry.md)。

## 账号登录模型

AI-HOTDog 可以借助 Chrome 的已登录状态读取 X、YouTube、知乎、微博、B站、小红书、Reddit、LinkedIn 等平台的公开可见信息。

它不会：

- 保存用户名或密码
- 读取 cookies、local storage、session storage、已保存密码或原始 token
- 绕过验证码、付费墙、风控流程或平台限制
- 发帖、点赞、评论、关注、订阅、私信、上传文件或修改账号设置

如果某个平台登录失效或访问受限，报告会把它列在 `需要重新绑定的平台` 中。

详细规则见 [references/login-and-access.md](./references/login-and-access.md)。

## 质量检查

运行完整发布前自检：

```bash
~/.codex/skills/ai-hotdog/scripts/self_check.py
```

单独检查数据源清单：

```bash
~/.codex/skills/ai-hotdog/scripts/validate_source_registry.py \
  ~/.codex/skills/ai-hotdog/references/source-registry.md
```

单独检查报告完整性：

```bash
~/.codex/skills/ai-hotdog/scripts/check_report_integrity.py \
  /path/to/report.md
```

报告检查会验证必需章节、Top 10 数量、Top 5 数量、来源占比、引用表、每条热点字段和模板占位符泄漏。

## 目录结构

```text
ai-hotdog/
├── SKILL.md                         # Skill 触发描述和流程路由
├── README.md                        # 中文说明
├── README.en.md                     # English README
├── agents/
│   └── openai.yaml                  # Codex UI 元数据
├── references/
│   ├── config-schema.md             # 工作区状态结构
│   ├── login-and-access.md          # 登录、绑定、重新绑定规则
│   ├── report-template.md           # 报告模板和严格规则
│   └── source-registry.md           # 默认数据源清单
└── scripts/
    ├── check_report_integrity.py    # 报告质量门
    ├── init_ai_hotdog.py            # 工作区初始化脚本
    ├── self_check.py                # 发布前自检
    └── validate_source_registry.py  # 数据源清单校验
```

## 设计原则

AI-HOTDog 使用常见的 agent skill 包装方式：

- `SKILL.md` 保持简洁，只负责触发、路由和关键原则。
- `references/` 存放详细规则、模板和数据源说明。
- `scripts/` 存放可重复运行的初始化和校验逻辑。
- `agents/openai.yaml` 提供 Codex UI 元数据。

这样做的目的，是让 Codex 运行时不会被过多说明文档拖慢，同时让 GitHub 读者能清楚理解、安装、验证和扩展这个 Skill。

## 路线图

- 增加财经、教育、餐饮、游戏、房产等垂直领域数据源包。
- 增加 `examples/` 示例报告。
- 增加 GitHub Actions，自动运行 `scripts/self_check.py`。
- 确定开源许可证。

## 许可证

暂未选择开源许可证。添加许可证之前，默认保留所有权利。
