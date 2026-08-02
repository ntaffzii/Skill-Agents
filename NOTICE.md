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
- [Boom-Vitt/claude-thai-skills](https://github.com/Boom-Vitt/claude-thai-skills) (MIT) - locale-specific content-domain skill design (trigger-phrase-rich frontmatter, When-to-use/When-NOT-to-use boundaries, common-mistakes and known-limitations sections) that informed the `skills/thai/` category in this repository. Legal, tax, and formatting content is written fresh and checked against current sources, not copied from that repository.
- [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) (MIT) - workflow architecture (canonical skill index, "no API key" starter path tiering, human-in-the-loop / not-a-signal-service framing, chaining skills into a market-regime → risk-gate → journal pipeline) that informed the `skills/trading/` category in this repository. That source repo ships 71 skills; this repository's starter set (8 skills) is scoped to the areas actually in use here and written fresh, not copied.
- [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) (**CC BY-NC 4.0 — non-commercial, incompatible with this repository's MIT license for direct reuse**) - only the general *concept* of a pre-finalization integrity gate that checks claims/citations before a research output ships informed `skills/research/claim-citation-check/` in this repository. No text, prompts, or code were copied from that repository; the concept of citation verification is not itself copyrightable, and the implementation here is original and independently written.

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
