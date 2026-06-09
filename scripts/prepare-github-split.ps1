param(
    [string]$OutputRoot = "",
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
if (-not $OutputRoot) {
    $OutputRoot = Join-Path $RepoRoot "github-ready"
}

$SkillRepo = Join-Path $OutputRoot "Skill-Agents"
$ToolsRepo = Join-Path $OutputRoot "ai-desk-mcp-tools"

function Copy-RepoItem {
    param(
        [Parameter(Mandatory = $true)][string]$Source,
        [Parameter(Mandatory = $true)][string]$DestinationRoot
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        return
    }

    $Name = Split-Path -Leaf $Source
    $Destination = Join-Path $DestinationRoot $Name

    if ((Get-Item -LiteralPath $Source).PSIsContainer) {
        New-Item -ItemType Directory -Force -Path $Destination | Out-Null
        robocopy $Source $Destination /E /XD ".git" ".venv" "venv" "node_modules" "__pycache__" "logs" "scratch" /XF "*.pyc" "*.pyo" | Out-Null
        if ($LASTEXITCODE -gt 7) {
            throw "robocopy failed for $Source with exit code $LASTEXITCODE"
        }
    }
    else {
        New-Item -ItemType Directory -Force -Path $DestinationRoot | Out-Null
        Copy-Item -LiteralPath $Source -Destination $Destination -Force
    }
}

if ($Clean -and (Test-Path -LiteralPath $OutputRoot)) {
    Write-Host "Cleaning $OutputRoot"
    Remove-Item -LiteralPath $OutputRoot -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $SkillRepo, $ToolsRepo | Out-Null

$SkillItems = @(
    ".gitignore",
    "README.md",
    "Skill.md",
    "data",
    "docs",
    "scripts",
    "skills",
    "workflows"
)

foreach ($Item in $SkillItems) {
    Copy-RepoItem -Source (Join-Path $RepoRoot $Item) -DestinationRoot $SkillRepo
}

$ToolItems = @(
    "server.py",
    "security.py",
    "requirements.txt",
    "trusted_sources.json",
    "config",
    "prompt_engine",
    "tools",
    "tests",
    "README.md"
)

foreach ($Item in $ToolItems) {
    Copy-RepoItem -Source (Join-Path (Join-Path $RepoRoot "mcp-tools") $Item) -DestinationRoot $ToolsRepo
}

$SkillFileCount = (Get-ChildItem -LiteralPath $SkillRepo -Recurse -File | Measure-Object).Count
$ToolsFileCount = (Get-ChildItem -LiteralPath $ToolsRepo -Recurse -File | Measure-Object).Count

Write-Host "Created GitHub-ready folders:"
Write-Host "  Skill-Agents:       $SkillRepo ($SkillFileCount files)"
Write-Host "  ai-desk-mcp-tools:  $ToolsRepo ($ToolsFileCount files)"
Write-Host ""
Write-Host "Original combined folder is unchanged:"
Write-Host "  $RepoRoot"
