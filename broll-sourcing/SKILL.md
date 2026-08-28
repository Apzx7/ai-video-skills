---
name: broll-sourcing
description: Sourcing B-roll and empty-shot footage for knowledge/finance explainer videos. Covers searching and downloading watermark-free clips (Bilibili, YouTube, news sites) via yt-dlp, slicing with ffmpeg, archiving to the user's broll library, mixing with free stock libraries and AI-generated shots, and copyright-safe usage rules. Use when the user asks for 空镜, B-roll, 素材, video footage, 下载视频, or footage for their explainer videos.
---

# B-roll 素材工作流

## 与白板动画技能的分工（知识类视频生产线）

知识类视频（讲解/财经/历史）由两个技能配合完成：

- **srt-whiteboard-animation**：把讲解文案（SRT 字幕）渲染成手绘白板动画——这是视频的「骨架」，承担核心概念讲解，完全本地免费渲染
- **本技能（broll-sourcing）**：提供「血肉」——下载/生成空镜素材用于转场、氛围、纪实画面补充

判断规则：用户说"把文案做成白板动画/SRT 生成动画"→ 用 srt-whiteboard-animation；用户说"找空镜/下载素材/B-roll"→ 用本技能。若用户要求做完整知识类视频，先跑白板动画出骨架，再问需要哪些空镜。

## 素材库结构（首次使用先问用户素材库根目录）

库根目录由用户指定（本技能发布者的实例：`D:\视频素材\我的素材\broll库\`），目录结构统一为：

- `01_下载原片\` 原始下载视频
- `02_空镜片段\` 切好的空镜（静音、1080p、mp4）
- `03_AI生成空镜\` AI 生成的空镜素材
- `04_已用归档\` 已用完的素材（移到这里，不删除）
- `scripts\` 本技能自带脚本（复制到这里）
- `douyin-config\` 抖音下载 cookie 配置（需要时创建）

## 三源混合策略（默认）

1. **下载素材**（B站/YouTube/新闻站）：用 yt-dlp，适合纪实画面、新闻镜头、纪录片片段
2. **免费素材库**：Pexels/Pixabay/Mixkit，无水印可商用，适合通用城市/自然/办公画面
3. **AI生成空镜**：即梦/可灵或 ImageGen，适合历史复原、抽象概念、无版权风险的原创画面

每个主题按内容自动分配：历史纪实类以下载素材为主；抽象概念/财经数据类以 AI 生成为主；通用过渡画面用免费素材库。

## 下载流程

先将本技能自带的 `scripts/broll_download.py` 复制到素材库 `scripts\` 下。

### 用户给链接时

直接执行：

```bash
python "<素材库根目录>\scripts\broll_download.py" "<链接>"
```

### 用户只给主题时

1. 用 `yt-dlp "bilisearchN:关键词"`（N=1~10 条结果）搜索 B 站，列出候选给用户挑；YouTube 用 `ytsearchN:关键词`
2. 用户选定后执行下载脚本

### 常用站点处理

- B站: `bv*[height<=1080]+ba/b[height<=1080]/b`，通常无需登录
- YouTube: 同格式串；需要 cookies 时提示用户用浏览器插件导出 cookies.txt
- 新闻站（央视网、新华网等）: yt-dlp 直接支持多数页面链接
- 会员/独家内容: yt-dlp 无法下载时如实告知，不承诺绕过付费

### 抖音链接（无水印专用）

用 douyin-dl（jiji262/douyin-downloader CLI，纯 Python，不走桌面版）：

```bash
cd "<素材库根目录>"
PYTHONIOENCODING=utf-8 douyin-dl -u "<抖音分享链接>" -c "douyin-config/config.yml"
```

关键事实：

- 无水印原理：调 aweme detail API 后从候选 URL 优先挑 `watermark=0` 的直连 CDN 地址
- **必须配置 cookie**（odin_tt、passport_csrf_token、ttwid），否则 API 返回 anti-bot 空响应。获取方式：运行 douyin-dl 上游仓库自带的 `tools/cookie_fetcher.py`（依赖 playwright，会弹出浏览器引导手动登录后自动导出 cookies）
- 视频分辨率问题：抖音无水印源有时只给 720p，属正常，告知用户即可
- Windows 控制台必须带 `PYTHONIOENCODING=utf-8`，否则 rich 库 GBK 报错

## 切片流程

下载完成后用本技能自带的 `scripts/broll_slice.py`（复制到素材库 `scripts\` 下）：

```bash
python "<素材库根目录>\scripts\broll_slice.py" "<视频完整路径>"
```

脚本交互式输入起止时间，支持 `1:23-1:45` 格式，多段用逗号分隔。输出统一为静音、1080p、mp4，自动命名。

Agent 主动使用时：先告知用户预计切几段、每段多少秒，让用户确认时间点。

## 版权与安全规则（必须遵守）

1. 新闻片段单段引用控制在 15 秒内，避免完整露出台标画面
2. 提醒用户：B站/YouTube 下载素材用于公开发布有版权风险，成片需混合自己的解说、字幕、剪辑，不可整段搬运
3. 商用/接单视频优先推荐免费素材库和 AI 生成，避免下载素材
4. 素材用完移入 `04_已用归档\`，不删除文件
5. 不下架、不爬取付费内容，不绕过 DRM

## AI 生成空镜提示词规范

用户要做 AI 空镜时，遵循既有协作模式：

1. 先确认画风、画幅（知识类视频通常横屏 16:9）
2. 输出提示词时用「固定锚点词块」保证系列一致性
3. 历史类内容优先查证史实再写提示词，避免 AI 画出穿帮画面（如错误的服饰、建筑年代）
4. 生成图存入 `03_AI生成空镜\`，命名带主题前缀

## 环境要求

- Python 3.8+，`pip install yt-dlp`
- ffmpeg/ffprobe 在 PATH 中；不在 PATH 时设置环境变量 `FFMPEG_PATH` 指向 ffmpeg 目录（脚本优先探测 PATH）
- douyin-dl：`pip install` 或按上游仓库说明安装（仅下载抖音时需要）
- Windows 控制台建议统一 `PYTHONIOENCODING=utf-8` 防 GBK 乱码

## 验证

- 下载完成: 检查 `01_下载原片\` 有新文件且大小 > 0
- 切片完成: 检查 `02_空镜片段\` 片段数正确，用 ffprobe 确认时长、1080p、无音轨
