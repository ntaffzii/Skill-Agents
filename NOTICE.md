# Notice And Attribution

This project is original work built for a personal AI-agent operating system. It studies public agent-skill and MCP repositories for patterns, but it does not claim to be an official fork, template, distribution, or endorsement of those projects.

## Inspiration

The structure and documentation style were informed by studying:

- `thananon/9arm-skills` - clean skill buckets such as engineering, productivity, personal, in-progress, and deprecated.
- `mattpocock/skills` - practical engineering workflows, diagnosis, TDD, review loops, and installable skills.
- `kepano/obsidian-skills` - focused Obsidian-specific skill design for Markdown, Canvas, and vault workflows.
- `sickn33/antigravity-awesome-skills` - large-scale skill catalogs, role bundles, workflows, validation, and installer-oriented organization.
- `google/skills` - product/domain-specific skill packs, installation notes, contribution guidance, and Apache-licensed distribution.
- `anthropics/skills` - public Agent Skills examples and the broader Agent Skills concept.
- [UI Skills](https://www.ui-skills.com/skills/) by Interface Office - a curated design-engineering skill directory whose taxonomy and linked skills informed the original `ui-design-engineering` synthesis in this repository.

The UI skill synthesis was particularly informed by public descriptions and patterns from Baseline UI and Fixing Accessibility by Ibelick, Frontend Design by Anthropic, Interface Design by Dammyjay93, Impeccable and its focused modes by Paul Bakaus, plus framework, browser-testing, performance, motion, and accessibility entries cataloged by UI Skills. Full links and adaptation notes are in `skills/engineering/ui-design-engineering/references/credits.md`.

## License Notes

- This repository's original code and docs are released under the license in `LICENSE`.
- Public repositories may have their own licenses and terms. Check each upstream repository before copying source files, skill text, scripts, or assets.
- MIT-licensed projects generally allow copying, modifying, and redistributing with attribution and inclusion of the original copyright/license notice.
- Apache-2.0 projects generally allow copying, modifying, and redistributing under the license terms, including preserving required notices.
- If an upstream repository has no clear top-level open-source license, treat its contents as reference material only unless permission is confirmed.

## What Was Reused

This project reuses ideas and patterns, not wholesale upstream skill files:

- skill folder shape
- `SKILL.md` frontmatter convention
- workflow/playbook organization
- tool registry and toolset ideas
- safety-first documentation style
- install and validation documentation patterns
- UI design-engineering taxonomy covering product intent, accessibility, interaction, motion, responsive adaptation, hardening, performance, and browser validation

If any future file copies upstream text, code, scripts, or assets directly, add a file-level note and preserve the upstream license requirements.
