# repo-tour Usage Guide

`repo-tour` ([skills/research/repo-tour/](../skills/research/repo-tour/SKILL.md)) reads a knowledge graph that `graphify` already built (`graphify-out/graph.json`) and produces three things graphify doesn't: a dependency-ordered reading tour, an onboarding doc, and a diff-impact report. It never scans a repo or calls an LLM itself — it's a cheap, fast consumer of an existing graph.

This guide was written from an actual test run in this repo (`skills/trading/`, 2026-08-03), not from the design doc alone. Every command and output below is real.

## Prerequisite: a graph must already exist

```bash
/graphify <path>          # e.g. /graphify skills/trading
```

Check `graphify-out/graph.json` exists before running any `repo-tour` command. If it doesn't, run graphify first — `repo-tour` has nothing to read otherwise.

## Step-by-step: how this was tested

1. **Ran `/graphify skills/trading`** — a real, small (16-file) corpus: 6 Python scripts + 10 Markdown/YAML docs, deliberately chosen to be big enough for a real dependency graph but small enough to verify by hand.
2. AST extraction (deterministic, free) found **49 nodes, 103 edges** in the 6 `.py` files.
3. Semantic extraction (one subagent, since 10 docs fit in one chunk) found **51 nodes, 88 edges, 3 hyperedges** in the Markdown/YAML — cross-skill references like "Pairs with...", the router's "suggested chain", named concepts (yield trap, R-multiple, Kelly criterion), and a citation node for the upstream `tradermonty/claude-trading-skills` repo this skill set is inspired by.
4. Merged + built into a graph: **100 nodes, 164 edges, 10 communities** → `graphify-out/graph.json`.
5. Ran all three `repo-tour` scripts against that real file. **This surfaced real bugs that synthetic self-test data had not caught** — see "What testing against a real graph found" below.

## Commands

### 1. Guided tour — dependency-ordered reading list

```bash
python3 skills/research/repo-tour/build_tour.py graphify-out/graph.json
```

Real output (first lines, from the test run above):

```
1. drawdown_circuit_breaker_gate -- gate.py
2. drawdown_circuit_breaker_gate_compute_drawdown_pct -- compute_drawdown_pct()
3. drawdown_circuit_breaker_gate_evaluate_drawdown_gate -- evaluate_drawdown_gate()
4. drawdown_circuit_breaker_gate_gateresult -- GateResult
5. drawdown_circuit_breaker_gate_py_decimal -- Decimal
...
```

Files/symbols with no unresolved dependencies come first (`gate.py` has no imports besides stdlib `Decimal`), then their own contents, then progressively more-connected files. Entries flagged `[part of a dependency cycle]` mean graphify found a circular import — those didn't occur in this test corpus.

### 2. Onboarding doc

```bash
python3 skills/research/repo-tour/build_onboarding.py graphify-out/graph.json "skills/trading" > onboarding.md
```

Real output (excerpt):

```markdown
# Onboarding: skills/trading

Generated from a graph with 100 nodes and 164 edges.

## Start here — most-connected modules

- **skills_trading_position_sizer_skill** (connections: 12) — Position Sizer Skill
- **skills_trading_drawdown_circuit_breaker_skill** (connections: 10) — Drawdown Circuit Breaker Skill
- **skills_trading_skill** (connections: 9) — Trading Skills (Router)
- **skills_trading_trader_memory_core_skill** (connections: 9) — Trader Memory Core Skill
- **skills_trading_dividend_value_screener_skill** (connections: 8) — Dividend / Value Screener Skill
```

The hub ranking matches intuition: `position-sizer` and `drawdown-circuit-breaker` are the two skills every other trading skill's workflow references, so they come out on top by raw edge degree — without needing graphify's own (ephemeral, deleted-after-run) god-node analysis.

**Note on redirecting to a file on Windows**: the CLI forces UTF-8 stdout internally (`sys.stdout.reconfigure(encoding="utf-8")`) specifically so `> onboarding.md` doesn't corrupt non-ASCII characters like the em dash used throughout — this was a real bug caught during testing (see below), already fixed.

### 3. Diff impact — what does changing this file affect?

```bash
git diff --name-only              # get the real changed-file list
python3 skills/research/repo-tour/diff_impact.py graphify-out/graph.json <changed files...>
```

Two real tests from this run:

```
$ python3 diff_impact.py graphify-out/graph.json drawdown-circuit-breaker/gate.py
# Diff Impact Report

## drawdown-circuit-breaker/gate.py
- Graph node: `drawdown_circuit_breaker_gate`
- No dependents found — nothing else in the graph depends on this file.
```

This is a **correct, honest** result, not a bug: no other `.py` file in this corpus imports `gate.py` — each trading skill's script is deliberately standalone (see [skills/trading/SKILL.md](../skills/trading/SKILL.md)'s "Rules" section). The cross-skill relationship between `exposure-coach` and `drawdown-circuit-breaker` exists only in prose (`SKILL.md` links), not in code — `diff_impact` only follows structural edges (`imports_from`/`calls`/etc.) by design, not documentation cross-references. See SKILL.md's "Known limitations" for why that's intentional, not a gap to fix blindly.

```
$ python3 diff_impact.py graphify-out/graph.json SKILL.md
# Diff Impact Report

## SKILL.md
- Graph node: `skills_trading_skill`
- No dependents found — nothing else in the graph depends on this file.
```

(The router's own `SKILL.md` — correctly matched to the router node, not to a sub-skill's `SKILL.md`, after the path-matching fix below.)

## What testing against a real graph found

Before this test, `graph_adapter.py`'s field names were inferred from graphify's own SKILL.md — reasonable, but unconfirmed. Running the real pipeline surfaced two categories of finding:

**Confirmed correct on first try:**
- Edge `source`/`target` keys
- Node `id` key
- Node `community` key
- Falling back to `label` for a node's display text when there's no separate summary field

**Found and fixed by testing (would have silently produced wrong-but-plausible-looking output otherwise):**

| Bug | Symptom if unfixed | Fix |
|---|---|---|
| Edge list is under `"links"`, not `"edges"` | `load_graph()` would report **zero edges** on every real graph — no crash, just silently empty | Check `"links"` first, `"edges"` as fallback |
| Node type is `"file_type"`, not `"type"` | Every node's `type` would show `"unknown"` | Check `"file_type"` first |
| Node path is `"source_file"`, not `"filePath"`/`"path"` | `diff_impact.py` would never match any real file — every query would report "no matching node" | Check `"source_file"` first |
| Real import edge type is `"imports_from"`, not `"imports"` | Tour ordering and diff-impact would silently ignore all real Python import edges — output looks plausible, just incomplete | Added to both `DEPENDENCY_EDGE_TYPES` and `IMPACT_EDGE_TYPES` |
| `find_node_by_path`'s suffix match was too loose for bare filenames | Querying `"foo/SKILL.md"` incorrectly matched the router's own bare `"SKILL.md"` node too | Require the shorter path to contain `/` before allowing suffix matching |

None of these were caught by the original synthetic-data self-tests, because the synthetic fixtures used the *assumed* (wrong) key names consistently on both the producer and consumer side — a classic case of a test validating internal consistency, not real-world correctness. This is exactly why the SKILL.md always said "the first real run is the real validation," and why this test was worth doing before trusting the skill.

## Where the test artifacts live

`graphify-out/` in this repo root now contains a real, working example: `graph.json`, `GRAPH_REPORT.md`, `cost.json` — built from `skills/trading/`. Point any `repo-tour` command at it directly to see live output without re-running graphify.
