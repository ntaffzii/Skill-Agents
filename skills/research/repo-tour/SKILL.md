---
name: repo-tour
description: Use after graphify has already built graphify-out/graph.json for a project, to generate a dependency-ordered guided tour, an onboarding doc for new team members, or a diff-impact analysis before a commit/PR — reading the existing graph instead of re-scanning the repo. Trigger on "onboarding guide", "เอกสารสำหรับทีมใหม่", "guided tour ของโค้ด", "diff impact", "อธิบาย repo ให้ทีมใหม่", "what does this change affect", when graphify-out/graph.json already exists. If graphify-out/graph.json does NOT exist yet, tell the user to run graphify first — this skill does not scan or build a graph itself.
---

# Repo Tour (reads an existing graphify graph)

## Overview

`graphify` already builds a persistent knowledge graph (`graphify-out/graph.json`) from a codebase — that's the expensive, token-hungry part, and it's already solved. What's missing is three specific consumption modes: a **dependency-ordered reading tour**, an **onboarding doc**, and a **diff-impact report**. This skill supplies those three by reading the existing graph, not by re-scanning the repo — cheap, fast, and doesn't duplicate graphify's own extraction pipeline.

**Fast-path rule (check this first, every time)**: if `graphify-out/graph.json` does not exist, **stop and tell the user to run `graphify` first** (`/graphify` or the graphify skill). Do not fall back to reading files manually — that's `project-discovery`'s job, not this skill's.

## When to use

- สร้างเอกสาร onboarding สำหรับทีมใหม่ จากกราฟที่ graphify สร้างไว้แล้ว
- สร้างลำดับการอ่านโค้ดที่แนะนำ (จากโมดูลพื้นฐานไปหาโมดูลที่พึ่งพามัน)
- เช็คว่า diff/PR ปัจจุบันกระทบส่วนไหนของระบบบ้าง ก่อน commit
- Any request to "explain this repo to a new person" or "what breaks if I change X" when a graph already exists

## When NOT to use

- `graphify-out/graph.json` doesn't exist — run `graphify` first, this skill has nothing to read
- The user wants the graph itself explored interactively (queries, path-finding between concepts) — that's `graphify query`/`graphify path`/`graphify explain`, already built and more capable than anything here
- A one-shot, no-graph project overview for a small/unfamiliar repo — `project-discovery` is lighter-weight for that

## Core knowledge

**Three sub-workflows, one shared graph loader** (`graph_adapter.py`):

| Workflow | Script | Input | Output |
|---|---|---|---|
| Guided tour | `build_tour.py` | `graph.json` | Dependency-ordered node list (foundational modules first) |
| Onboarding doc | `build_onboarding.py` | `graph.json` + project name | Markdown doc: hub modules + reading order |
| Diff impact | `diff_impact.py` | `graph.json` + changed file paths | Per-file impact report, grouped by hop distance |

**Guided tour ordering**: topological sort over `imports`/`depends_on`/`requires` edges. An edge `source → target` means "source depends on target," so the tour visits `target` first. Real codebases have circular imports — nodes caught in a cycle are appended afterward and explicitly flagged `cycle_fallback`, never silently mixed in as if they were cleanly ordered.

**Onboarding doc**: ranks "hub" modules by total edge degree (most-connected = worth understanding early), computed directly from the edge list — does **not** depend on graphify's `god_nodes`/community analysis files, which graphify deletes as intermediate scratch after each run and are not guaranteed to exist.

**Diff impact**: for each changed file, walks the graph **backward** (finds what depends on the changed file, not what the changed file depends on) up to a hop limit, grouped by distance. Get the changed-file list with:
```bash
git diff --name-only              # unstaged changes
git diff --name-only --cached     # staged changes
git diff --name-only HEAD~1       # vs. the previous commit
```
Then run: `python3 diff_impact.py graphify-out/graph.json <file1> <file2> ...`

This is a **read-only report over the graph** — it does not run tests or execute anything. It narrows *where to look*, it does not replace actually running the test suite.

## Common mistakes

1. Running this skill without checking `graphify-out/graph.json` exists first — there's nothing to read, and re-scanning the repo manually here duplicates graphify's job.
2. Treating a `cycle_fallback` node in the tour output as if it were cleanly topologically ordered — it wasn't; the graph has a circular dependency there.
3. Assuming diff-impact's "no dependents found" means the change is definitely safe — it means the graph shows no dependents; a genuinely new/untracked relationship (or a stale graph) can hide real impact. Suggest re-running graphify if the graph is old relative to the diff.
4. Treating the impact report as a substitute for running tests — it's a "where to look" map, not a correctness guarantee.

## Code

All four modules are pure stdlib (no dependencies) and independently self-testable:

- `graph_adapter.py` — schema-tolerant loader (`load_graph`, `normalize_node`, `normalize_edge`, `build_adjacency`)
- `build_tour.py` — `topological_tour(nodes, edges)`; CLI: `python3 build_tour.py graphify-out/graph.json`
- `build_onboarding.py` — `render_onboarding_doc(project_name, nodes, edges)`; CLI: `python3 build_onboarding.py graphify-out/graph.json "Project Name" > onboarding.md`
- `diff_impact.py` — `impact_of_changed_files(nodes, edges, changed_paths)`; CLI: `python3 diff_impact.py graphify-out/graph.json <changed files...>`

Run `python3 <file>.py` with no arguments for that module's self-test (uses synthetic in-memory graph data, not a real graph export).

## Known limitations

- **The exact field names in `graphify-out/graph.json` were not confirmed against a real export** — no sample was available when this skill was written; the schema was inferred from graphify's own SKILL.md, which shows intermediate shapes (`id`, `source`, `target`, etc.) but not the final `to_json()` output verbatim. `graph_adapter.py` is written defensively (tries several common key-name variants per field, e.g. `id`/`node_id`/`name`) specifically because of this uncertainty. **The first real run against an actual `graphify-out/graph.json` should be treated as the real validation** — if `load_graph` raises a "missing an id-like field" error, the real schema uses a field name not in this skill's variant list, and `NODE_ID_KEYS`/`EDGE_SOURCE_KEYS`/etc. in `graph_adapter.py` need a new entry added, not a workaround elsewhere.
- Onboarding "hub" ranking (edge degree) is a simple proxy for importance, not graphify's own god-node algorithm (which may use different centrality measures) — the numbers won't necessarily match `GRAPH_REPORT.md`'s own god-node list if that file is still around.
- Diff-impact's file-path matching (`find_node_by_path`) is a tolerant string match (exact or suffix), not a verified path-resolution — a very short or ambiguous path could match more than one node; the code takes the first match, which may not be the intended one on an ambiguous input.
