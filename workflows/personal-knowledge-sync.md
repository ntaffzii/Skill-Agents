# Personal Knowledge Sync

## Goal

Move knowledge between Obsidian, Notion, local memory, and optional RAG indexes without losing source metadata or overwriting private notes.

## When To Use

Use when the user asks to sync, publish, migrate, organize, index, or summarize personal notes across Obsidian, Notion, memory, or RAG.

## Skills

- `obsidian-notion-bridge`
- `obsidian-vault-workflow`
- `obsidian-markdown`
- `markdown-report`
- `handoff`

## Steps

1. Choose source of truth.
   - Ask or infer whether Obsidian, Notion, or local memory is authoritative for this task.
   - Prefer Obsidian/local Markdown as the editable source unless the user says otherwise.

2. Inspect scope.
   - Read only selected notes/pages first.
   - Extract titles, tags, links, URLs, IDs, and source paths.
   - Search vector memory for related prior decisions.

3. Plan conversion.
   - For Obsidian to Notion, create Notion payload plans.
   - For Notion to Obsidian, create Markdown write plans.
   - For RAG, chunk sources and plan provider-specific indexing.

4. Review safety.
   - Do not delete, overwrite, or auto-sync broad folders.
   - Preserve source path, Notion URL/page id, tags, backlinks, and aliases where possible.
   - Generate a user-run script only when the user wants to apply changes outside sandbox.

5. Hand off.
   - Provide files/pages inspected, payloads drafted, and decisions saved.

## Verification

- Markdown frontmatter is valid.
- Wikilinks and tags are preserved or intentionally mapped.
- Notion payloads are drafts until user applies them.
- RAG chunks include stable source IDs.

## Output

End with:

- Source of truth
- Notes/pages inspected
- Sync or index plan
- Draft files or payloads
- Manual steps needed

