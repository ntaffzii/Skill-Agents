<#
Validates that data/skills-index.json is current — i.e. regenerating it from
the actual skill folders produces byte-identical output to what's committed.
This is what makes the index trustworthy as a "canonical source": unlike a
hand-maintained catalog, it cannot silently drift from the real skills,
because CI fails the moment someone adds/renames/removes a skill without
re-running generate-skills-index.ps1.
#>
param(
    [string]$Index = "data/skills-index.json"
)

if (-not (Test-Path -Path $Index)) {
    Write-Error "$Index not found. Run scripts/generate-skills-index.ps1 first."
    exit 1
}

$committed = Get-Content -Path $Index -Raw

$tempFile = [System.IO.Path]::GetTempFileName()
try {
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\generate-skills-index.ps1 -Output $tempFile | Out-Null
    $fresh = Get-Content -Path $tempFile -Raw
} finally {
    Remove-Item -Path $tempFile -ErrorAction SilentlyContinue
}

if ($committed -ne $fresh) {
    Write-Error "$Index is stale. Run: powershell -NoProfile -File .\scripts\generate-skills-index.ps1"
    exit 1
}

try {
    $entries = $committed | ConvertFrom-Json
} catch {
    Write-Error "$Index is not valid JSON: $_"
    exit 1
}

$errors = @()
foreach ($entry in $entries) {
    if (-not $entry.id) {
        $errors += "entry with path '$($entry.path)' is missing id (SKILL.md missing 'name' frontmatter?)"
    }
    if (-not $entry.description) {
        $errors += "$($entry.id) is missing description"
    }
    if (-not (Test-Path -Path $entry.path)) {
        $errors += "$($entry.id) path not found: $($entry.path)"
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

"Validated {0} skills-index entries (index is current)." -f $entries.Count
