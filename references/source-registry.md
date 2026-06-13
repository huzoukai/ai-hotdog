# AI-HOTDog Source Registry

Use this reference to initialize or revise an AI-HOTDog data source list. Keep the registry explicit: every source must have a stable id, source type, access mode, priority, expected signal, and failure policy.

## Required Fields

| field | allowed values | meaning |
| --- | --- | --- |
| source_id | lowercase id | Stable unique id used in reports and status files. |
| name | text | Reader-facing source name. |
| region | global, china, both, custom | Geographic focus. |
| type | official, code, paper, media, search, social, video, product, appstore, government, community | Source category used for source-share stats. |
| access_mode | public, chrome_login, manual | Whether the source should work publicly or needs user login/manual handling. |
| priority | primary, secondary, supplemental | Whether it can be a main fact source or only a supporting signal. |
| url_or_query | URL or query template | Use `{keywords}` for configurable searches. |
| required_signals | semicolon list | What must be visible for the source to count as usable. |
| failure_policy | skip, manual_required, limited_note | How to handle failures in reports. |

## Source-Share Buckets

Use these buckets in every report:

| bucket | includes |
| --- | --- |
| official_original | `official`, `government`, direct company/product release pages |
| news_media | `media`, `search` when pointing to news results |
| social_discussion | `social`, `community` discussion feeds |
| video_platform | `video` |
| code_project | `code` |
| paper_research | `paper` |
| product_startup | `product`, `appstore` |
| chinese_internet | any `region=china` source, counted separately as regional share |

## General Stable Sources

| source_id | name | region | type | access_mode | priority | url_or_query | required_signals | failure_policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| google_news | Google News | global | search | public | secondary | https://news.google.com/search?q={keywords} | search results;source links;dates | limited_note |
| bing_news | Bing News | global | search | public | secondary | https://www.bing.com/news/search?q={keywords} | search results;source links;dates | limited_note |
| baidu_search | Baidu Search | china | search | public | secondary | https://www.baidu.com/s?wd={keywords} | search results;source links | limited_note |
| sogou_search | Sogou Search | china | search | public | secondary | https://www.sogou.com/web?query={keywords} | search results;source links | limited_note |
| product_hunt | Product Hunt | global | product | public | supplemental | https://www.producthunt.com/search?q={keywords} | product cards;launch dates | limited_note |
| hacker_news | Hacker News | global | community | public | supplemental | https://hn.algolia.com/?q={keywords} | discussions;points;dates | limited_note |
| ycombinator | Y Combinator | global | product | public | supplemental | https://www.ycombinator.com/companies?query={keywords} | company cards;descriptions | limited_note |
| app_store | Apple App Store | global | appstore | public | supplemental | https://www.apple.com/search/{keywords}?src=serp | app results;publisher | limited_note |
| google_play | Google Play | global | appstore | public | supplemental | https://play.google.com/store/search?q={keywords}&c=apps | app results;publisher | limited_note |
| reuters | Reuters | global | media | public | primary | https://www.reuters.com/site-search/?query={keywords} | article titles;dates;source urls | limited_note |
| bloomberg | Bloomberg | global | media | public | secondary | https://www.bloomberg.com/search?query={keywords} | article titles;dates | limited_note |
| techcrunch | TechCrunch | global | media | public | secondary | https://techcrunch.com/search/{keywords}/ | article titles;dates | limited_note |
| the_verge | The Verge | global | media | public | secondary | https://www.theverge.com/search?q={keywords} | article titles;dates | limited_note |
| mit_technology_review | MIT Technology Review | global | media | public | secondary | https://www.technologyreview.com/search/?s={keywords} | article titles;dates | limited_note |
| wired | Wired | global | media | public | secondary | https://www.wired.com/search/?q={keywords} | article titles;dates | limited_note |
| x_twitter | X | global | social | chrome_login | supplemental | https://x.com/search?q={keywords}&src=typed_query&f=live | search results;timestamps;public post urls | manual_required |
| youtube | YouTube | global | video | chrome_login | supplemental | https://www.youtube.com/results?search_query={keywords} | video titles;channels;dates | manual_required |
| reddit | Reddit | global | community | public | supplemental | https://www.reddit.com/search/?q={keywords} | discussions;communities;dates | limited_note |
| linkedin | LinkedIn | global | social | chrome_login | supplemental | https://www.linkedin.com/search/results/content/?keywords={keywords} | post titles;authors;dates | manual_required |

## China Stable Sources

| source_id | name | region | type | access_mode | priority | url_or_query | required_signals | failure_policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kr36 | 36kr | china | media | public | secondary | https://36kr.com/search/articles/{keywords} | article titles;dates | limited_note |
| latepost | LatePost | china | media | public | secondary | https://www.latepost.com/search?keyword={keywords} | article titles;dates | limited_note |
| huxiu | Huxiu | china | media | public | secondary | https://www.huxiu.com/search.html?s={keywords} | article titles;dates | limited_note |
| titanium_media | TMTPost | china | media | public | secondary | https://www.tmtpost.com/search/{keywords} | article titles;dates | limited_note |
| jiemian | Jiemian | china | media | public | secondary | https://www.jiemian.com/search?keyword={keywords} | article titles;dates | limited_note |
| caixin | Caixin | china | media | public | secondary | https://search.caixin.com/search/{keywords}.html | article titles;dates | limited_note |
| yicai | Yicai | china | media | public | secondary | https://www.yicai.com/search?keys={keywords} | article titles;dates | limited_note |
| sspai | Sspai | china | media | public | supplemental | https://sspai.com/search/post/{keywords} | article titles;dates | limited_note |
| zhihu | Zhihu | china | social | chrome_login | supplemental | https://www.zhihu.com/search?type=content&q={keywords} | results;answers;timestamps | manual_required |
| weibo | Weibo | china | social | chrome_login | supplemental | https://s.weibo.com/weibo?q={keywords} | posts;hot labels;timestamps | manual_required |
| bilibili | Bilibili | china | video | chrome_login | supplemental | https://search.bilibili.com/all?keyword={keywords} | videos;authors;dates | manual_required |
| xiaohongshu | Xiaohongshu | china | social | chrome_login | supplemental | https://www.xiaohongshu.com/search_result?keyword={keywords} | notes;authors;dates | manual_required |
| wechat_public | WeChat Public Pages | china | social | manual | supplemental | search engine query: site:mp.weixin.qq.com {keywords} | article titles;account names;dates | manual_required |
| miit | Ministry of Industry and Information Technology | china | government | public | primary | https://www.miit.gov.cn/search/index.html?searchword={keywords} | official documents;dates | limited_note |
| cac | Cyberspace Administration of China | china | government | public | primary | https://www.cac.gov.cn/was5/web/search?searchword={keywords} | official documents;dates | limited_note |

## Default AI Vertical Sources

| source_id | name | region | type | access_mode | priority | url_or_query | required_signals | failure_policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai_blog | OpenAI Blog | global | official | public | primary | https://openai.com/news/ | posts;dates;canonical urls | skip |
| openai_research | OpenAI Research | global | official | public | primary | https://openai.com/research/ | posts;dates;canonical urls | skip |
| anthropic_news | Anthropic News | global | official | public | primary | https://www.anthropic.com/news | posts;dates;canonical urls | skip |
| google_deepmind | Google DeepMind | global | official | public | primary | https://deepmind.google/discover/blog/ | posts;dates;canonical urls | skip |
| meta_ai | Meta AI | global | official | public | primary | https://ai.meta.com/blog/ | posts;dates;canonical urls | skip |
| microsoft_ai | Microsoft AI Blog | global | official | public | primary | https://blogs.microsoft.com/ai/ | posts;dates;canonical urls | skip |
| nvidia_ai | NVIDIA AI Blog | global | official | public | primary | https://blogs.nvidia.com/blog/category/deep-learning/ | posts;dates;canonical urls | skip |
| xai | xAI | global | official | public | primary | https://x.ai/news | posts;dates;canonical urls | skip |
| mistral_ai | Mistral AI News | global | official | public | primary | https://mistral.ai/news/ | posts;dates;canonical urls | skip |
| huggingface_blog | Hugging Face Blog | global | official | public | primary | https://huggingface.co/blog | posts;dates;canonical urls | skip |
| github_trending | GitHub Trending | global | code | public | primary | https://github.com/trending?since=daily | repositories;stars;language | limited_note |
| github_search | GitHub Search | global | code | public | primary | https://github.com/search?q={keywords}&type=repositories&s=updated&o=desc | repositories;stars;updated dates | limited_note |
| github_topics_ai | GitHub AI Topics | global | code | public | secondary | https://github.com/topics/artificial-intelligence | repositories;stars;descriptions | limited_note |
| huggingface_models | Hugging Face Models | global | code | public | primary | https://huggingface.co/models?search={keywords} | models;downloads;likes | limited_note |
| huggingface_spaces | Hugging Face Spaces | global | code | public | secondary | https://huggingface.co/spaces?search={keywords} | spaces;likes;updated dates | limited_note |
| papers_with_code | Papers with Code | global | paper | public | secondary | https://paperswithcode.com/search?q={keywords} | papers;tasks;dates | limited_note |
| arxiv_ai | arXiv AI Search | global | paper | public | primary | https://arxiv.org/search/?query={keywords}&searchtype=all&source=header | papers;authors;dates | limited_note |
| semantic_scholar | Semantic Scholar | global | paper | public | secondary | https://www.semanticscholar.org/search?q={keywords}&sort=relevance | papers;authors;dates | limited_note |
| openreview | OpenReview | global | paper | public | supplemental | https://openreview.net/search?term={keywords} | papers;venues;dates | limited_note |
| jiqizhixin | Machine Heart | china | media | public | secondary | https://www.jiqizhixin.com/search?keywords={keywords} | article titles;dates | limited_note |
| qbitai | QbitAI | china | media | public | secondary | https://www.qbitai.com/?s={keywords} | article titles;dates | limited_note |
| xinzhiyuan | Xinzhiyuan | china | media | public | secondary | https://www.163.com/dy/media/T1603594732083.html | article titles;dates | limited_note |
| leiphone_ai | Leiphone AI | china | media | public | secondary | https://www.leiphone.com/search?s={keywords} | article titles;dates | limited_note |
| infoq_cn | InfoQ China | china | media | public | secondary | https://www.infoq.cn/search?q={keywords} | article titles;dates | limited_note |
| jazzyear | Jiazi Guangnian | china | media | public | secondary | https://www.jazzyear.com/search/{keywords} | article titles;dates | limited_note |

## Initialization Notes

- Start with the general stable sources plus a vertical source pack selected by the user.
- For a non-AI topic, keep the general stable sources and add user-provided vertical media, communities, official sites, and search queries.
- Use login-state sources for heat and discussion only unless they point to an official/original announcement.
- Report source share by both source type and region. A source can contribute to one type bucket and one regional bucket.
