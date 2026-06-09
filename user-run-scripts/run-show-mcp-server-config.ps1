$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Python = Join-Path $Root "mcp-tools\.venv\Scripts\python.exe"
$Server = Join-Path $Root "mcp-tools\server.py"

@"
{
  "mcpServers": {
    "ai-desk-tools": {
      "command": "$Python",
      "args": ["$Server"]
    }
  }
}
"@
