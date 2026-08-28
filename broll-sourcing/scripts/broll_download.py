# -*- coding: utf-8 -*-
"""
B-roll 素材下载器（Python API 版，修复 Windows 文件名乱码）
用法: python broll_download.py "<视频链接或搜索词>"
下载到 ../01_下载原片/，自动选最高1080p，自动合成 MP4。
ffmpeg 优先从 PATH 探测，找不到时可用环境变量 FFMPEG_PATH 指定目录。
"""
import sys, os, re

# Windows 控制台 GBK 编码兼容
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import yt_dlp

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
RAW_DIR = os.path.join(LIB_DIR, "01_下载原片")
os.makedirs(RAW_DIR, exist_ok=True)

# ffmpeg 位置：优先 PATH，其次 FFMPEG_PATH 环境变量
FFMPEG_DIR = os.environ.get("FFMPEG_PATH") or None

def sanitize(name):
    """清理文件名中的非法字符"""
    return re.sub(r'[\\/:*?"<>|\n\r\t]', "_", name).strip()[:80]

def main():
    if len(sys.argv) < 2:
        print("[提示] 用法: broll_download.py <链接或搜索词>")
        return

    query = sys.argv[1].strip()
    if "http" not in query:
        query = f"bilisearch1:{query}"

    # 先拿标题
    with yt_dlp.YoutubeDL({"skip_download": True, "quiet": True, "no_warnings": True}) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
        except Exception as e:
            print(f"[失败] 无法获取视频信息: {e}")
            return
        if "entries" in info:  # 搜索结果，取第一条
            entries = list(info["entries"])
            if not entries:
                print("[失败] 没搜到结果，换个关键词试试")
                return
            info = entries[0]
        title = sanitize(info.get("title", "未命名"))
        duration = info.get("duration")
        dur_str = f"{int(duration)//60}分{int(duration)%60}秒" if duration else "未知时长"
        print(f"[信息] 视频标题: {title}")
        print(f"[信息] 时长: {dur_str}")

    # 下载
    opts = {
        "format": "bv*[height<=1080]+ba/b[height<=1080]/b",
        "merge_output_format": "mp4",
        "ffmpeg_location": FFMPEG_DIR,
        "outtmpl": os.path.join(RAW_DIR, f"{title}.%(ext)s"),
        "noplaylist": True,
        "windowsfilenames": True,
        "progress": True,
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([query])
        print(f"\n[完成] 已保存到: {RAW_DIR}")
        print("[提示] 下一步: 用 broll_slice.py 切片空镜")
    except Exception as e:
        print(f"\n[失败] 下载出错: {e}")

if __name__ == "__main__":
    main()
