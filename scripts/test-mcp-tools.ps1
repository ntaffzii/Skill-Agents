param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -Path "mcp-tools")) {
    Write-Error "Run this script from the repository root."
    exit 1
}

& $Python -c "from pathlib import Path
for p in Path('mcp-tools').rglob('*.py'):
    compile(p.read_text(encoding='utf-8'), str(p), 'exec')
print('syntax ok')"

& $Python -m unittest discover -s ".\mcp-tools\tests"
