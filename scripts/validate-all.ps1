param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -Path "mcp-tools")) {
    Write-Error "Run this script from the repository root."
    exit 1
}

powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-tools.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-toolsets.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-workflows.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-skills.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-skills.ps1 -Root Skill.md
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\validate-skills-index.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\test-mcp-tools.ps1 -Python $Python

"All validations passed."
