Param(
    [string]$RepoPath = "d:\个人记录\obsidian-file\wjmber\LifeOS"
)

Set-Location $RepoPath

$now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

git add -A

if (git diff --cached --quiet) {
    Write-Output "[$now] No changes to commit."
    exit 0
}

$commitMessage = "auto backup $now"
git commit -m $commitMessage

git rev-parse --abbrev-ref --symbolic-full-name "@{u}" *> $null

if ($LASTEXITCODE -ne 0) {
    Write-Output "[$now] No upstream configured, please run 'git push -u origin main' once."
    exit 0
}

git push

Write-Output "[$now] Backup committed and pushed."

