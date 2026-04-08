param(
    [Parameter(Mandatory = $true)][string]$RawRoot,
    [Parameter(Mandatory = $true)][string[]]$RawPaths,
    [Parameter(Mandatory = $true)][string]$Status
)

Set-StrictMode -Version Latest

. "$PSScriptRoot\common.ps1"

$resolvedRawRoot = (Resolve-Path $RawRoot).Path
$now = (Get-Date).ToString('s')

$results = foreach ($rawPath in $RawPaths) {
    $fullPath = if ([System.IO.Path]::IsPathRooted($rawPath)) { $rawPath } else { Join-Path $resolvedRawRoot $rawPath }
    $file = Get-Item -LiteralPath $fullPath
    $text = Get-FileText -Path $file.FullName
    $parsed = Get-FrontmatterData -Text $text

    $frontmatter = @{}
    foreach ($key in $parsed.frontmatter.Keys) {
        $frontmatter[$key] = $parsed.frontmatter[$key]
    }

    $hash = Get-CanonicalRawHash -Frontmatter $frontmatter -Body $parsed.body

    $statusKey = if ($frontmatter.ContainsKey('wiki_status')) { 'wiki_status' } elseif ($frontmatter.ContainsKey('wiki-tags')) { 'wiki-tags' } else { 'wiki_status' }

    $overridden = @($statusKey, 'wiki_content_hash', 'wiki_last_compiled')
    $out = [ordered]@{}
    $out[$statusKey] = $Status
    $out['wiki_content_hash'] = $hash
    $out['wiki_last_compiled'] = $now

    foreach ($key in $parsed.frontmatter.Keys) {
        if ($overridden -contains $key) {
            continue
        }
        $out[$key] = $parsed.frontmatter[$key]
    }

    $lines = @('---')
    foreach ($entry in $out.GetEnumerator()) {
        $k = [string]$entry.Key
        $v = $entry.Value
        if ($v -is [System.Collections.IList]) {
            $lines += ("{0}:" -f $k)
            foreach ($item in $v) {
                $lines += ("  - {0}" -f ([string]$item))
            }
        } else {
            $lines += ("{0}: {1}" -f $k, ([string]$v))
        }
    }
    $lines += '---'
    $frontmatterText = ($lines -join "`n")
    $updated = $frontmatterText + "`n`n" + $parsed.body.TrimStart("`r", "`n")

    if ($updated -ne $text) {
        Write-Utf8File -Path $file.FullName -Content $updated
    }

    [pscustomobject]@{
        path = $file.FullName
        relative_path = Get-RelativePathText -BasePath $resolvedRawRoot -TargetPath $file.FullName
        status_key = $statusKey
        status = $Status
        wiki_content_hash = $hash
        wiki_last_compiled = $now
        updated = ($updated -ne $text)
    }
}

Write-Output (ConvertTo-JsonText -InputObject $results)
