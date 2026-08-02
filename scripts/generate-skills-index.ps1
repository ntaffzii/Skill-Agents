<#
Generates data/skills-index.json — the canonical, machine-readable index of
every skill in the repo (skills/**/SKILL.md and Skill.md/**/SKILL.md).

This is a *generated* file: it is derived entirely from SKILL.md frontmatter
and folder structure, so it cannot drift from the real skills the way a
hand-maintained catalog can. Run this after adding/removing/renaming a skill,
then run validate-skills-index.ps1 to confirm the committed file is current
(CI should fail if someone forgets to regenerate).
#>
param(
    [string]$Output = "data/skills-index.json"
)

function Get-SkillEntries {
    param(
        [string]$Root,
        [string]$RootLabel
    )

    $entries = @()
    $skillFiles = Get-ChildItem -Path $Root -Recurse -Filter "SKILL.md" -File

    foreach ($file in $skillFiles) {
        $content = Get-Content -Path $file.FullName -Raw
        $name = if ($content -match '(?m)^name:\s*(.+)$') { $Matches[1].Trim() } else { $null }
        $description = if ($content -match '(?m)^description:\s*(.+)$') { $Matches[1].Trim().Trim('"') } else { $null }

        $relative = (Resolve-Path -Path $file.FullName -Relative) -replace '^\.[\\/]', '' -replace '\\', '/'
        $skillDir = Split-Path -Path $file.FullName -Parent
        $rootFull = (Resolve-Path -Path $Root).Path
        $relDir = (Resolve-Path -Path $skillDir).Path.Substring($rootFull.Length).Trim('\', '/').Replace('\', '/')
        $segments = @($relDir.Split('/') | Where-Object { $_ -ne '' })

        if ($segments.Count -eq 0) {
            # SKILL.md sits directly at the root (e.g. Skill.md/<name>/SKILL.md handled below via segments==1)
            $category = $RootLabel
            $role = "category-index"
        } elseif ($segments.Count -eq 1) {
            $category = $segments[0]
            $role = "category-index"
        } else {
            $category = $segments[0]
            $role = "skill"
        }

        # tier heuristic: a code file (.py/.ts) alongside SKILL.md means it has a real self-test
        $codeFiles = @(Get-ChildItem -Path $skillDir -Filter "*.py" -File -ErrorAction SilentlyContinue)
        $codeFiles += @(Get-ChildItem -Path $skillDir -Filter "*.ts" -File -ErrorAction SilentlyContinue)
        $tier = if ($codeFiles.Count -gt 0) { "validator" } else { "prose" }

        $entries += [PSCustomObject]@{
            id          = $name
            category    = $category
            role        = $role
            tier        = $tier
            path        = $relative
            description = $description
            root        = $RootLabel
        }
    }

    return $entries
}

$all = @()
$all += Get-SkillEntries -Root "skills" -RootLabel "skills"
if (Test-Path -Path "Skill.md") {
    $all += Get-SkillEntries -Root "Skill.md" -RootLabel "Skill.md"
}

$all = $all | Sort-Object root, category, id

$json = $all | ConvertTo-Json -Depth 5
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Resolve-Path -Path (Split-Path -Path $Output -Parent)).Path + "/" + (Split-Path -Path $Output -Leaf), $json + "`n", $utf8NoBom)

"Wrote {0} skill entries to {1}" -f $all.Count, $Output
