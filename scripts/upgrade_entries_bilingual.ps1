param(
    [string]$RepoRoot = ".",
    [string]$EntriesRoot = "entries/cvpr2024"
)

$ErrorActionPreference = "Stop"

function Ensure-YamlKey {
    param(
        [System.Collections.Generic.List[string]]$Lines,
        [string]$Key,
        [string]$Value
    )
    $pattern = "^{0}\s*:" -f [Regex]::Escape($Key)
    foreach ($line in $Lines) {
        if ($line -match $pattern) {
            return $false
        }
    }
    $Lines.Add(("{0}: {1}" -f $Key, $Value)) | Out-Null
    return $true
}

$resolvedRepoRoot = (Resolve-Path $RepoRoot).Path
$entriesPath = Join-Path $resolvedRepoRoot $EntriesRoot
$templatesPath = Join-Path $resolvedRepoRoot "templates"

if (-not (Test-Path $entriesPath)) {
    throw "Entries path not found: $entriesPath"
}
if (-not (Test-Path $templatesPath)) {
    throw "Templates path not found: $templatesPath"
}

$beginnerTemplate = Get-Content -Raw (Join-Path $templatesPath "beginner.md")
$masterTemplate = Get-Content -Raw (Join-Path $templatesPath "master.md")
$researchTemplate = Get-Content -Raw (Join-Path $templatesPath "research.md")

$entryDirs = Get-ChildItem $entriesPath -Directory | Sort-Object Name
$updatedMdCount = 0
$updatedMetaCount = 0
$updatedIdeaCount = 0

foreach ($dir in $entryDirs) {
    $beginnerPath = Join-Path $dir.FullName "beginner.md"
    $masterPath = Join-Path $dir.FullName "master.md"
    $researchPath = Join-Path $dir.FullName "research.md"

    if (Test-Path $beginnerPath) {
        Set-Content -Encoding UTF8 -Path $beginnerPath -Value $beginnerTemplate
        $updatedMdCount++
    }
    if (Test-Path $masterPath) {
        Set-Content -Encoding UTF8 -Path $masterPath -Value $masterTemplate
        $updatedMdCount++
    }
    if (Test-Path $researchPath) {
        Set-Content -Encoding UTF8 -Path $researchPath -Value $researchTemplate
        $updatedMdCount++
    }

    $metaPath = Join-Path $dir.FullName "meta.yaml"
    if (Test-Path $metaPath) {
        $metaLines = [System.Collections.Generic.List[string]]::new()
        (Get-Content $metaPath) | ForEach-Object { $metaLines.Add($_) | Out-Null }

        $metaChanged = $false
        $metaChanged = (Ensure-YamlKey -Lines $metaLines -Key "title_zh" -Value "NOT_SPECIFIED") -or $metaChanged
        $metaChanged = (Ensure-YamlKey -Lines $metaLines -Key "field_zh" -Value "null") -or $metaChanged
        $metaChanged = (Ensure-YamlKey -Lines $metaLines -Key "task_zh" -Value "null") -or $metaChanged
        $metaChanged = (Ensure-YamlKey -Lines $metaLines -Key "summary_one_line_zh" -Value "NOT_SPECIFIED") -or $metaChanged

        if ($metaChanged) {
            Set-Content -Encoding UTF8 -Path $metaPath -Value $metaLines
            $updatedMetaCount++
        }
    }

    $ideaPath = Join-Path $dir.FullName "idea.yaml"
    if (Test-Path $ideaPath) {
        $ideaLines = [System.Collections.Generic.List[string]]::new()
        (Get-Content $ideaPath) | ForEach-Object { $ideaLines.Add($_) | Out-Null }

        $ideaChanged = $false
        $ideaChanged = (Ensure-YamlKey -Lines $ideaLines -Key "improvement_point_zh" -Value "NOT_SPECIFIED") -or $ideaChanged
        $ideaChanged = (Ensure-YamlKey -Lines $ideaLines -Key "core_mechanism_zh" -Value "NOT_SPECIFIED") -or $ideaChanged
        $ideaChanged = (Ensure-YamlKey -Lines $ideaLines -Key "why_it_works_zh" -Value "NOT_SPECIFIED") -or $ideaChanged
        $ideaChanged = (Ensure-YamlKey -Lines $ideaLines -Key "applicable_conditions_zh" -Value "[]") -or $ideaChanged
        $ideaChanged = (Ensure-YamlKey -Lines $ideaLines -Key "benefits_zh" -Value "[]") -or $ideaChanged
        $ideaChanged = (Ensure-YamlKey -Lines $ideaLines -Key "tradeoffs_zh" -Value "[]") -or $ideaChanged
        $ideaChanged = (Ensure-YamlKey -Lines $ideaLines -Key "transferability_zh" -Value "NOT_SPECIFIED") -or $ideaChanged
        $ideaChanged = (Ensure-YamlKey -Lines $ideaLines -Key "implementation_hint_zh" -Value "NOT_SPECIFIED") -or $ideaChanged
        $ideaChanged = (Ensure-YamlKey -Lines $ideaLines -Key "task_keywords_zh" -Value "[]") -or $ideaChanged
        $ideaChanged = (Ensure-YamlKey -Lines $ideaLines -Key "method_keywords_zh" -Value "[]") -or $ideaChanged
        $ideaChanged = (Ensure-YamlKey -Lines $ideaLines -Key "innovation_keywords_zh" -Value "[]") -or $ideaChanged

        if ($ideaChanged) {
            Set-Content -Encoding UTF8 -Path $ideaPath -Value $ideaLines
            $updatedIdeaCount++
        }
    }
}

Write-Host ("Entries scanned: {0}" -f $entryDirs.Count)
Write-Host ("Markdown files rewritten: {0}" -f $updatedMdCount)
Write-Host ("meta.yaml updated: {0}" -f $updatedMetaCount)
Write-Host ("idea.yaml updated: {0}" -f $updatedIdeaCount)
