$ErrorActionPreference = "Stop"

$RepoRoot = "D:\Documents\04_GitRepos\get_jobs"
$LogDir = "$RepoRoot\target\logs"
$LogFile = "$LogDir\get-jobs.log"

if (!(Test-Path $RepoRoot)) {
  throw "RepoRoot not found: $RepoRoot"
}

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
if (!(Test-Path $LogFile)) {
  New-Item -ItemType File -Path $LogFile | Out-Null
}

Get-Content -Path $LogFile -Wait -Tail 200

