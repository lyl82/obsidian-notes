# Skill：将 LifeOS 仓库同步到 GitHub（以当天日期作为版本记录）

## 目标

- 将本地仓库 `d:\个人记录\obsidian-file\wjmber\LifeOS` 推送到 GitHub
- 版本记录的名称使用当天日期（建议作为提交信息）

## 输入

- 仓库根目录：`d:\个人记录\obsidian-file\wjmber\LifeOS`
- 远程：默认 `origin`
- 分支：默认 `main`
- 当天日期格式：`yyyy-MM-dd`

## 输出

- GitHub `origin/main` 更新到最新提交
- 本地新增 1 条提交记录（提交信息为当天日期）

## 标准流程（PowerShell）

```powershell
Set-Location "d:\个人记录\obsidian-file\wjmber\LifeOS"

git rev-parse --is-inside-work-tree
git branch --show-current
git remote -v

git pull --rebase origin main

$date = Get-Date -Format "yyyy-MM-dd"

git add -A
git commit -m $date

git push origin main
```

## 无变更也要留版本记录

```powershell
Set-Location "d:\个人记录\obsidian-file\wjmber\LifeOS"
$date = Get-Date -Format "yyyy-MM-dd"

git status --porcelain=v1
git commit --allow-empty -m $date
git push origin main
```

## 初次绑定/检查远程

```powershell
Set-Location "d:\个人记录\obsidian-file\wjmber\LifeOS"
git remote -v
git remote set-url origin https://github.com/<owner>/<repo>.git
```

## 常见故障排查（优先级从高到低）

### 1) Git 被代理配置卡住（最常见）

现象：
- `git push` / `git ls-remote` 报 `Failed to connect`、`Connection was reset`、`Empty reply from server`
- 但浏览器或 `Invoke-WebRequest https://github.com` 是正常的

检查：

```powershell
git config --global --get http.proxy
git config --global --get https.proxy
git config --get http.proxy
git config --get https.proxy
```

处理（取消 Git 代理）：

```powershell
git config --global --unset-all http.proxy
git config --global --unset-all https.proxy
git config --unset-all http.proxy
git config --unset-all https.proxy
```

处理（需要本地代理时）：

- 先确认代理端口真的在监听（示例：1080）：

```powershell
Test-NetConnection 127.0.0.1 -Port 1080
```

- 再把 Git 代理指向实际可用的代理地址（示例）：

```powershell
git config --global http.proxy  http://127.0.0.1:1080
git config --global https.proxy http://127.0.0.1:1080
```

### 2) HTTP/2 或 TLS 兼容问题

```powershell
git config http.version HTTP/1.1
git config --global http.sslBackend schannel
```

### 3) 认证问题

现象：
- 报 `Authentication failed` / `could not read Username` / `403`

处理建议：
- HTTPS：使用 Git Credential Manager 或 Personal Access Token（PAT），不要把 token 写入仓库文件
- SSH：改用 SSH remote，并确保已配置密钥

## 验证清单

```powershell
Set-Location "d:\个人记录\obsidian-file\wjmber\LifeOS"
git status
git log -1 --oneline
git ls-remote origin main
```

## 安全边界

- 不提交密钥、token、密码、浏览器导出的敏感数据
- 任何需要凭证的步骤，只通过系统凭证管理器或手动输入，不写进仓库
