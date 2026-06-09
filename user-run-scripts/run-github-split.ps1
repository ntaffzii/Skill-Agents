param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")

powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Root "scripts\prepare-github-split.ps1") -Clean:$Clean
