param(
    [string]$Index = "data/workflows.json"
)

$workflows = Get-Content -Path $Index -Raw | ConvertFrom-Json

foreach ($workflow in $workflows) {
    "{0} - {1}`n  {2}`n  skills: {3}" -f `
        $workflow.id, `
        $workflow.path, `
        $workflow.description, `
        ($workflow.recommendedSkills -join ", ")
}
