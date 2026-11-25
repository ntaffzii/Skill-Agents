param(
    [string]$Python = "",
    [switch]$SkipZip
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$ScriptsDir = Join-Path $RepoRoot "scripts"
$EntryScript = Join-Path $ScriptsDir "sync_gui.py"
$ReleaseDir = Join-Path $RepoRoot "dist\release"
$WorkDir = Join-Path $RepoRoot "build\pyinstaller"

if (-not $Python) {
    $VenvPy = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $VenvPy) {
        $Python = $VenvPy
    } else {
        $Python = "python"
    }
}

Write-Host "Using Python: $Python"
& $Python -c "import PySide6, PyInstaller" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Missing PySide6 or PyInstaller in '$Python'. Install with: uv pip install --python `"$Python`" `".[gui,build]`""
    exit 1
}

if (Test-Path -LiteralPath $ReleaseDir) {
    Remove-Item -LiteralPath $ReleaseDir -Recurse -Force
}
if (Test-Path -LiteralPath $WorkDir) {
    Remove-Item -LiteralPath $WorkDir -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $ReleaseDir, $WorkDir | Out-Null

$AppName = "SkillAgentsSync"
& $Python -m PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --onefile `
    --name $AppName `
    --collect-data certifi `
    --paths $ScriptsDir `
    --distpath $ReleaseDir `
    --workpath $WorkDir `
    --specpath $WorkDir `
    $EntryScript

if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller build failed with exit code $LASTEXITCODE"
}

$ExePath = Join-Path $ReleaseDir "$AppName.exe"
if (-not (Test-Path -LiteralPath $ExePath)) {
    throw "Expected output executable not found: $ExePath"
}

$Artifacts = @($ExePath)
if (-not $SkipZip) {
    $ZipPath = Join-Path $ReleaseDir "$AppName-windows-x64.zip"
    Compress-Archive -Path $ExePath -DestinationPath $ZipPath -Force
    $Artifacts += $ZipPath
}

$ChecksumFile = Join-Path $ReleaseDir "SHA256SUMS.txt"
$ChecksumLines = foreach ($File in $Artifacts) {
    $Hash = (Get-FileHash -Path $File -Algorithm SHA256).Hash.ToLowerInvariant()
    "$Hash  $(Split-Path -Leaf $File)"
}
Set-Content -Path $ChecksumFile -Value $ChecksumLines -Encoding UTF8

Write-Host "`nRelease artifacts created in ${ReleaseDir}:"
Get-ChildItem -LiteralPath $ReleaseDir | ForEach-Object {
    Write-Host "  - $($_.Name) ($([Math]::Round($_.Length / 1MB, 2)) MB)"
}
