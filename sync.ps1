$ErrorActionPreference = "Stop"

$RepoRoot = $PSScriptRoot
$ScriptPath = Join-Path $RepoRoot "scripts\sync_skills.py"
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"

function Test-PythonCmd {
    param([string]$Exe, [string[]]$PrefixArgs = @())
    try {
        & $Exe @PrefixArgs -c "import sys" *> $null
        return ($LASTEXITCODE -eq 0)
    } catch {
        return $false
    }
}

$RunnerExe = $null
$RunnerPrefix = @()

if ((Test-Path -LiteralPath $VenvPython) -and (Test-PythonCmd -Exe $VenvPython)) {
    $RunnerExe = $VenvPython
} elseif ((Get-Command py -ErrorAction SilentlyContinue) -and (Test-PythonCmd -Exe "py" -PrefixArgs @("-3"))) {
    $RunnerExe = "py"
    $RunnerPrefix = @("-3")
} elseif ((Get-Command python -ErrorAction SilentlyContinue) -and (Test-PythonCmd -Exe "python")) {
    $RunnerExe = "python"
} elseif ((Get-Command python3 -ErrorAction SilentlyContinue) -and (Test-PythonCmd -Exe "python3")) {
    $RunnerExe = "python3"
} elseif (Get-Command uv -ErrorAction SilentlyContinue) {
    $RunnerExe = "uv"
    $RunnerPrefix = @("run", "--project", $RepoRoot, "python")
}

if (-not $RunnerExe) {
    Write-Error "Python 3.12+ not found. Please install Python or uv, or download the standalone release from GitHub Releases."
    exit 1
}

& $RunnerExe @RunnerPrefix $ScriptPath @args
exit $LASTEXITCODE
