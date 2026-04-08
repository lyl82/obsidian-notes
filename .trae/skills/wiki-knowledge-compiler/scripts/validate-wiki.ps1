param(
    [Parameter(Mandatory = $true)][string]$WikiRoot,
    [string[]]$Paths
)

Set-StrictMode -Version Latest

. "$PSScriptRoot\common.ps1"

function Get-DocumentKind {
    param(
        [Parameter(Mandatory = $true)][string]$WikiRootPath,
        [Parameter(Mandatory = $true)][string]$FilePath
    )

    $relative = Get-RelativePathText -BasePath $WikiRootPath -TargetPath $FilePath
    if ($relative -eq 'index.md') { return 'index' }
    if ($relative.StartsWith("summaries$([System.IO.Path]::DirectorySeparatorChar)")) { return 'summary' }
    if ($relative.StartsWith("concepts$([System.IO.Path]::DirectorySeparatorChar)")) { return 'concept' }
    return 'unknown'
}

function Test-HeadingSet {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string[]]$Headings
    )

    $issues = @()
    foreach ($heading in $Headings) {
        $pattern = "(?m)^##\s+$([regex]::Escape($heading))\s*$"
        if (-not [regex]::IsMatch($Text, $pattern)) {
            $issues += "missing_heading:$heading"
        }
    }
    return $issues
}

function Get-TemplateHeadings {
    param(
        [Parameter(Mandatory = $true)][string]$ScriptRoot,
        [Parameter(Mandatory = $true)][string]$DocumentKind
    )

    $templateName = switch ($DocumentKind) {
        'summary' { 'summary.template.md' }
        'concept' { 'concept.template.md' }
        'index' { 'index.template.md' }
        default { $null }
    }

    if (-not $templateName) {
        return @()
    }

    $templatePath = Join-Path (Join-Path (Split-Path -Parent $ScriptRoot) 'templates') $templateName
    $templateText = Get-FileText -Path $templatePath
    $matches = [regex]::Matches($templateText, '(?m)^##\s+(.+?)\s*$')
    $headings = @()
    foreach ($match in $matches) {
        $headings += $match.Groups[1].Value.Trim()
    }
    return $headings
}

function Get-LinkValidationIssues {
    param(
        [Parameter(Mandatory = $true)][string]$WikiRootPath,
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string]$DocumentKind,
        [Parameter(Mandatory = $true)][string]$Text
    )

    $issues = @()
    $matches = [regex]::Matches($Text, '\[\[\s*@?([^\]]+?)\s*\]\]')
    foreach ($match in $matches) {
        $rawTarget = $match.Groups[1].Value.Trim()
        if ([string]::IsNullOrWhiteSpace($rawTarget)) {
            continue
        }

        $target = $rawTarget
        if ($target.StartsWith('@')) {
            $target = $target.Substring(1).Trim()
        }

        if ($target.StartsWith('0_Inbox/Clippings') -or $target.StartsWith('0_Inbox\Clippings')) {
            continue
        }

        $candidates = @()
        if ($target -match '[\\/]') {
            $normalizedTarget = $target.Replace('/', [System.IO.Path]::DirectorySeparatorChar).Replace('\', [System.IO.Path]::DirectorySeparatorChar)
            $candidate = Join-Path $WikiRootPath $normalizedTarget
            if (-not $candidate.ToLowerInvariant().EndsWith('.md')) {
                $candidate += '.md'
            }
            $candidates += $candidate
        } else {
            $candidates += Join-Path (Join-Path $WikiRootPath 'concepts') ($target + '.md')
            $candidates += Join-Path (Join-Path $WikiRootPath 'summaries') ($target + '.md')
            $candidates += Join-Path $WikiRootPath ($target + '.md')
        }

        $exists = $false
        foreach ($candidate in $candidates | Select-Object -Unique) {
            if (Test-Path -LiteralPath $candidate) {
                $exists = $true
                break
            }
        }

        if (-not $exists) {
            $issues += "missing_link_target:$target"
        }
    }

    return $issues
}

$resolvedWikiRoot = (Resolve-Path $WikiRoot).Path

if ($Paths -and $Paths.Count -gt 0) {
    $targets = foreach ($path in $Paths) {
        if ([System.IO.Path]::IsPathRooted($path)) {
            Get-Item -LiteralPath $path
        } else {
            Get-Item -LiteralPath (Join-Path $resolvedWikiRoot $path)
        }
    }
} else {
    $targets = @()
    $summariesDir = Join-Path $resolvedWikiRoot 'summaries'
    if (Test-Path -LiteralPath $summariesDir) {
        $targets += Get-ChildItem -LiteralPath $summariesDir -File -Filter '*.md'
    }
    $conceptsDir = Join-Path $resolvedWikiRoot 'concepts'
    if (Test-Path -LiteralPath $conceptsDir) {
        $targets += Get-ChildItem -LiteralPath $conceptsDir -File -Filter '*.md'
    }
    $indexPath = Join-Path $resolvedWikiRoot 'index.md'
    if (Test-Path -LiteralPath $indexPath) {
        $targets += Get-Item -LiteralPath $indexPath
    }
}

$results = foreach ($file in $targets) {
    $text = Get-FileText -Path $file.FullName
    $parsed = Get-FrontmatterData -Text $text
    $kind = Get-DocumentKind -WikiRootPath $resolvedWikiRoot -FilePath $file.FullName
    $issues = @()

    if (-not $parsed.has_frontmatter) {
        $issues += 'missing_frontmatter'
    }

    $frontmatter = @{}
    foreach ($key in $parsed.frontmatter.Keys) {
        $frontmatter[$key] = $parsed.frontmatter[$key]
    }

    if (-not $frontmatter.ContainsKey('title')) {
        $issues += 'missing_frontmatter_title'
    }

    if (-not $frontmatter.ContainsKey('tags')) {
        $issues += 'missing_frontmatter_tags'
    }

    switch ($kind) {
        'summary' {
            $issues += Test-HeadingSet -Text $text -Headings (Get-TemplateHeadings -ScriptRoot $PSScriptRoot -DocumentKind $kind)
        }
        'concept' {
            $issues += Test-HeadingSet -Text $text -Headings (Get-TemplateHeadings -ScriptRoot $PSScriptRoot -DocumentKind $kind)
        }
        'index' {
            $issues += Test-HeadingSet -Text $text -Headings (Get-TemplateHeadings -ScriptRoot $PSScriptRoot -DocumentKind $kind)
        }
        default {
            $issues += 'unknown_document_kind'
        }
    }

    $issues += Get-LinkValidationIssues -WikiRootPath $resolvedWikiRoot -FilePath $file.FullName -DocumentKind $kind -Text $text

    [pscustomobject]@{
        path = $file.FullName
        relative_path = Get-RelativePathText -BasePath $resolvedWikiRoot -TargetPath $file.FullName
        kind = $kind
        valid = ($issues.Count -eq 0)
        issue_count = $issues.Count
        issues = $issues
    }
}

Write-Output (ConvertTo-JsonText -InputObject $results)
