# ai-video-skills

AI 视频创作 Skill 合集。每个 skill 是一份给 AI 助手的"操作手册"：给定场景，按步骤执行，按格式输出。适用于 QoderWork、Claude Code 等支持 skills 的 AI 工具，也可作为提示词参考直接阅读。

## 技能列表

### ai-microfilm-prompt-pack（v1.3.0）

AI 微电影 / AI 漫剧提示词包产出流程。给一个想法或一段文案，产出完整可执行的提示词包。

- 形态分流：十几秒短视频走爆款逻辑（黄金三秒钩子 + 情绪爆点 + 转场卡点）；微电影（1 分钟以上）走五段式故事结构（激励事件 / 进展纠葛 / 危机 / 高潮 / 引发思考的结尾）
- 固定生成顺序：角色素体三视图 → 道具状态版三视图（以素体图为参考图生）→ 特殊道具设定图 → 场景空镜图 → 每镜关键帧 → 图生视频
- 交付物：分镜脚本、三视图提示词、道具设定图提示词、场景提示词、每镜完整提示词、带时间码配音稿
- 素材归档规范：主题文件夹下分 人物 / 道具 / 场景 / 镜头 / 旁白 / 成片，全程去水印

### style-liaozhai-guofeng

聊斋国风水墨工笔 AI 动画风格库。提供三套可直接复制的风格锚点词块（通用 / 夜色 / 惊悚变奏）、人物与场景锚点示例、配套负面提示词，供 ai-microfilm-prompt-pack 第 0 步引用。其他风格可按同样结构沉淀为新的 style-* 技能。

### broll-sourcing

知识/财经类讲解视频的 B-roll 空镜素材工作流：B站/YouTube/新闻站无水印素材搜索下载（yt-dlp）、ffmpeg 切片空镜、抖音无水印下载（douyin-dl）、三源混合策略（下载素材 + 免费素材库 + AI 生成），附版权安全规则与归档规范。自带下载/切片脚本（scripts/），素材库路径首次使用时由用户指定。

## 目录结构

```
ai-video-skills/
├── ai-microfilm-prompt-pack/
│   ├── SKILL.md       # 主流程
│   └── reference.md   # 参考库：锚点写法、负面词库、工具路径、对照案例
├── style-liaozhai-guofeng/
│   └── SKILL.md       # 风格锚点词块 + 负面词库 + 使用边界
└── broll-sourcing/
    ├── SKILL.md       # B-roll 素材工作流
    └── scripts/       # 下载/切片脚本（broll_download.py、broll_slice.py）
```

## 安装使用

作为 Skill 安装：把对应 skill 目录整个复制到工具的技能目录（如 `~/.qoderworkcn/skills/`、`~/.claude/skills/`），工具会自动识别并在相关任务中调用。

作为提示词参考：直接打开 SKILL.md，按其中流程与锚点词块手动使用。

## License

[MIT](LICENSE)
