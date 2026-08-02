# git_publish_skill_agents
# Risk: high
# Purpose: Initialize and push the GitHub-ready Skill-Agents repo. Requires a remote URL.
# Generated: 2026-08-02 16:23:24
#
# Review this script before running it.
# Run from the combined Skill-Agents repo unless the script says otherwise.

param(
    [Parameter(Mandatory = $true)][string]$RemoteUrl,
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Repo = Join-Path $Root "github-ready\Skill-Agents"

if (-not (Test-Path $Repo)) {
    throw "Missing $Repo. Run run-github-split.ps1 first."
}

Push-Location $Repo
try {
    if (-not (Test-Path ".git")) {
        git init
    }
    git checkout -B $Branch
    git add .
    git commit -m "Initial Skill-Agents publish"
    git remote remove origin 2>$null
    git remote add origin $RemoteUrl
    git push -u origin $Branch
}
finally {
    Pop-Location
}
