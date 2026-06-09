$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Tools = Join-Path $Root "mcp-tools"
$Venv = Join-Path $Tools ".venv"

if (-not (Test-Path $Venv)) {
    python -m venv $Venv
}

& (Join-Path $Venv "Scripts\python.exe") -m pip install --upgrade pip
& (Join-Path $Venv "Scripts\pip.exe") install -r (Join-Path $Tools "requirements.txt")
