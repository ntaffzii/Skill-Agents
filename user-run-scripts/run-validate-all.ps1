$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$BundledPython = "C:\Users\natth\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if (Test-Path $BundledPython) {
    powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Root "scripts\validate-all.ps1") -Python $BundledPython
}
else {
    powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Root "scripts\validate-all.ps1")
}
