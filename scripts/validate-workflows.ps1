param(
    [string]$Index = "data/workflows.json"
)

$errors = @()

if (-not (Test-Path -Path $Index)) {
    Write-Error "$Index not found"
    exit 1
}

try {
    $workflows = Get-Content -Path $Index -Raw | ConvertFrom-Json
} catch {
    Write-Error "$Index is not valid JSON: $_"
    exit 1
}

foreach ($workflow in $workflows) {
    if (-not $workflow.id) {
        $errors += "workflow missing id"
    }

    if (-not ($workflow.id -match '^[a-z0-9][a-z0-9-]*$')) {
        $errors += "$($workflow.id) has invalid id"
    }

    if (-not $workflow.title) {
        $errors += "$($workflow.id) missing title"
    }

    if (-not $workflow.description) {
        $errors += "$($workflow.id) missing description"
    }

    if (-not $workflow.path) {
        $errors += "$($workflow.id) missing path"
    } elseif (-not (Test-Path -Path $workflow.path)) {
        $errors += "$($workflow.id) path not found: $($workflow.path)"
    }

    if (-not $workflow.recommendedSkills -or $workflow.recommendedSkills.Count -eq 0) {
        $errors += "$($workflow.id) missing recommendedSkills"
    }

    if (-not $workflow.steps -or $workflow.steps.Count -eq 0) {
        $errors += "$($workflow.id) missing steps"
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

"Validated {0} workflows." -f $workflows.Count
