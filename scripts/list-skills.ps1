param(
    [string]$Root = "skills"
)

$skillFiles = Get-ChildItem -Path $Root -Recurse -Filter "SKILL.md" -File

foreach ($file in $skillFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    $name = if ($content -match '(?m)^name:\s*(.+)$') { $Matches[1].Trim() } else { "(missing name)" }
    $description = if ($content -match '(?m)^description:\s*(.+)$') { $Matches[1].Trim() } else { "(missing description)" }
    $relative = Resolve-Path -Path $file.FullName -Relative

    "{0} - {1}`n  {2}" -f $name, $relative, $description
}
