$ErrorActionPreference = "Stop"
$RepoDir = "h:\01_Work\Dev\project-work\agents-tools"
$GlobalDir = "$env:USERPROFILE\.gemini\config"

Write-Host "Deploying AI Customizations to Global Directory..."
Write-Host "WARNING: This will overwrite manual changes in $GlobalDir"

# Create directories
New-Item -ItemType Directory -Force -Path "$GlobalDir\skills\deep-planning" | Out-Null
New-Item -ItemType Directory -Force -Path "$GlobalDir\agents" | Out-Null
New-Item -ItemType Directory -Force -Path "$GlobalDir\rules" | Out-Null
New-Item -ItemType Directory -Force -Path "$RepoDir\dist" | Out-Null

# Phase A: Antigravity Global
Copy-Item -Path "$RepoDir\.agents\skills\deep-planning\SKILL.md" -Destination "$GlobalDir\skills\deep-planning\SKILL.md" -Force
Copy-Item -Path "$RepoDir\.agents\agents\architect.md" -Destination "$GlobalDir\agents\architect.md" -Force
Copy-Item -Path "$RepoDir\.agents\agents\implementer.md" -Destination "$GlobalDir\agents\implementer.md" -Force
Copy-Item -Path "$RepoDir\AGENTS.md" -Destination "$GlobalDir\rules\global_agents.md" -Force

Write-Host "Phase A complete: Antigravity Global tools installed."

# Phase B: Compile for Cursor/OpenCode
$AgentsMd = Get-Content -Path "$RepoDir\AGENTS.md" -Raw
$SkillMd = Get-Content -Path "$RepoDir\.agents\skills\deep-planning\SKILL.md" -Raw

# Strip YAML from SKILL.md
$SkillContent = $SkillMd -replace '(?s)^---.*?---\r?\n', ''

$CursorRulesPath = "$RepoDir\dist\global_cursorrules.md"

$OutputContent = @"
# Global Agent Rules
$AgentsMd

---

# Available Skills

## 1. deep-planning
**Use for:** Any non-trivial coding task — new features, multi-file changes, architecture decisions, bug fixes with unclear root cause.

**Instructions:**
$SkillContent
"@

Set-Content -Path $CursorRulesPath -Value $OutputContent -Force
Write-Host "Phase B complete: Multi-Agent Adapters generated at $CursorRulesPath"
Write-Host "Done."
