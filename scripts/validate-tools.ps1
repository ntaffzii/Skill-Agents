param(
    [string]$Index = "data/tools.json"
)

$errors = @()

if (-not (Test-Path -Path $Index)) {
    Write-Error "$Index not found"
    exit 1
}

try {
    $toolGroups = Get-Content -Path $Index -Raw | ConvertFrom-Json
} catch {
    Write-Error "$Index is not valid JSON: $_"
    exit 1
}

foreach ($group in $toolGroups) {
    if (-not ($group.id -match '^[a-z0-9][a-z0-9-]*$')) {
        $errors += "$($group.id) has invalid id"
    }

    if (-not $group.title) {
        $errors += "$($group.id) missing title"
    }

    if (-not $group.description) {
        $errors += "$($group.id) missing description"
    }

    if (-not $group.module) {
        $errors += "$($group.id) missing module"
    } elseif (-not (Test-Path -Path $group.module)) {
        $errors += "$($group.id) module path not found: $($group.module)"
    }

    if (-not $group.tools -or $group.tools.Count -eq 0) {
        $errors += "$($group.id) missing tools"
    }

    foreach ($tool in $group.tools) {
        if (-not ($tool -match '^[a-z0-9][a-z0-9_]*$')) {
            $errors += "$($group.id) has invalid tool name: $tool"
        }
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

"Validated {0} tool groups." -f $toolGroups.Count
