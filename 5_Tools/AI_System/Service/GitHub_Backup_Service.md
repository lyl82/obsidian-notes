# Service: GitHub 自动备份 (Skill & Instruction)

**Service Purpose**: 确保 LifeOS 系统的所有增量改动能够以“小时”为单位自动同步到 GitHub 私有仓库，实现数据的高冗余备份，且不干扰用户的“版本发布”节奏。

cd "d:\个人记录\obsidian-file\wjmber\LifeOS"

# 如果还没有 .git 目录，则初始化
git init

# 关联远程仓库（按你实际仓库地址改）
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 第一次手动提交（随便起个说明性名字）
git add -A
git commit -m "Initial backup"
git branch -M main   # 如果你想让主分支叫 main
git push -u origin main

---

## 1. 技术架构 (Architecture)

本系统由三个核心组件构成：
1.  **本地 Git 仓库**：位于 `d:\个人记录\obsidian-file\wjmber\LifeOS`。
2.  **自动化脚本**：[auto-backup.ps1](file:///d:/个人记录/obsidian-file/wjmber/LifeOS/auto-backup.ps1) (PowerShell 编写)。
3.  **定时触发器**：Windows 任务计划程序 (Task Scheduler)。

---

## 2. 用户操作指南 (User Manual)
*适用于用户在没有 AI 协助的情况下手动管理系统*

### A. 如何判断备份是否成功？
1.  **查看本地日志**：在终端进入目录执行 `git log -n 5`，如果看到 `auto backup 2026-xx-xx ...` 格式的提交，说明本地备份成功。
2.  **查看远程状态**：访问 [obsidian-notes](https://github.com/lyl82/obsidian-notes) 仓库，检查最新的提交时间。

### B. 如何手动触发同步？
如果发现自动备份未运行，可以在 PowerShell 终端执行：
```powershell
powershell -ExecutionPolicy Bypass -File "d:\个人记录\obsidian-file\wjmber\LifeOS\auto-backup.ps1"
```

### C. 常见问题处理
*   **认证失败**：如果提示 `Permission denied`，说明 GitHub 登录状态过期。执行 `git push` 触发重新登录。
*   **网络问题**：脚本会自动跳过推送，并在下一次网络正常时重试。无需手动干预。

---

## 3. AI 移交协议 (AI Handoff Protocol)
*适用于后续接管 LifeOS 的其他 AI 助手*

### A. Skill 定义 (Skill Specification)
*   **能力名称**：`git-auto-backup`
*   **职责**：维护 LifeOS 物理数据的实时冗余。
*   **操作范围**：`LifeOS` 根目录下的 `.git` 目录及 `auto-backup.ps1`。

### B. 接管自检清单
当新 AI 接入时，必须检查：
1.  `git remote -v` 是否指向 `https://github.com/lyl82/obsidian-notes.git`。
2.  `auto-backup.ps1` 是否存在且路径正确。
3.  检查最近一次备份的时间戳（通过 `git log -1 --format=%cd`）。

### C. 脚本逻辑维护
脚本逻辑严禁修改以下核心原则：
1.  **先判断再提交**：必须先执行 `git diff --cached --quiet` 检查是否有改动，避免产生大量空提交。
2.  **静默运行**：在任务计划程序中运行时应保持静默，不弹出黑色窗口。

---

## 4. 维护规则 (Trigger Rules)

*   **IF** 发现连续 3 个小时没有 `auto backup` 提交记录
    *   **THEN** 提示用户检查“Windows 任务计划程序”服务是否正常运行。
*   **IF** 发现本地 `git push` 持续报错
    *   **THEN** 尝试引导用户在终端执行一次手动推送以检查具体报错信息。

---

## 5. 关键文件索引 (Key Links)
- 自动化脚本：[auto-backup.ps1](file:///d:/个人记录/obsidian-file/wjmber/LifeOS/auto-backup.ps1)
- 远程备份仓库：[obsidian-notes](https://github.com/lyl82/obsidian-notes)
- 环境配置文件：`.git/config`
