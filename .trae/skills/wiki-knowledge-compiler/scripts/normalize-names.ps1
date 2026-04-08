param(
    [Parameter(Mandatory = $true, ValueFromRemainingArguments = $true)]
    [string[]]$Titles
)

Set-StrictMode -Version Latest

. "$PSScriptRoot\common.ps1"

$items = foreach ($title in $Titles) {
    $normalized = Normalize-WikiFileName -Title $title
    [pscustomobject]@{
        input = $title
        normalized = $normalized
        changed = ($title -ne $normalized)
    }
}

Write-Output (ConvertTo-JsonText -InputObject $items)
