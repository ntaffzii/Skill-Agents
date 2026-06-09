param(
    [string]$Root = "skills"
)

$errors = @()
$skillFiles = Get-ChildItem -Path $Root -Recurse -Filter "SKILL.md" -File

foreach ($file in $skillFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    $relative = Resolve-Path -Path $file.FullName -Relative

    if (-not $content.StartsWith("---")) {
        $errors += "$relative missing opening frontmatter marker"
        continue
    }

    if (-not ($content -match '(?m)^name:\s*[a-z0-9][a-z0-9-]*\s*$')) {
        $errors += "$relative missing valid lowercase hyphenated name"
    }

    if (-not ($content -match '(?m)^description:\s*\S.+$')) {
        $errors += "$relative missing description"
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

"Validated {0} skills." -f $skillFiles.Count
