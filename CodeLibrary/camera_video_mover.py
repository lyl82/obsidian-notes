"""
================================================================
脚本名称: camera_video_mover.py
总功能描述:
    将指定目录下的所有视频文件剪切(移动)到目标目录，用于快速清空相册目录、集中管理视频。
    注意: 对于 MTP 设备路径(如「此电脑/手机名/内部存储设备/...」)，标准文件 API 可能无法直接访问，
          建议先在资源管理器中把手机相册内容复制到本地盘符目录，再运行本脚本进行剪切归档。

核心逻辑:
    1. 源目录扫描: 遍历源目录(可配置是否递归)，过滤出常见视频扩展名文件。
    2. 目标目录准备: 自动创建目标目录(如 H:\\2025)，保持现有文件不覆盖。
    3. 剪切移动: 使用 shutil.move 将文件从源目录剪切到目标目录，如发生同名冲突则自动重命名。
    4. 安全控制: 支持 DRY_RUN(仅打印计划，不实际移动)模式，默认开启，确认无误后可手动关闭。
================================================================
"""

import os
import shutil
import datetime
from typing import Tuple

# ===================== 配置区域 =====================
# ⚠️ IMPORTANT:
#   对于「此电脑\\Redmi K70\\内部存储设备\\DCIM\\Camera」这类路径，
#   Python 无法直接通过 os.walk 访问，因为它是 MTP 设备而不是普通盘符。
#   建议流程:
#     1) 在资源管理器中把手机相册目录整体复制到某个本地/移动硬盘目录，例如:
#          H:\\Redmi_K70_DCIM\\Camera
#     2) 把下面 SOURCE_DIR 改成该本地目录路径;
#     3) 运行本脚本完成剪切到 H:\\2025。

# 源目录(请改成实际可访问的本地路径)
SOURCE_DIR = r"H:\\Redmi_K70_DCIM\\Camera"  # 示例路径，请根据实际情况修改

# 目标目录: 你的需求是剪切到 H:\\2025
DEST_DIR = r"H:\\2025"

# 是否递归遍历子目录
RECURSIVE = False

# 支持的视频扩展名
VIDEO_EXTENSIONS = (".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv")

# 安全模式: 为 True 时，只打印将要执行的操作，不真正移动文件
DRY_RUN = True

# ==================================================


def ensure_directory(path: str) -> None:
    """确保目录存在"""
    if not os.path.exists(path):
        os.makedirs(path)


def is_video_file(filename: str) -> bool:
    """判断是否为视频文件"""
    lower = filename.lower()
    return any(lower.endswith(ext) for ext in VIDEO_EXTENSIONS)


def resolve_conflict(dest_path: str) -> str:
    """如果目标路径已存在文件，生成一个不冲突的新文件名"""
    if not os.path.exists(dest_path):
        return dest_path

    base, ext = os.path.splitext(dest_path)
    timestamp = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")
    new_path = f"{base}{timestamp}{ext}"
    # 如果极端情况仍然冲突，再加计数器
    counter = 1
    while os.path.exists(new_path):
        new_path = f"{base}{timestamp}_{counter}{ext}"
        counter += 1
    return new_path


def move_videos(source_dir: str, dest_dir: str, recursive: bool = False, dry_run: bool = True) -> Tuple[int, int]:
    """执行视频文件的剪切移动

    返回值: (found_count, moved_count)
    """
    if not os.path.exists(source_dir):
        print(f"源目录不存在或不可访问: {source_dir}")
        return 0, 0

    ensure_directory(dest_dir)

    found = 0
    moved = 0

    print("开始扫描目录:", source_dir)
    print("递归模式:", "ON" if recursive else "OFF")
    print("DRY_RUN 模式:", "ON (仅预览, 不实际移动)" if dry_run else "OFF (将执行实际移动)")
    print("目标目录:", dest_dir)
    print("支持的视频扩展名:", ", ".join(VIDEO_EXTENSIONS))
    print("-" * 60)

    if recursive:
        walker = os.walk(source_dir)
    else:
        # 仅当前目录
        try:
            files = os.listdir(source_dir)
        except PermissionError as e:
            print(f"无法列出目录 {source_dir}: {e}")
            return 0, 0
        walker = [(source_dir, [], files)]

    for root, dirs, files in walker:
        for filename in files:
            if not is_video_file(filename):
                continue

            found += 1
            src_path = os.path.join(root, filename)
            dest_path = os.path.join(dest_dir, filename)
            dest_path_final = resolve_conflict(dest_path)

            rel_root = os.path.relpath(root, source_dir)
            rel_info = "." if rel_root == "." else rel_root
            print(f"发现视频: {filename} | 所在: {rel_info}")
            print(f"  -> 计划移动到: {dest_path_final}")

            if not dry_run:
                try:
                    shutil.move(src_path, dest_path_final)
                    moved += 1
                    print("  [已移动]")
                except Exception as e:
                    print(f"  [失败] 无法移动 {src_path} -> {dest_path_final}: {e}")
            else:
                print("  [DRY_RUN] 未实际移动")

            print("-")

    print("扫描结束。共发现视频文件:", found)
    print("实际移动数量:", moved if not dry_run else 0)
    if dry_run:
        print("当前为 DRY_RUN 预览模式。如确认无误，可将 DRY_RUN = False 再次运行。")

    return found, moved


if __name__ == "__main__":
    move_videos(SOURCE_DIR, DEST_DIR, recursive=RECURSIVE, dry_run=DRY_RUN)
