---
name: "obsidian-skills"
description: "导入并使用 Obsidian Skills 技能库；当用户请求使用/浏览 obsidian-skills 或导入其模板与清单时调用。"
---

# Obsidian Skills

- 作用：提供 Obsidian Skills 仓库中的技能清单与用法，支持在本地 `skills/obsidian-skills` 路径读取
- 调用时机：当用户要求“下载/使用/浏览 obsidian-skills 的技能或模板”，或希望将其作为本地技能库使用

## 使用方式
- 本地存在时：若目录 `LifeOS/skills/obsidian-skills` 已存在，则从该目录读取技能文件（md）
- 本地不存在时：请下载仓库 ZIP 并仅保留其中的 `skills` 子目录到 `LifeOS/skills/obsidian-skills`
  - 仓库地址：https://github.com/kepano/obsidian-skills/tree/main/skills
  - ZIP 下载路径（浏览器）：在仓库页面点击 Code → Download ZIP

## 本机示例（任选其一）
- 方式 A（浏览器下载 ZIP）：
  1. 下载并解压到任意临时目录
  2. 复制解压后的 `skills` 子目录到：`D:\个人记录\obsidian-file\wjmber\LifeOS\skills\obsidian-skills`
- 方式 B（本机终端 git）：
  ```powershell
  cd "D:\个人记录\obsidian-file\wjmber\LifeOS"
  git clone https://github.com/kepano/obsidian-skills.git
  # 复制 obsidian-skills\skills\* 到 LifeOS\skills\obsidian-skills
  ```

## 完成后可用能力
- 浏览与检索：从 `skills/obsidian-skills` 中按主题查找技能
- 生成与执行：基于技能文件的流程/清单生成个人实践计划或模板

