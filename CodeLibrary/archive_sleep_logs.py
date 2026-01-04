"""
================================================================
脚本名称: archive_sleep_logs.py
总功能描述: 
    该脚本用于对 人生OS 1.0 系统中“睡眠-非结构dao”目录下的 Markdown 文件进行自动化归档处理。
    核心功能包括：
    1. 时间属性读取：获取文件的创建时间，提取年-月信息。
    2. 目录自动构建：在目标归档路径下按年-月创建文件夹。
    3. 自动标签注入：
        - 注入所属父文件夹名作为标签。
        - 根据文本内容匹配预设关键词（如压力、疲劳、睡眠等）自动生成内容标签。
    4. 内容迁移：将带有标签的新内容写入目标路径。
================================================================
"""

import os
import shutil
import datetime
import re

# 配置路径
source_dir = r"d:\个人记录\obsidian-file\wjmber\tasks\需求\人生OS\1_ControlPlane\SystemState\Sleep\睡眠-非结构dao"
dest_base_dir = r"d:\个人记录\obsidian-file\wjmber\《记录》\《2025》\归档"
parent_folder_name = "睡眠-非结构dao"

def get_tags_from_content(content):
    """根据内容匹配关键词生成标签"""
    keywords = ["压力", "疲劳", "睡眠", "障碍", "认知", "状态", "记录", "总结", "情绪", "思考", "环境"]
    found_tags = []
    for kw in keywords:
        if kw in content:
            found_tags.append(f"#{kw}")
    return found_tags

def archive_files():
    """执行归档主逻辑"""
    if not os.path.exists(source_dir):
        print(f"源目录不存在: {source_dir}")
        return

    # 仅处理 md 文件
    files = [f for f in os.listdir(source_dir) if f.endswith(".md")]
    
    if not files:
        print("没有找到待归档的 .md 文件。")
        return

    for filename in files:
        file_path = os.path.join(source_dir, filename)
        
        # 1. 获取最后修改时间
        stat = os.stat(file_path)
        mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
        year_month = mtime.strftime("%Y-%m")
        
        # 2. 创建目标子目录
        target_dir = os.path.join(dest_base_dir, year_month)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # 3. 读取原始内容
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # 4. 生成标签行
        content_tags = get_tags_from_content(content)
        all_tags = [f"#{parent_folder_name}"] + content_tags
        tag_line = " ".join(all_tags) + "\n\n"
        
        # 5. 拼接标签并写入新位置
        new_content = tag_line + content
        target_file_path = os.path.join(target_dir, filename)
        
        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        # 6. 删除源文件
        os.remove(file_path)
        print(f"已归档并移除源文件: {filename} -> {target_file_path}")

if __name__ == "__main__":
    archive_files()
