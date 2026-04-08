param(
    [Parameter(Mandatory = $true)][string]$WikiRoot,
    [Parameter(Mandatory = $true)][string]$Operation,
    [Parameter(Mandatory = $true)][int]$RawCount,
    [Parameter(Mandatory = $true)][int]$WriteCount,
    [Parameter(Mandatory = $true)][string]$Validate,
    [string]$Notes = ''
)

Set-StrictMode -Version Latest

. "$PSScriptRoot\common.ps1"

$resolvedWikiRoot = (Resolve-Path $WikiRoot).Path
$logPath = Join-Path $resolvedWikiRoot 'log.md'

if (-not (Test-Path -LiteralPath $logPath)) {
    $templatePath = Join-Path (Join-Path (Split-Path -Parent $PSScriptRoot) 'templates') 'log.template.md'
    $content = Get-FileText -Path $templatePath
    $content = $content.Replace('<YYYY-MM-DD>', (Get-Date).ToString('yyyy-MM-dd'))
    Write-Utf8File -Path $logPath -Content $content
}

$time = (Get-Date).ToString('s')
$safeNotes = $Notes.Replace("`r", ' ').Replace("`n", ' ').Trim()
$line = "| $time | $Operation | $RawCount | $WriteCount | $Validate | $safeNotes |"
Append-Utf8Line -Path $logPath -Line $line

Write-Output (ConvertTo-JsonText -InputObject ([pscustomobject]@{
    path = $logPath
    appended = $true
    line = $line
}))
