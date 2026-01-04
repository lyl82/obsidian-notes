"""
================================================================
脚本名称: workout_archiver.py
总功能描述: 
    专门用于归档“锻炼&空间移动”目录下的所有 Markdown 文件。
    核心逻辑：
    1. 递归扫描：支持处理子文件夹下的所有文件。
    2. 创建时间读取：使用文件的创建时间（ctime）提取归档月份。
    3. 自动化标签体系：
        - 强制标签：所有文件自动注入 #锻炼。
        - 文件夹标签：读取直接父文件夹名称作为标签。
        - 语义标签：基于内容关键词自动匹配（如压力、疲劳、肌肉等）。
    4. 移动逻辑：归档成功后自动删除源文件，保持目录整洁。
================================================================
"""

import os
import datetime
import shutil

# 配置区域
SOURCE_DIR = r"D:\个人记录\obsidian-file\wjmber\《行为内容存储箱》\A-《锻炼&空间移动》"
DEST_BASE_DIR = r"D:\个人记录\obsidian-file\wjmber\《记录》\《2025》\归档"

# 关键词库
KEYWORDS = ["压力", "疲劳", "睡眠", "障碍", "认知", "状态", "记录", "总结", "情绪", "思考", "环境", "肌肉", "运动", "公园", "身体", "训练", "感受"]

def get_tags_from_content(content):
    """提取内容关键词标签"""
    found_tags = []
    for kw in KEYWORDS:
        if kw in content:
            found_tags.append(f"#{kw}")
    return found_tags

def archive_workout_files():
    """递归归档锻炼目录下的文件"""
    if not os.path.exists(SOURCE_DIR):
        print(f"源目录不存在: {SOURCE_DIR}")
        return

    print(f"开始扫描锻炼目录: {SOURCE_DIR}")
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        for filename in files:
            if not filename.endswith(".md"):
                continue
            
            file_path = os.path.join(root, filename)
            
            # 1. 获取时间属性 (创建时间 ctime)
            try:
                stat = os.stat(file_path)
                # Windows 下 st_ctime 是创建时间
                ctime = datetime.datetime.fromtimestamp(stat.st_ctime)
                year_month = ctime.strftime("%Y-%m")
            except Exception as e:
                print(f"获取时间失败 {filename}: {e}")
                continue

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
            # 获取直接父文件夹名作为基础标签
            parent_folder = os.path.basename(root)
            # 如果父文件夹就是源根目录，则不重复打标（或可自定义）
            parent_tag = f"#{parent_folder}" if parent_folder != os.path.basename(SOURCE_DIR) else ""
            
            content_tags = get_tags_from_content(content)
            
            # 强制注入 #锻炼 标签
            all_tags = ["#锻炼"]
            if parent_tag:
                all_tags.append(parent_tag)
            all_tags.extend(content_tags)
            
            # 去重并生成标签行
            unique_tags = []
            for t in all_tags:
                if t not in unique_tags:
                    unique_tags.append(t)
            
            tag_line = " ".join(unique_tags) + "\n\n"
            
            # 5. 写入目标
            new_content = tag_line + content
            target_file_path = os.path.join(target_dir, filename)
            
            # 处理同名文件冲突（如果需要）
            if os.path.exists(target_file_path):
                base, ext = os.path.splitext(filename)
                target_file_path = os.path.join(target_dir, f"{base}_{datetime.datetime.now().strftime('%H%M%S')}{ext}")

            try:
                with open(target_file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                
                # 6. 移动成功后删除源文件
                os.remove(file_path)
                print(f"已移动: {filename} -> {year_month}/")
            except Exception as e:
                print(f"写入或移动失败 {filename}: {e}")

    print("\n锻炼目录归档完成。")

if __name__ == "__main__":
    archive_workout_files()
