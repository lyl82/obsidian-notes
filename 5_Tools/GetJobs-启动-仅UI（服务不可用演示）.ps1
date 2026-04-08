$ErrorActionPreference = "Stop"

$RepoRoot = "D:\Documents\04_GitRepos\get_jobs"
$JavaHome = "D:\Documents\04_GitRepos\env\jdk-21\jdk-21.0.10+7"
$DistDir = "$RepoRoot\src\main\resources\dist"
$Port = 6866

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

if (!(Test-Path $DistDir)) {
  throw "dist directory not found: $DistDir"
}

$env:JAVA_HOME = $JavaHome
Set-Location $RepoRoot

$portInUse = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue
if ($null -ne $portInUse) {
  $pid = $portInUse | Select-Object -First 1 -ExpandProperty OwningProcess
  $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
  $name = if ($null -ne $proc) { $proc.ProcessName } else { "unknown" }
  throw "Port $Port is already in use. PID=$pid Name=$name."
}

& "$env:JAVA_HOME\bin\jwebserver.exe" -d $DistDir -p $Port -b 0.0.0.0
