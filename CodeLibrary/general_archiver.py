"""
================================================================
脚本名称: general_archiver.py
总功能描述: 
    该脚本是一个通用的 Markdown 文件归档工具，支持从多个源目录批量迁移文件。
    核心逻辑：
    1. 多路径支持：可配置多个源目录进行扫描。
    2. 目录深度控制：默认仅处理源目录根下的 .md 文件，避免误删子系统文件夹。
    3. 自动化标签体系：
        - 文件夹标签：读取源目录名称作为标签。
        - 语义标签：基于内容关键词自动匹配（如工作、社交、情绪等）。
    4. 时间轴归档：基于文件修改时间（mtime）自动分月存储。
================================================================
"""

import os
import datetime

# 配置区域
SOURCE_DIRS = [
    r"D:\个人记录\obsidian-file\wjmber\tasks",
    r"D:\个人记录\obsidian-file\wjmber\《行为内容存储箱》\中文-en-语言文字层"
]
DEST_BASE_DIR = r"D:\个人记录\obsidian-file\wjmber\《记录》\《2025》\归档"

# 关键词库
KEYWORDS = ["工作", "社交", "情绪", "思考", "任务", "英语", "经济", "政治", "心理", "信息", "运动", "健康"]

def get_tags_from_content(content):
    """提取内容关键词标签"""
    found_tags = []
    for kw in KEYWORDS:
        if kw in content:
            found_tags.append(f"#{kw}")
    return found_tags

def process_directory(source_path):
    """处理单个目录下的文件"""
    if not os.path.exists(source_path):
        print(f"警告: 目录不存在 - {source_path}")
        return

    # 获取文件夹名作为基础标签
    folder_tag = f"#{os.path.basename(source_path)}"
    
    # 仅获取当前目录下的 md 文件（不递归，防止误触系统目录）
    files = [f for f in os.listdir(source_path) if os.path.isfile(os.path.join(source_path, f)) and f.endswith(".md")]
    
    for filename in files:
        file_path = os.path.join(source_path, filename)
        
        # 1. 获取时间属性
        stat = os.stat(file_path)
        mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
        year_month = mtime.strftime("%Y-%m")
        
        # 2. 准备目标路径
        target_dir = os.path.join(DEST_BASE_DIR, year_month)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # 3. 读取并处理内容
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"读取失败 {filename}: {e}")
            continue
            
        # 4. 生成标签行
        content_tags = get_tags_from_content(content)
        all_tags = [folder_tag] + content_tags
        tag_line = " ".join(all_tags) + "\n\n"
        
        # 5. 写入目标
        new_content = tag_line + content
        target_file_path = os.path.join(target_dir, filename)
        
        try:
            with open(target_file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            
            # 6. 归档成功后删除源文件
            os.remove(file_path)
            print(f"归档成功并移除源文件: {filename} -> {year_month}/")
            
        except Exception as e:
            print(f"写入或删除失败 {filename}: {e}")

def main():
    print(f"开始执行通用归档任务...")
    for path in SOURCE_DIRS:
        print(f"\n正在处理目录: {path}")
        process_directory(path)
    print("\n所有任务已完成。")

if __name__ == "__main__":
    main()
