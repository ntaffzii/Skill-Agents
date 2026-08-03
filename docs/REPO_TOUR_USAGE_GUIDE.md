# graphify + repo-tour Usage Guide

Two tools, two different origins, used together:

- **`graphify`** — external tool (PyPI package `graphifyy`, plus a Claude Code skill installed at `~/.claude/skills/graphify/`). Not part of this repo. Scans a codebase and builds a persistent knowledge graph (`graphify-out/graph.json`).
- **`repo-tour`** ([skills/research/repo-tour/](../skills/research/repo-tour/SKILL.md)) — part of *this* repo. Reads whatever `graph.json` graphify already produced and answers three specific questions graphify itself doesn't: what order should I read this in, what's the onboarding summary, and what does changing this file affect. It never scans a repo or calls an LLM — pure Python, reads a JSON file that already exists.

```
graphify (external)  scans a project  →  graphify-out/graph.json
repo-tour (ours)      reads that file  →  tour / onboarding / diff-impact
```

This guide was written from real test runs in this repo, not from design docs alone. Every command and output below actually ran.

## Part 1 — graphify

### You do not need Claude Code to run it

`graphify` is a real installed CLI (`uv tool install graphifyy` puts `graphify.exe` on PATH). Two ways to build a graph, both work with zero agent involvement:

```bash
graphify extract <path> --code-only          # pure AST, no LLM, no API key, no cost at all
graphify extract <path> --backend ollama     # docs/papers too, using a local LLM (free) instead of Claude
graphify extract <path> --backend gemini     # or Gemini/OpenAI/DeepSeek/Claude via your own API key
```

`graphify extract` is documented by the tool itself as "headless full extraction (AST + semantic LLM) for CI/scripts" — built specifically for non-agent use. Real run from this session:

```
$ graphify extract skills/thai --code-only
[graphify extract] scanning skills/thai
[graphify extract] --code-only: skipping 20 non-code file(s) (20 docs, 0 papers, 0 images) — no LLM extraction
[graphify extract] found 7 code, 0 docs, 0 papers, 0 images
[graphify extract] AST extraction on 7 code files...
[graphify extract] wrote skills/thai/graphify-out/graph.json: 68 nodes, 108 edges, 12 communities
```

Zero LLM calls, zero cost, ran directly in a terminal.

### When you *are* inside an agent session (Claude Code)

The `/graphify` skill walks through the same pipeline manually, but for the semantic-extraction step (anything that isn't code) it dispatches Claude Code subagents instead of calling a separate paid API — that's an optimization for being inside an agent session already, not a requirement of the tool. A real semantic-extraction run in this repo (10 small Markdown files, one subagent) used **~116k output tokens**. That cost is real whichever path builds the graph — subagent dispatch or a configured `--backend` — so scope a graphify run to a subdirectory rather than a whole doc-heavy repo when you can.

### Two things graphify already does natively — check before reaching for repo-tour

- **`graphify query "<question>"`** / **`graphify explain "X"`** / **`graphify path "A" "B"`** — real standalone CLI commands, no agent needed, once a graph exists.
- **`graphify affected "X"`** — reverse-traversal impact analysis, built in. Its default relation set (`calls, indirect_call, references, imports, imports_from, re_exports, inherits, extends, implements, uses, mixes_in, embeds`) is *broader* than repo-tour's `diff_impact.py`. The difference is interface, not capability: `affected` takes one **node label** at a time; `diff_impact.py` takes a **list of changed file paths straight from `git diff`** and reports per file in one shot. Pick whichever matches how you're starting the question — from a diff, or from a symbol name you already know.

## Part 2 — repo-tour

### Prerequisite: a graph must already exist

```bash
graphify extract <path> --code-only    # or /graphify <path> inside an agent session
```

Check `graphify-out/graph.json` exists before running any `repo-tour` command — it never builds one itself.

### The three commands

```bash
python3 skills/research/repo-tour/build_tour.py graphify-out/graph.json [--out tour.md]
python3 skills/research/repo-tour/build_onboarding.py graphify-out/graph.json "Project Name" [--out onboarding.md]
python3 skills/research/repo-tour/diff_impact.py graphify-out/graph.json <changed files...> [--out impact.md]
```

Real output, run against this repo's own `skills/trading/` graph (100 nodes, 164 edges):

```
$ python3 build_onboarding.py graphify-out/graph.json "Trading Skills"
# Onboarding: Trading Skills

Generated from a graph with 100 nodes and 164 edges.

## Start here — most-connected modules

- **skills_trading_position_sizer_skill** (connections: 12) — Position Sizer Skill
- **skills_trading_drawdown_circuit_breaker_skill** (connections: 10) — Drawdown Circuit Breaker Skill
- **skills_trading_skill** (connections: 9) — Trading Skills (Router)
```

The hub ranking matches intuition without needing graphify's own (ephemeral, deleted-after-run) god-node analysis — `position-sizer` and `drawdown-circuit-breaker` really are the two skills every other trading skill's workflow references.

**The two quoted arguments across the three commands are not the same kind of thing** — this tripped up testing, worth being explicit:

| Command | The quoted argument is... | Must match the graph? |
|---|---|---|
| `build_onboarding.py <graph> "..."` | A free-text title for the doc header | No — literally anything, purely cosmetic |
| `diff_impact.py <graph> "..."` | A real file path | Yes — must match (or suffix-match) a real `source_file` in the graph, or you get "no matching node" |

### Not tied to one folder — proven, not just claimed

The same three scripts, unmodified, were run against a *second*, unrelated graph (`skills/thai/graphify-out/graph.json`, built separately via `graphify extract --code-only`) and produced correct output immediately — `thai_id_validate/validate.py` correctly ranked as the top hub (10 connections, the most functions). `repo-tour` takes a `graph.json` path as its only real input; it has no hardcoded assumption about which project or subfolder built it.

### Where to save each output — they don't all belong in the same place

| Output | Persist it? | Where | Why |
|---|---|---|---|
| Onboarding doc | Yes, commit it | `docs/ONBOARDING.md` | Read by multiple people, repeatedly, over time |
| Guided tour | Optional | `docs/TOUR.md` | Nice reference, less critical than onboarding |
| Diff impact | **No** — don't commit as a standing file | PR description or chat | Describes one specific uncommitted diff; stale and misleading the moment that diff changes or merges |

Never write any of the three into `graphify-out/` — that directory is gitignored (machine-local cache + an absolute interpreter path), so anything meant to be shared must go somewhere your VCS actually tracks. Real generated examples live at [docs/ONBOARDING.md](ONBOARDING.md) and [docs/TOUR.md](TOUR.md).

## What testing against a real graph found (worth knowing before you trust any of this blindly)

`graph_adapter.py`'s field names were originally inferred from graphify's own SKILL.md prose — reasonable, but unconfirmed. Running the real pipeline surfaced bugs a synthetic self-test using the same wrong assumption on both ends could never catch:

| Bug | Symptom if unfixed | Fix |
|---|---|---|
| Edge list is under `"links"`, not `"edges"` | `load_graph()` reports **zero edges** on every real graph — no crash, just silently empty | Check `"links"` first, `"edges"` as fallback |
| Node type is `"file_type"`, not `"type"` | Every node's type shows `"unknown"` | Check `"file_type"` first |
| Node path is `"source_file"`, not `"filePath"`/`"path"` | `diff_impact.py` never matches any real file | Check `"source_file"` first |
| Real import edge type is `"imports_from"`, not `"imports"` | Tour/diff-impact silently ignore real Python import edges — output looks plausible, just incomplete | Added to `DEPENDENCY_EDGE_TYPES` and `IMPACT_EDGE_TYPES` |
| Suffix path-matching too loose for bare filenames (e.g. graphify's own `"SKILL.md"` with no directory) | Querying `"foo/SKILL.md"` wrongly matched an unrelated bare `"SKILL.md"` node | Require the shorter path to contain `/` before suffix-matching applies |
| Onboarding's truncation note said "see the full graph" with no pointer | Reader hits a dead end at "... and 80 more" | Names the actual command (`build_tour.py --out`) and the real count |

Every fix above has a regression test that exercises the real shape, not just the originally-assumed one — see each script's `_self_test()`.

## Where the test artifacts live

- `graphify-out/` (repo root) — real graph built from `skills/trading/`: `graph.json`, `GRAPH_REPORT.md`, `cost.json`. Gitignored, regenerate with `graphify extract skills/trading` if missing.
- `skills/thai/graphify-out/` — real graph built from `skills/thai/`, code-only, used to prove repo-tour generalizes beyond one folder. Also gitignored.
- [docs/ONBOARDING.md](ONBOARDING.md) / [docs/TOUR.md](TOUR.md) — real, committed output from the `skills/trading/` graph.
