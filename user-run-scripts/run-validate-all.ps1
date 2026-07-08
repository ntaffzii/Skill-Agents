# validate_all
# Risk: low
# Purpose: Run all repo validators and MCP tool tests.
# Generated: 2026-07-08 21:30:28
#
# Review this script before running it.
# Run from the combined Skill-Agents repo unless the script says otherwise.

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$BundledPython = "C:\Users\natth\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if (Test-Path $BundledPython) {
    powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Root "scripts\validate-all.ps1") -Python $BundledPython
}
else {
    powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Root "scripts\validate-all.ps1")
}
