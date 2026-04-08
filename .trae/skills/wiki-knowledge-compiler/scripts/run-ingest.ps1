param(
    [Parameter(Mandatory = $true)][string]$RawRoot,
    [Parameter(Mandatory = $true)][string]$WikiRoot,
    [string[]]$RawPaths,
    [string]$ChangesFile
)

Set-StrictMode -Version Latest

. "$PSScriptRoot\common.ps1"

$scanJson = & "$PSScriptRoot\scan-inputs.ps1" -RawRoot $RawRoot -Paths $RawPaths
$scan = @($scanJson | ConvertFrom-Json)
$toProcess = @($scan | Where-Object { $_.decision -eq 'process' })
$rawCount = ($toProcess | Measure-Object).Count

$writeCount = 0
$validate = 'skip'
$notes = ''

if ($ChangesFile) {
    $applyJson = & "$PSScriptRoot\apply-changes.ps1" -ChangesFile $ChangesFile
    $apply = @($applyJson | ConvertFrom-Json)
    $writeCount = (@($apply | Where-Object { $_.action -eq 'create' -or $_.action -eq 'update' }) | Measure-Object).Count

    $validateJson = & "$PSScriptRoot\validate-wiki.ps1" -WikiRoot $WikiRoot
    $validateResults = @($validateJson | ConvertFrom-Json)
    $failCount = (@($validateResults | Where-Object { -not $_.valid }) | Measure-Object).Count
    $validate = if ($failCount -eq 0) { 'pass' } else { 'fail' }
    if ($failCount -gt 0) {
        $notes = "validate_failed=$failCount"
    } else {
        $rawRelativePaths = @($toProcess | Select-Object -ExpandProperty relative_path)
        & "$PSScriptRoot\update-raw-status.ps1" -RawRoot $RawRoot -RawPaths $rawRelativePaths -Status 'done' | Out-Null
    }
} else {
    $notes = 'no_changes_file'
}

& "$PSScriptRoot\append-log.ps1" -WikiRoot $WikiRoot -Operation 'ingest' -RawCount $rawCount -WriteCount $writeCount -Validate $validate -Notes $notes | Out-Null

Write-Output (ConvertTo-JsonText -InputObject ([pscustomobject]@{
    raw_scanned = ($scan | Measure-Object).Count
    raw_to_process = $rawCount
    write_count = $writeCount
    validate = $validate
    notes = $notes
}))
