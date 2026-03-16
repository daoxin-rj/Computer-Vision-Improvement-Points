param(
    [string]$SourceDir = "G:\A-CVPR\2024",
    [string]$Year = "2024",
    [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"

function New-Slug {
    param([string]$Text)
    $slug = $Text.ToLowerInvariant()
    $slug = [Regex]::Replace($slug, "[^a-z0-9]+", "-")
    $slug = $slug.Trim("-")
    if ([string]::IsNullOrWhiteSpace($slug)) {
        $slug = "paper"
    }
    if ($slug.Length -gt 80) {
        $slug = $slug.Substring(0, 80).Trim("-")
    }
    return $slug
}

function Escape-Yaml {
    param([string]$Text)
    if ($null -eq $Text) {
        return ""
    }
    return $Text.Replace("`"", "''")
}

$resolvedRepoRoot = (Resolve-Path $RepoRoot).Path
$entriesRoot = Join-Path $resolvedRepoRoot ("entries\cvpr" + $Year)
$templateRoot = Join-Path $resolvedRepoRoot "templates"
$manifestPath = Join-Path $SourceDir "manifest.csv"

if (-not (Test-Path $SourceDir)) {
    throw "Source directory not found: $SourceDir"
}
if (-not (Test-Path $templateRoot)) {
    throw "Template directory not found: $templateRoot"
}

New-Item -ItemType Directory -Force -Path $entriesRoot | Out-Null

$manifestByFilename = @{}
if (Test-Path $manifestPath) {
    Import-Csv $manifestPath | ForEach-Object {
        if ($_.filename -and -not $manifestByFilename.ContainsKey($_.filename)) {
            $manifestByFilename[$_.filename] = $_
        }
    }
}

$pdfFiles = Get-ChildItem $SourceDir -File -Filter *.pdf | Sort-Object Name
$partFiles = Get-ChildItem $SourceDir -File -Filter *.part | Sort-Object Name

$usedSlugs = @{}
$indexRows = New-Object System.Collections.Generic.List[object]

$beginnerTemplate = Get-Content -Raw (Join-Path $templateRoot "beginner_L1小白.md")
$masterTemplate = Get-Content -Raw (Join-Path $templateRoot "master_L2入门.md")
$researchTemplate = Get-Content -Raw (Join-Path $templateRoot "research_L3复现.md")
$ideaTemplate = Get-Content -Raw (Join-Path $templateRoot "idea_改进点.yaml")

$i = 0
foreach ($pdf in $pdfFiles) {
    $i++
    $manifestRow = $null
    if ($manifestByFilename.ContainsKey($pdf.Name)) {
        $manifestRow = $manifestByFilename[$pdf.Name]
    }

    $title = [System.IO.Path]::GetFileNameWithoutExtension($pdf.Name)
    if ($manifestRow -and $manifestRow.title) {
        $title = $manifestRow.title
    }

    $slugBase = New-Slug $title
    $slug = $slugBase
    if ($usedSlugs.ContainsKey($slugBase)) {
        $usedSlugs[$slugBase]++
        $slug = "{0}-{1}" -f $slugBase, $usedSlugs[$slugBase]
    } else {
        $usedSlugs[$slugBase] = 1
    }

    $entryDir = Join-Path $entriesRoot $slug
    New-Item -ItemType Directory -Force -Path $entryDir | Out-Null

    Copy-Item $pdf.FullName (Join-Path $entryDir "paper.pdf") -Force

    $pdfUrl = "NOT_SPECIFIED"
    $manifestStatus = "NOT_SPECIFIED"
    if ($manifestRow) {
        if ($manifestRow.pdf_url) {
            $pdfUrl = $manifestRow.pdf_url
        }
        if ($manifestRow.status) {
            $manifestStatus = $manifestRow.status
        }
    }

    $metaYaml = @"
English:
  title: "$(Escape-Yaml $title)"
  authors: []
  venue: "CVPR"
  year: 2024
  url: "$(Escape-Yaml $pdfUrl)"
  code_url: null
  field: null
  task: null
  summary_one_line: NOT_SPECIFIED

中文:
  标题: NOT_SPECIFIED
  作者: []
  会议: "CVPR"
  年份: 2024
  链接: "$(Escape-Yaml $pdfUrl)"
  代码链接: null
  领域: NOT_SPECIFIED
  任务: NOT_SPECIFIED
  一句话总结: NOT_SPECIFIED
"@

    $sourceYaml = @"
source_filename: "$(Escape-Yaml $pdf.Name)"
source_size_bytes: $($pdf.Length)
source_manifest_status: "$(Escape-Yaml $manifestStatus)"
imported_at_utc: "$((Get-Date).ToUniversalTime().ToString("o"))"
"@

    Set-Content -Encoding UTF8 -Path (Join-Path $entryDir "meta_元信息.yaml") -Value $metaYaml
    Set-Content -Encoding UTF8 -Path (Join-Path $entryDir "source.yaml") -Value $sourceYaml
    Set-Content -Encoding UTF8 -Path (Join-Path $entryDir "beginner_L1小白.md") -Value $beginnerTemplate
    Set-Content -Encoding UTF8 -Path (Join-Path $entryDir "master_L2入门.md") -Value $masterTemplate
    Set-Content -Encoding UTF8 -Path (Join-Path $entryDir "research_L3复现.md") -Value $researchTemplate
    Set-Content -Encoding UTF8 -Path (Join-Path $entryDir "idea_改进点.yaml") -Value $ideaTemplate

    $indexRows.Add([pscustomobject]@{
        slug = $slug
        title = $title
        source_filename = $pdf.Name
        size_bytes = $pdf.Length
        paper_url = $pdfUrl
        manifest_status = $manifestStatus
    }) | Out-Null

    if (($i % 100) -eq 0) {
        Write-Host ("Processed {0}/{1}" -f $i, $pdfFiles.Count)
    }
}

$indexPath = Join-Path $entriesRoot "index.csv"
$indexRows | Export-Csv -NoTypeInformation -Encoding UTF8 $indexPath

$partsPath = Join-Path $entriesRoot "skipped_parts.txt"
if ($partFiles.Count -gt 0) {
    ($partFiles | Select-Object -ExpandProperty Name) | Set-Content -Encoding UTF8 $partsPath
} else {
    "NONE" | Set-Content -Encoding UTF8 $partsPath
}

Write-Host ("Import done. Entries: {0}" -f $pdfFiles.Count)
Write-Host ("Skipped .part files: {0}" -f $partFiles.Count)
Write-Host ("Output root: {0}" -f $entriesRoot)
