$ErrorActionPreference = "Stop"

$RepoRoot = "D:\Documents\04_GitRepos\get_jobs"
$JavaHome = "D:\Documents\04_GitRepos\env\jdk-21\jdk-21.0.10+7"
$GradleHome = "D:\Documents\04_GitRepos\env\.gradle"
$PlaywrightBrowsers = "D:\Documents\04_GitRepos\env\playwright"
$TmpDir = "D:\Documents\04_GitRepos\env\tmp"

if (!(Test-Path $RepoRoot)) {
  throw "RepoRoot not found: $RepoRoot"
}

if (!(Test-Path $JavaHome)) {
  $jdkBase = "D:\Documents\04_GitRepos\env\jdk-21"
  if (Test-Path $jdkBase) {
    $candidate = Get-ChildItem -Directory -Path $jdkBase | Sort-Object Name -Descending | Select-Object -First 1
    if ($null -ne $candidate) {
      $JavaHome = $candidate.FullName
    }
  }
}

if (!(Test-Path $JavaHome)) {
  throw "JAVA_HOME not found. Please unzip JDK21 under D: and update this script: $JavaHome"
}

$env:JAVA_HOME = $JavaHome
$env:GRADLE_USER_HOME = $GradleHome
$env:PLAYWRIGHT_BROWSERS_PATH = $PlaywrightBrowsers
$env:TEMP = $TmpDir
$env:TMP = $TmpDir

Set-Location $RepoRoot

New-Item -ItemType Directory -Force -Path "$RepoRoot\target\logs" | Out-Null
New-Item -ItemType Directory -Force -Path $GradleHome | Out-Null
New-Item -ItemType Directory -Force -Path $PlaywrightBrowsers | Out-Null
New-Item -ItemType Directory -Force -Path $TmpDir | Out-Null

$port6866 = Get-NetTCPConnection -State Listen -LocalPort 6866 -ErrorAction SilentlyContinue
if ($null -ne $port6866) {
  $pid = $port6866 | Select-Object -First 1 -ExpandProperty OwningProcess
  $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
  $name = if ($null -ne $proc) { $proc.ProcessName } else { "unknown" }
  throw "Port 6866 is already in use. PID=$pid Name=$name. Stop it first (likely UI-only jwebserver)."
}

$port8888 = Get-NetTCPConnection -State Listen -LocalPort 8888 -ErrorAction SilentlyContinue
if ($null -ne $port8888) {
  $pid = $port8888 | Select-Object -First 1 -ExpandProperty OwningProcess
  $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
  $name = if ($null -ne $proc) { $proc.ProcessName } else { "unknown" }
  throw "Port 8888 is already in use. PID=$pid Name=$name. Stop it first (or change server.port)."
}

$JarPath = "$RepoRoot\build\libs\get_jobs-0.0.1-SNAPSHOT.jar"
if (!(Test-Path $JarPath)) {
  & "$RepoRoot\gradlew.bat" build -x test
}

& "$env:JAVA_HOME\bin\java.exe" -jar $JarPath
