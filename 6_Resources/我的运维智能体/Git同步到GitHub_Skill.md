# Skill：将 LifeOS 仓库同步到 GitHub（以当天日期作为版本记录）

## 一、任务背景与目标

### 1.1 任务概述
本任务旨在建立 LifeOS 知识库的版本控制与远程备份机制，确保本地笔记内容能够安全、定期地同步到 GitHub 仓库。

### 1.2 核心目标
- 将本地仓库 `d:\个人记录\obsidian-file\wjmber\LifeOS` 推送到 GitHub 远程仓库
- 自动以当天日期作为版本标签，便于追溯和回滚
- 配置 `.gitignore` 排除大型文件（归档目录、图片、视频等）

### 1.3 项目环境
- **本地仓库路径**：`d:\个人记录\obsidian-file\wjmber\LifeOS`
- **远程仓库**：`https://github.com/lyl82/obsidian-notes.git`
- **默认分支**：`main`
- **操作系统**：Windows（PowerShell 环境）

---

## 二、前置条件检查清单

### 2.1 环境依赖
| 依赖项 | 要求 | 验证方法 |
|--------|------|----------|
| Git | 已安装 | `git --version` |
| PowerShell | 5.1 及以上 | `$PSVersionTable.PSVersion` |
| 网络连接 | 可访问 GitHub | `Invoke-WebRequest https://github.com` |

### 2.2 仓库状态检查
```powershell
Set-Location "d:\个人记录\obsidian-file\wjmber\LifeOS"

# 检查是否在 Git 仓库内
git rev-parse --is-inside-work-tree

# 检查当前分支
git branch --show-current

# 检查远程配置
git remote -v

# 检查工作区状态
git status
```

### 2.3 凭证准备
- **HTTPS 方式**：准备 GitHub 账号密码或 Personal Access Token（PAT）
- **SSH 方式**：确保已配置 SSH 密钥并添加到 GitHub

---

## 三、标准同步流程

### 3.1 完整同步脚本（PowerShell）
```powershell
# ==============================================
# LifeOS GitHub 同步脚本
# 执行前请确保已完成前置条件检查
# ==============================================

Set-Location "d:\个人记录\obsidian-file\wjmber\LifeOS"

# 1. 获取当天日期
$date = Get-Date -Format "yyyy-MM-dd"
Write-Host "[$date] 开始同步 LifeOS 仓库..." -ForegroundColor Cyan

# 2. 拉取远程最新变更（避免冲突）
Write-Host "步骤 1: 拉取远程最新代码..." -ForegroundColor Yellow
git pull --rebase origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "警告：拉取失败，可能存在冲突需要手动解决" -ForegroundColor Yellow
}

# 3. 添加所有变更
Write-Host "步骤 2: 暂存所有文件变更..." -ForegroundColor Yellow
git add -A

# 4. 提交变更（以日期作为提交信息）
Write-Host "步骤 3: 提交变更..." -ForegroundColor Yellow
git commit -m "Sync LifeOS - $date"

# 5. 创建版本标签
Write-Host "步骤 4: 创建版本标签 $date..." -ForegroundColor Yellow
git tag -a $date -m "Version $date"

# 6. 推送到远程仓库
Write-Host "步骤 5: 推送代码到 GitHub..." -ForegroundColor Yellow
git push origin main

# 7. 推送标签到远程
Write-Host "步骤 6: 推送标签到 GitHub..." -ForegroundColor Yellow
git push origin $date

Write-Host "[$date] 同步完成！" -ForegroundColor Green
```

### 3.2 无变更时的空提交（保持每日版本记录）
```powershell
Set-Location "d:\个人记录\obsidian-file\wjmber\LifeOS"
$date = Get-Date -Format "yyyy-MM-dd"

# 检查是否有变更
$hasChanges = git status --porcelain=v1
if (-not $hasChanges) {
    Write-Host "无代码变更，创建空提交保持版本记录..." -ForegroundColor Yellow
    git commit --allow-empty -m "Daily sync - $date"
}

git tag -a $date -m "Version $date"
git push origin main
git push origin $date
```

---

## 四、.gitignore 配置说明

### 4.1 配置目的
排除以下类型文件，减小仓库体积：
- 归档目录（历史记录）
- 大型媒体文件（图片、视频、音频）
- 可执行文件和安装包
- Obsidian 缓存文件

### 4.2 配置内容
```gitignore
# 归档目录（不上传历史记录）
7_Archive/

# 图片文件
*.png
*.jpg
*.jpeg
*.gif
*.bmp
*.tiff
*.tif
*.webp
*.svg
*.ico

# 视频文件
*.mp4
*.mov
*.avi
*.mkv
*.flv
*.wmv
*.webm
*.mpeg
*.mpg

# 音频文件
*.mp3
*.wav
*.flac
*.ogg
*.m4a

# 大型文档和压缩文件
*.pdf
*.zip
*.rar
*.7z
*.tar
*.gz
*.bz2

# 可执行文件和安装包
*.exe
*.dll
*.msi
*.dmg

# Obsidian 缓存文件
.obsidian/
```

### 4.3 更新 .gitignore 后的处理
```powershell
# 若 .gitignore 更新前已有被忽略的文件被跟踪，需要清除缓存
git rm -r --cached 7_Archive  # 移除归档目录的跟踪
git add .gitignore
git commit -m "Update .gitignore - exclude archive and media files"
git push origin main
```

---

## 五、常见故障排查（优先级从高到低）

### 5.1 Git 代理配置问题（最常见）

**现象**：
- `git push` / `git ls-remote` 报 `Failed to connect`、`Connection was reset`
- 浏览器访问 GitHub 正常，但 Git 无法连接

**检查命令**：
```powershell
git config --global --get http.proxy
git config --global --get https.proxy
git config --get http.proxy
git config --get https.proxy
```

**处理方法**：
```powershell
# 方案1：取消 Git 代理（推荐）
git config --global --unset-all http.proxy
git config --global --unset-all https.proxy
git config --unset-all http.proxy
git config --unset-all https.proxy

# 方案2：配置正确的代理（如需使用代理）
# 先验证代理端口
Test-NetConnection 127.0.0.1 -Port 1080
# 配置代理
git config --global http.proxy http://127.0.0.1:1080
git config --global https.proxy http://127.0.0.1:1080
```

### 5.2 HTTP/2 或 TLS 兼容问题

**处理方法**：
```powershell
git config http.version HTTP/1.1
git config --global http.sslBackend schannel
```

### 5.3 认证问题

**现象**：报 `Authentication failed` / `could not read Username` / `403`

**处理方法**：

**方案1：使用凭证管理器（推荐）**
```powershell
git config --global credential.helper manager
```
首次推送时会弹出凭证输入窗口，输入后自动保存。

**方案2：使用 SSH（彻底避免 token）**
```powershell
# 生成 SSH 密钥（一路回车）
ssh-keygen -t ed25519 -C "your_email@example.com" -f $env:USERPROFILE\.ssh\id_ed25519 -N ""

# 查看公钥内容
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```
将输出的公钥添加到 GitHub：Settings → SSH and GPG keys → New SSH key

切换远程地址：
```powershell
git remote set-url origin git@github.com:lyl82/obsidian-notes.git
```

### 5.4 标签已存在问题

**现象**：`fatal: tag '2026-05-04' already exists`

**处理方法**：
```powershell
$date = Get-Date -Format "yyyy-MM-dd"

# 删除本地标签
git tag -d $date

# 删除远程标签
git push origin :refs/tags/$date

# 重新创建并推送
git tag -a $date -m $date
git push origin $date
```

---

## 六、验证与确认

### 6.1 同步后验证清单
```powershell
Set-Location "d:\个人记录\obsidian-file\wjmber\LifeOS"

# 1. 检查本地状态
git status

# 2. 查看最新提交
git log -1 --oneline

# 3. 验证远程分支
git ls-remote origin main

# 4. 验证标签
git tag -l

# 5. 验证远程标签
git ls-remote --tags origin
```

### 6.2 GitHub 页面验证
1. 访问 `https://github.com/lyl82/obsidian-notes`
2. 确认 `main` 分支已更新
3. 检查 **Releases** 或 **Tags** 页面确认标签已创建

---

## 七、安全边界与注意事项

### 7.1 敏感信息防护
- **严禁**提交密钥、token、密码、浏览器导出数据
- 任何需要凭证的步骤，仅通过系统凭证管理器或手动输入
- 敏感配置文件应加入 `.gitignore`

### 7.2 标签使用规范
- 标签名固定格式：`yyyy-MM-dd`
- 标签与提交信息保持一致
- 避免重复创建同名标签

### 7.3 备份建议
- 定期检查 GitHub 仓库状态
- 重要变更后及时验证同步结果
- 考虑启用 GitHub 的自动备份功能

---

## 八、附录：快捷操作脚本

### 8.1 一键同步脚本（推荐保存为 `sync-lifeos.ps1`）
```powershell
<#
.SYNOPSIS
    LifeOS GitHub 同步脚本
.DESCRIPTION
    自动同步 LifeOS 仓库到 GitHub，并创建日期标签
#>

$repoPath = "d:\个人记录\obsidian-file\wjmber\LifeOS"
$date = Get-Date -Format "yyyy-MM-dd"

try {
    Set-Location $repoPath -ErrorAction Stop
    
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  LifeOS GitHub 同步脚本" -ForegroundColor Cyan
    Write-Host "  Date: $date" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan

    # 拉取更新
    Write-Host "[1/6] 拉取远程更新..." -ForegroundColor Yellow
    git pull --rebase origin main

    # 添加变更
    Write-Host "`n[2/6] 暂存文件..." -ForegroundColor Yellow
    git add -A

    # 提交
    Write-Host "`n[3/6] 提交变更..." -ForegroundColor Yellow
    git commit -m "Sync LifeOS - $date"

    # 创建标签
    Write-Host "`n[4/6] 创建标签..." -ForegroundColor Yellow
    git tag -a $date -m "Version $date"

    # 推送代码
    Write-Host "`n[5/6] 推送代码..." -ForegroundColor Yellow
    git push origin main

    # 推送标签
    Write-Host "`n[6/6] 推送标签..." -ForegroundColor Yellow
    git push origin $date

    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "  同步成功！" -ForegroundColor Green
    Write-Host "========================================`n" -ForegroundColor Green

} catch {
    Write-Host "`n同步失败：$_" -ForegroundColor Red
    exit 1
}
```

### 8.2 脚本使用方法
```powershell
# 保存脚本后，在 PowerShell 中执行
.\sync-lifeos.ps1

# 若遇到执行策略限制，运行：
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

**文档版本**：v1.0  
**创建日期**：2026-05-04  
**适用场景**：LifeOS 知识库日常同步
