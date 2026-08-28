# -*- coding: utf-8 -*-
"""
B-roll 空镜切片器
用法: python broll_slice.py "<视频文件路径>"
交互式输入起止时间，切片输出到 ../02_空镜片段/，统一静音+1080p mp4。
ffmpeg 优先从 PATH 探测，找不到时可用环境变量 FFMPEG_PATH 指定。
"""
import sys, os, subprocess, re, shutil

# Windows 控制台 GBK 编码兼容
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
RAW_DIR = os.path.join(LIB_DIR, "01_下载原片")
SLICE_DIR = os.path.join(LIB_DIR, "02_空镜片段")
os.makedirs(SLICE_DIR, exist_ok=True)

FFMPEG = shutil.which("ffmpeg") or os.environ.get("FFMPEG_PATH")
if not FFMPEG:
    print("[失败] 找不到 ffmpeg：请将其加入 PATH，或设置环境变量 FFMPEG_PATH 指向 ffmpeg 可执行文件")
    sys.exit(1)

def parse_time(s):
    """支持 1:23 或 12:34 或 1:02:03 格式"""
    s = s.strip()
    parts = s.split(":")
    parts = [float(p) for p in parts]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    else:
        return float(s)

def main():
    if len(sys.argv) < 2:
        print("[提示] 用法: broll_slice.py <视频文件路径>")
        return

    src = sys.argv[1].strip().strip('"')
    if not os.path.exists(src):
        # 尝试在下载目录里找
        cand = os.path.join(RAW_DIR, src)
        if os.path.exists(cand):
            src = cand
        else:
            print(f"[失败] 找不到文件: {src}")
            return

    base = os.path.splitext(os.path.basename(src))[0]
    print(f"[信息] 视频: {base}")
    print("[说明] 时间格式: 1:23 或 12:34 或 1:02:03；多个片段用逗号分隔")
    print("       例: 0:15-0:23, 1:05-1:12, 2:30-2:41")

    seg_input = input("请输入片段起止时间: ").strip()
    segs = [s.strip() for s in seg_input.split(",") if s.strip()]

    count = 0
    for i, seg in enumerate(segs, 1):
        m = re.match(r"([\d:\.]+)\s*[-~]\s*([\d:\.]+)", seg)
        if not m:
            print(f"[跳过] 无法解析: {seg}")
            continue
        t0, t1 = parse_time(m.group(1)), parse_time(m.group(2))
        if t1 <= t0:
            print(f"[跳过] 结束时间需大于开始时间: {seg}")
            continue
        out = os.path.join(SLICE_DIR, f"{base}_片段{i:02d}_{int(t0)}s-{int(t1)}s.mp4")
        cmd = [
            FFMPEG, "-y",
            "-ss", str(t0), "-to", str(t1),
            "-i", src,
            "-an",                      # 去掉声音（空镜B-roll）
            "-vf", "scale=-2:1080",     # 统一1080p
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
            out,
        ]
        print(f"[切片 {i}] {seg} -> {os.path.basename(out)}")
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0:
            count += 1
            print(f"      完成")
        else:
            print(f"      失败: {r.stderr[-200:]}")

    print(f"\n[完成] 共切出 {count} 个片段，保存在: {SLICE_DIR}")

if __name__ == "__main__":
    main()
