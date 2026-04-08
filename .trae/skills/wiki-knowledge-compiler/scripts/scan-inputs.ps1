param(
    [Parameter(Mandatory = $true)][string]$RawRoot,
    [string[]]$Paths
)

Set-StrictMode -Version Latest

. "$PSScriptRoot\common.ps1"

$resolvedRoot = (Resolve-Path $RawRoot).Path

if ($Paths -and $Paths.Count -gt 0) {
    $targets = foreach ($path in $Paths) {
        if ([System.IO.Path]::IsPathRooted($path)) {
            Get-Item -LiteralPath $path
        } else {
            Get-Item -LiteralPath (Join-Path $resolvedRoot $path)
        }
    }
} else {
    $targets = Get-ChildItem -LiteralPath $resolvedRoot -File
}

$items = foreach ($file in $targets) {
    $text = Get-FileText -Path $file.FullName
    $parsed = Get-FrontmatterData -Text $text
    $frontmatter = @{}
    foreach ($key in $parsed.frontmatter.Keys) {
        $frontmatter[$key] = $parsed.frontmatter[$key]
    }

    $canonicalHash = Get-CanonicalRawHash -Frontmatter $frontmatter -Body $parsed.body
    $status = Get-NormalizedWikiStatus -Frontmatter $frontmatter
    $storedHash = if ($frontmatter.ContainsKey('wiki_content_hash')) { [string]$frontmatter['wiki_content_hash'] } else { '' }
    $decision = 'process'
    $reason = 'pending_or_untracked'

    if ($status -eq 'skipped') {
        $decision = 'skip'
        $reason = 'wiki_status_skipped'
    } elseif ($status -eq 'done' -and $storedHash -and $storedHash -eq $canonicalHash) {
        $decision = 'skip'
        $reason = 'done_and_hash_unchanged'
    } elseif ($status -eq 'done' -and $storedHash -and $storedHash -ne $canonicalHash) {
        $decision = 'process'
        $reason = 'stale_hash_changed'
    } elseif ($status -eq 'stale') {
        $decision = 'process'
        $reason = 'wiki_status_stale'
    }

    [pscustomobject]@{
        path = $file.FullName
        relative_path = Get-RelativePathText -BasePath $resolvedRoot -TargetPath $file.FullName
        file_name = $file.Name
        extension = $file.Extension
        has_frontmatter = $parsed.has_frontmatter
        frontmatter = $frontmatter
        canonical_hash = $canonicalHash
        wiki_status = $status
        decision = $decision
        reason = $reason
        summary_target = Get-SummaryFileNameForRaw -RawFileName $file.Name
    }
}

Write-Output (ConvertTo-JsonText -InputObject $items)
