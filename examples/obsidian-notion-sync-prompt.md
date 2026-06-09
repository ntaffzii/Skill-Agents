# Obsidian Notion Sync Prompt

```text
Use personal-knowledge-sync.
Use personal-knowledge-rag toolset if available.

Goal:
Convert selected Obsidian notes into Notion payload plans and RAG chunks.

Source of truth:
Obsidian/local Markdown is source of truth.

Constraints:
- Draft Notion payloads only.
- Do not apply updates to Notion.
- Do not rename or delete notes.
- Preserve tags, wikilinks, aliases, source paths, Notion URLs, and page IDs where available.
- Call out any lossy conversion.

Output:
- Notes inspected
- Tags and links found
- Notion payload drafts
- RAG chunk plan
- Manual review checklist
```

