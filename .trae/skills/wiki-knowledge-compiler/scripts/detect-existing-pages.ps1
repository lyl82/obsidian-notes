param(
    [Parameter(Mandatory = $true)][string]$WikiRoot,
    [Parameter(Mandatory = $true)][string[]]$RawPaths
)

Set-StrictMode -Version Latest

. "$PSScriptRoot\common.ps1"

$resolvedWikiRoot = (Resolve-Path $WikiRoot).Path
$summariesRoot = Join-Path $resolvedWikiRoot 'summaries'
$conceptsRoot = Join-Path $resolvedWikiRoot 'concepts'
$indexPath = Join-Path $resolvedWikiRoot 'index.md'

$items = foreach ($rawPath in $RawPaths) {
    $rawItem = Get-Item -LiteralPath $rawPath
    $rawText = Get-FileText -Path $rawItem.FullName
    $parsed = Get-FrontmatterData -Text $rawText
    $frontmatter = @{}
    foreach ($key in $parsed.frontmatter.Keys) {
        $frontmatter[$key] = $parsed.frontmatter[$key]
    }

    $summaryFileName = Get-SummaryFileNameForRaw -RawFileName $rawItem.Name
    $summaryPath = Join-Path $summariesRoot $summaryFileName

    $conceptNames = @()
    if ($frontmatter.ContainsKey('wiki_concepts')) {
        $value = $frontmatter['wiki_concepts']
        if ($value -is [System.Collections.IList]) {
            $conceptNames = @($value)
        } elseif ($value) {
            $conceptNames = @($value)
        }
    }

    $conceptStates = @(foreach ($conceptName in $conceptNames) {
        $conceptFileName = (Normalize-WikiFileName -Title ([string]$conceptName)) + '.md'
        $conceptPath = Join-Path $conceptsRoot $conceptFileName
        [pscustomobject]@{
            concept = [string]$conceptName
            normalized_file = $conceptFileName
            exists = (Test-Path -LiteralPath $conceptPath)
            path = $conceptPath
        }
    })

    [pscustomobject]@{
        raw_path = $rawItem.FullName
        summary = [pscustomobject]@{
            file_name = $summaryFileName
            exists = (Test-Path -LiteralPath $summaryPath)
            path = $summaryPath
        }
        concepts = $conceptStates
        index = [pscustomobject]@{
            exists = (Test-Path -LiteralPath $indexPath)
            path = $indexPath
        }
    }
}

Write-Output (ConvertTo-JsonText -InputObject $items)
