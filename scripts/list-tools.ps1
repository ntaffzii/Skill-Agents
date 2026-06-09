param(
    [string]$Index = "data/tools.json"
)

$toolGroups = Get-Content -Path $Index -Raw | ConvertFrom-Json

foreach ($group in $toolGroups) {
    "{0} - {1}`n  {2}`n  module: {3}`n  tools: {4}" -f `
        $group.id, `
        $group.title, `
        $group.description, `
        $group.module, `
        ($group.tools -join ", ")
}
