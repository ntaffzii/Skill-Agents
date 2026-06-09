param(
    [Parameter(Mandatory = $true)][string]$RemoteUrl,
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Repo = Join-Path $Root "github-ready\ai-desk-mcp-tools"

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
    git commit -m "Initial ai-desk-mcp-tools publish"
    git remote remove origin 2>$null
    git remote add origin $RemoteUrl
    git push -u origin $Branch
}
finally {
    Pop-Location
}
