Set-StrictMode -Version Latest

function Get-FileText {
    param(
        [Parameter(Mandatory = $true)][string]$Path
    )
    return [System.IO.File]::ReadAllText($Path, [System.Text.UTF8Encoding]::UTF8)
}

function Get-FrontmatterData {
    param(
        [Parameter(Mandatory = $true)][string]$Text
    )

    $result = [ordered]@{
        frontmatter = [ordered]@{}
        body = $Text
        has_frontmatter = $false
    }

    if (-not $Text.StartsWith("---")) {
        return [pscustomobject]$result
    }

    $normalized = $Text -replace "`r`n", "`n"
    $match = [regex]::Match($normalized, '^(?s)---\n(.*?)\n---\n?(.*)$')
    if (-not $match.Success) {
        return [pscustomobject]$result
    }

    $frontmatterText = $match.Groups[1].Value
    $body = $match.Groups[2].Value
    $lines = $frontmatterText -split "`n"
    $data = [ordered]@{}
    $currentKey = $null

    foreach ($line in $lines) {
        if ($line -match '^\s*-\s+(.*)$' -and $currentKey) {
            if (-not $data.Contains($currentKey)) {
                $data[$currentKey] = @()
            }
            if ($data[$currentKey] -isnot [System.Collections.IList]) {
                $data[$currentKey] = @($data[$currentKey])
            }
            $data[$currentKey] += $matches[1].Trim()
            continue
        }

        if ($line -match '^([A-Za-z0-9_\-]+)\s*:\s*(.*)$') {
            $currentKey = $matches[1]
            $value = $matches[2].Trim()
            if ($value -eq '') {
                $data[$currentKey] = @()
            } else {
                $data[$currentKey] = $value.Trim('"')
            }
            continue
        }

        $currentKey = $null
    }

    $result.frontmatter = $data
    $result.body = $body
    $result.has_frontmatter = $true
    return [pscustomobject]$result
}

function Update-FrontmatterField {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string]$Key,
        [Parameter(Mandatory = $true)][string]$Value
    )

    $normalized = $Text -replace "`r`n", "`n"

    if (-not $normalized.StartsWith("---`n")) {
        $line = ('{0}: {1}' -f $Key, $Value)
        $fm = "---`n$line`n---`n`n"
        return ($fm + $Text)
    }

    $match = [regex]::Match($normalized, '^(?s)---\n(.*?)\n---\n?(.*)$')
    if (-not $match.Success) {
        $line = ('{0}: {1}' -f $Key, $Value)
        $fm = "---`n$line`n---`n`n"
        return ($fm + $Text)
    }

    $frontmatterText = $match.Groups[1].Value
    $body = $match.Groups[2].Value

    $pattern = "(?i)^$([regex]::Escape($Key))\\s*:\\s*.*$"
    $lines = @($frontmatterText -split "`n")
    $filtered = @()
    foreach ($line in $lines) {
        if ($line -match $pattern) {
            continue
        }
        $filtered += $line
    }

    $line = ('{0}: {1}' -f $Key, $Value)
    $frontmatterText = ($line + "`n" + (($filtered -join "`n").TrimEnd("`n")))

    return ("---`n$frontmatterText`n---`n$body")
}

function Get-CanonicalRawHash {
    param(
        [Parameter(Mandatory = $true)][hashtable]$Frontmatter,
        [Parameter(Mandatory = $true)][string]$Body
    )

    $clean = [ordered]@{}
    foreach ($key in $Frontmatter.Keys) {
        if ($key -notmatch '^wiki_' -and $key -ne 'wiki-tags') {
            $clean[$key] = $Frontmatter[$key]
        }
    }

    $payload = @{
        frontmatter = $clean
        body = $Body
    } | ConvertTo-Json -Depth 10 -Compress

    $bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $hash = $sha.ComputeHash($bytes)
        return ([BitConverter]::ToString($hash)).Replace('-', '').ToLowerInvariant()
    } finally {
        $sha.Dispose()
    }
}

function Get-NormalizedWikiStatus {
    param(
        [Parameter(Mandatory = $true)][hashtable]$Frontmatter
    )

    $value = $null
    if ($Frontmatter.ContainsKey('wiki_status')) {
        $value = $Frontmatter['wiki_status']
    } elseif ($Frontmatter.ContainsKey('wiki-tags')) {
        $value = $Frontmatter['wiki-tags']
    }

    if ($null -eq $value) {
        return 'pending'
    }

    if ($value -is [System.Collections.IList]) {
        if ($value.Count -eq 0) {
            return 'pending'
        }
        $value = $value[0]
    }

    $normalized = ([string]$value).Trim().ToLowerInvariant()
    if ([string]::IsNullOrWhiteSpace($normalized)) {
        return 'pending'
    }

    return $normalized
}

function Normalize-WikiFileName {
    param(
        [Parameter(Mandatory = $true)][string]$Title
    )

    $name = $Title.Trim()
    $replacements = [ordered]@{
        '/' = ' and '
        '\' = ' and '
        '|' = ' and '
        ':' = '-'
        '*' = 'x'
        '?' = ''
        '"' = ''
        '<' = ''
        '>' = ''
    }

    foreach ($entry in $replacements.GetEnumerator()) {
        $escaped = [regex]::Escape($entry.Key)
        $name = $name -replace $escaped, $entry.Value
    }

    $name = $name -replace '\s+', ' '
    $name = $name.Trim()
    $name = $name.TrimEnd('.', ' ')

    if ([string]::IsNullOrWhiteSpace($name)) {
        $name = 'untitled'
    }

    $reserved = @(
        'con','prn','aux','nul',
        'com1','com2','com3','com4','com5','com6','com7','com8','com9',
        'lpt1','lpt2','lpt3','lpt4','lpt5','lpt6','lpt7','lpt8','lpt9'
    )

    if ($reserved -contains $name.ToLowerInvariant()) {
        $name = "${name}_"
    }

    return $name
}

function Get-SummaryFileNameForRaw {
    param(
        [Parameter(Mandatory = $true)][string]$RawFileName
    )

    if ($RawFileName.ToLowerInvariant().EndsWith('.md')) {
        return $RawFileName
    }

    return "$RawFileName.md"
}

function Get-RelativePathText {
    param(
        [Parameter(Mandatory = $true)][string]$BasePath,
        [Parameter(Mandatory = $true)][string]$TargetPath
    )

    $base = $BasePath
    if (-not $base.EndsWith([System.IO.Path]::DirectorySeparatorChar)) {
        $base += [System.IO.Path]::DirectorySeparatorChar
    }

    $baseUri = New-Object System.Uri($base)
    $targetUri = New-Object System.Uri($TargetPath)
    $relativeUri = $baseUri.MakeRelativeUri($targetUri)
    return [System.Uri]::UnescapeDataString($relativeUri.ToString()).Replace('/', [System.IO.Path]::DirectorySeparatorChar)
}

function Ensure-ParentDirectory {
    param(
        [Parameter(Mandatory = $true)][string]$Path
    )

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
}

function Write-Utf8File {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    Ensure-ParentDirectory -Path $Path
    $utf8 = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8)
}

function Append-Utf8Line {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Line
    )

    Ensure-ParentDirectory -Path $Path
    $utf8 = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::AppendAllText($Path, $Line + [Environment]::NewLine, $utf8)
}

function ConvertTo-JsonText {
    param(
        [Parameter(Mandatory = $true)]$InputObject
    )

    return ($InputObject | ConvertTo-Json -Depth 10)
}
