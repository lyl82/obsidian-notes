"""
# 总功能: 从小米云 Web 端导出所有笔记到本地 Markdown 文件。
# 核心逻辑:
# 1. 自动化登录/会话维持: 利用 Selenium 打开 Chrome 浏览器。
# 2. API 交互: 在浏览器上下文中执行 JavaScript 调用小米云内部 API 获取笔记列表及详情。
# 3. 数据转换: 将笔记内容转换为 Markdown 格式，并处理创建/修改时间。
# 4. 本地存储: 按笔记标题（或 ID）保存为 .md 文件。
# 应用场景: 备份小米云笔记，或将数据迁移至 Obsidian/Logseq 等工具。
"""

import os
import json
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- 配置区 ---
EXPORT_DIR = "XiaomiNotes_Export"  # 导出目录
CHROME_DATA_DIR = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data") # 默认 Chrome 数据目录
PROFILE_NAME = "Default"  # 默认配置文件名
# --- --- --- ---

def sanitize_filename(name):
    """清理文件名中的非法字符"""
    return re.sub(r'[\\/:*?"<>|]', '_', name)

def get_driver():
    """初始化 Selenium WebDriver，尝试使用本地 Chrome 配置以复用登录状态"""
    chrome_options = Options()
    # 注意：如果当前已经有一个 Chrome 实例正在运行且使用了该 User Data，Selenium 会报错。
    # 建议运行前关闭所有 Chrome 窗口，或者指定一个新的临时目录。
    # 这里为了方便，默认先不加载 User Data，让用户在弹出的浏览器中确认登录。
    
    # 如果用户想完全自动化且知道路径，可以取消下面两行的注释：
    # chrome_options.add_argument(f"--user-data-dir={CHROME_DATA_DIR}")
    # chrome_options.add_argument(f"--profile-directory={PROFILE_NAME}")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def export_notes():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    driver = get_driver()
    try:
        print("正在打开小米云笔记...")
        driver.get("https://i.mi.com/note/h5#/")
        
        print("请在浏览器中完成登录（如果尚未登录）。")
        print("等待页面加载并确认登录状态...")
        
        # 循环检查是否进入了笔记主页
        while True:
            if "i.mi.com/note/h5" in driver.current_url:
                # 简单判断是否有笔记列表的 API 可调用环境
                check_script = "return typeof window.location.href !== 'undefined';"
                if driver.execute_script(check_script):
                    break
            time.sleep(2)
        
        print("登录确认成功，开始获取笔记列表...")

        # 使用 JavaScript 在浏览器内直接请求 API，这样可以自动带上 Cookie 和 Auth Headers
        fetch_list_js = """
        return fetch('https://i.mi.com/note/full/page?limit=1000').then(res => res.json());
        """
        
        # 由于 fetch 是异步的，我们需要处理一下
        notes_data = driver.execute_async_script("""
            var callback = arguments[arguments.length - 1];
            fetch('https://i.mi.com/note/full/page?limit=1000')
                .then(response => response.json())
                .then(data => callback(data))
                .catch(err => callback({error: err.message}));
        """)

        if "error" in notes_data or notes_data.get("result") != "ok":
            print(f"获取笔记列表失败: {notes_data.get('error', '未知错误')}")
            return

        entries = notes_data.get("data", {}).get("entries", [])
        print(f"找到 {len(entries)} 条笔记，准备逐条下载详情...")

        for idx, entry in enumerate(entries):
            note_id = entry.get("id")
            
            # 获取单条笔记详情
            note_detail = driver.execute_async_script(f"""
                var callback = arguments[arguments.length - 1];
                fetch('https://i.mi.com/note/note/{note_id}/')
                    .then(response => response.json())
                    .then(data => callback(data))
                    .catch(err => callback({{error: err.message}}));
            """)

            if "error" in note_detail or note_detail.get("result") != "ok":
                print(f"[{idx+1}/{len(entries)}] 获取详情失败 (ID: {note_id})")
                continue

            note = note_detail.get("data", {}).get("entry", {})
            content = note.get("content", "")
            create_date = note.get("createDate", 0)
            modify_date = note.get("modifyDate", 0)
            
            # 转换时间
            c_time = datetime.fromtimestamp(create_date / 1000).strftime('%Y-%m-%d %H:%M:%S')
            m_time = datetime.fromtimestamp(modify_date / 1000).strftime('%Y-%m-%d %H:%M:%S')

            # 提取标题（取内容第一行或前 20 个字）
            lines = content.strip().split('\n')
            title = lines[0][:50] if lines else f"Untitled_{note_id}"
            title = sanitize_filename(title)
            if not title: title = f"Untitled_{note_id}"

            # 构造 Markdown
            md_content = f"""---
title: {title}
id: {note_id}
created: {c_time}
modified: {m_time}
---

{content}
"""
            
            file_path = os.path.join(EXPORT_DIR, f"{title}.md")
            
            # 处理重名
            counter = 1
            while os.path.exists(file_path):
                file_path = os.path.join(EXPORT_DIR, f"{title}_{counter}.md")
                counter += 1

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            
            print(f"[{idx+1}/{len(entries)}] 已导出: {title}")

        print(f"\n全部导出完成！文件保存在: {os.path.abspath(EXPORT_DIR)}")

    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    export_notes()
