param(
    [string]$SkillName = "",
    [string]$Provider = ""
)

$ScriptPath = Join-Path $PSScriptRoot "scripts\sync_skills.py"

if ($SkillName -and $Provider) {
    python $ScriptPath $SkillName -p $Provider
} elseif ($SkillName) {
    python $ScriptPath $SkillName
} else {
    python $ScriptPath
}
