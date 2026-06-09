$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Python = Join-Path $Root "mcp-tools\.venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    throw "MCP tools virtualenv not found. Run run-install-mcp-dependencies.ps1 first."
}

& $Python -m playwright install chromium
