# Obsidian Vault Cleanup

## Goal

Organize an Obsidian vault or folder while preserving links, metadata, and local conventions.

## When To Use

Use when the user asks to clean, organize, connect, normalize, tag, index, or restructure Obsidian notes.

## Skills

- `obsidian-vault-workflow`
- `obsidian-markdown`
- `obsidian-canvas`

## Steps

1. Discover conventions with `obsidian-vault-workflow`.
   - Inspect folder names, tags, properties, templates, indexes, and link style.
   - Do not invent a new taxonomy before reading the existing one.
   - If Notion or memory tools are available and the user asks for cross-workspace organization, inspect only the relevant external notes or decisions before planning.

2. Plan changes.
   - Identify notes to edit.
   - Decide whether the job needs tags, properties, backlinks, index notes, or a canvas.
   - Avoid mass renames unless explicitly approved.

3. Edit notes with `obsidian-markdown`.
   - Normalize frontmatter.
   - Add wikilinks and tags.
   - Preserve note voice and personal content.

4. Add visual structure with `obsidian-canvas` if requested or useful.
   - Create a map, board, or concept graph.
   - Keep JSON Canvas valid.

5. Verify.
   - Check YAML frontmatter.
   - Check wikilinks and embeds.
   - Check renamed or moved files have aliases or updated references.
   - If notes should connect to Notion, produce a Notion update plan instead of silently syncing or overwriting pages.

## Output

End with:

- Notes changed
- Structure added
- Links or tags updated
- Notion or external-note handoff plan, if requested
- Anything intentionally left untouched
