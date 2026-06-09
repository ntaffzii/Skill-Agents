param(
    [string]$Toolsets = "data/toolsets.json",
    [string]$Tools = "data/tools.json"
)

$errors = @()

if (-not (Test-Path -Path $Toolsets)) {
    Write-Error "$Toolsets not found"
    exit 1
}

if (-not (Test-Path -Path $Tools)) {
    Write-Error "$Tools not found"
    exit 1
}

try {
    $toolsetsData = Get-Content -Path $Toolsets -Raw | ConvertFrom-Json
    $toolsData = Get-Content -Path $Tools -Raw | ConvertFrom-Json
} catch {
    Write-Error "Invalid JSON: $_"
    exit 1
}

$toolIds = @{}
foreach ($tool in $toolsData) {
    $toolIds[$tool.id] = $true
}

foreach ($toolset in $toolsetsData) {
    if (-not ($toolset.id -match '^[a-z0-9][a-z0-9-]*$')) {
        $errors += "$($toolset.id) has invalid id"
    }
    if (-not $toolset.title) {
        $errors += "$($toolset.id) missing title"
    }
    if (-not $toolset.description) {
        $errors += "$($toolset.id) missing description"
    }
    if (-not $toolset.toolGroups -or $toolset.toolGroups.Count -eq 0) {
        $errors += "$($toolset.id) missing toolGroups"
    }
    foreach ($groupId in $toolset.toolGroups) {
        if (-not $toolIds.ContainsKey($groupId)) {
            $errors += "$($toolset.id) references missing tool group: $groupId"
        }
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

"Validated {0} toolsets." -f $toolsetsData.Count
