param(
    [Parameter(Mandatory = $true)][string]$ChangesFile,
    [switch]$DryRun
)

Set-StrictMode -Version Latest

. "$PSScriptRoot\common.ps1"

$resolvedChangesFile = (Resolve-Path $ChangesFile).Path
$payload = Get-FileText -Path $resolvedChangesFile | ConvertFrom-Json

$changes = @()
if ($payload -is [System.Array]) {
    $changes = @($payload)
} elseif ($payload.PSObject.Properties.Name -contains 'changes') {
    $changes = @($payload.changes)
}

if (-not $changes -or $changes.Count -eq 0) {
    throw "No changes found in manifest: $resolvedChangesFile"
}

$results = foreach ($change in $changes) {
    if (-not $change.path) {
        throw "Each change item must include 'path'."
    }
    if ($null -eq $change.content) {
        throw "Each change item must include 'content'."
    }

    $targetPath = [string]$change.path
    $content = [string]$change.content
    $exists = Test-Path -LiteralPath $targetPath
    $before = if ($exists) { Get-FileText -Path $targetPath } else { $null }
    $action = if (-not $exists) { 'create' } elseif ($before -eq $content) { 'unchanged' } else { 'update' }

    if (-not $DryRun -and $action -ne 'unchanged') {
        Write-Utf8File -Path $targetPath -Content $content
    }

    [pscustomobject]@{
        path = $targetPath
        exists_before = $exists
        action = $action
        wrote = (-not $DryRun -and $action -ne 'unchanged')
        dry_run = [bool]$DryRun
        bytes = [System.Text.Encoding]::UTF8.GetByteCount($content)
    }
}

Write-Output (ConvertTo-JsonText -InputObject $results)
