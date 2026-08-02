#!/usr/bin/env python3
"""graph_adapter.py -- schema-tolerant loader/normalizer for a graphify-style graph.json.

Field names below are confirmed against graphify's actual installed source
(graphify/export.py's to_json(), read directly -- not guessed) as of the
version installed when this was verified: graph.json is produced by
networkx.readwrite.json_graph.node_link_data(G, edges="links"), which means:

- The top-level edge list key is **"links"**, not "edges" (confirmed live:
  a naive `raw["edges"]` silently returns nothing against a real export).
- Node type lives in **"file_type"** (code/document/paper/image/rationale/
  concept), not "type".
- Node file path lives in **"source_file"**, not "filePath"/"path".
- Node display name lives in **"label"**, not "summary" (there is no
  separate summary field on a real node).
- Edge relation type lives in **"relation"** (calls/imports/implements/...),
  confidence in "confidence" (EXTRACTED/INFERRED/AMBIGUOUS) and
  "confidence_score" (0-1 float).

Every field lookup still tries multiple key-name variants (the confirmed
name first) rather than hard-coding one exact key -- graphify is an actively
developed external project and its export schema could still change between
versions. Run `python3 graph_adapter.py` for the self-test.
"""
from __future__ import annotations

import json
from pathlib import Path

NODE_ID_KEYS = ["id", "node_id", "name"]
NODE_TYPE_KEYS = ["file_type", "type", "node_type", "kind"]
NODE_PATH_KEYS = ["source_file", "filePath", "file_path", "path", "source_location", "location"]
NODE_SUMMARY_KEYS = ["summary", "description", "label"]
NODE_COMMUNITY_KEYS = ["community", "cluster", "community_id"]

EDGE_SOURCE_KEYS = ["source", "from", "src", "start"]
EDGE_TARGET_KEYS = ["target", "to", "dst", "end"]
EDGE_TYPE_KEYS = ["relation", "type", "edge_type", "kind"]
EDGE_WEIGHT_KEYS = ["confidence_score", "weight", "confidence"]

# Top-level key holding the edge list. graphify's node_link_data(..., edges="links")
# renames it to "links"; some other tools/older versions may still use "edges".
EDGE_LIST_KEYS = ["links", "edges"]


def _first_present(d: dict, keys: list[str], default=None):
    for key in keys:
        if key in d and d[key] is not None:
            return d[key]
    return default


def normalize_node(raw: dict) -> dict:
    node_id = _first_present(raw, NODE_ID_KEYS)
    if node_id is None:
        raise ValueError(f"node is missing an id-like field (tried {NODE_ID_KEYS}): {raw!r}")
    return {
        "id": node_id,
        "type": _first_present(raw, NODE_TYPE_KEYS, "unknown"),
        "path": _first_present(raw, NODE_PATH_KEYS),
        "summary": _first_present(raw, NODE_SUMMARY_KEYS, ""),
        "community": _first_present(raw, NODE_COMMUNITY_KEYS),
        "raw": raw,
    }


def normalize_edge(raw: dict) -> dict:
    source = _first_present(raw, EDGE_SOURCE_KEYS)
    target = _first_present(raw, EDGE_TARGET_KEYS)
    if source is None or target is None:
        raise ValueError(f"edge is missing a source/target-like field: {raw!r}")
    return {
        "source": source,
        "target": target,
        "type": _first_present(raw, EDGE_TYPE_KEYS, "related"),
        "weight": _first_present(raw, EDGE_WEIGHT_KEYS, 1),
        "raw": raw,
    }


def load_graph(path: str) -> dict:
    """Load and normalize a graphify-out/graph.json (or compatible) file.

    Raises ValueError with a clear message if the file has no 'nodes' array
    -- the surest sign this isn't actually a graph export -- rather than
    returning an empty, silently-useless result.
    """
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    raw_nodes = raw.get("nodes", [])
    raw_edges = _first_present(raw, EDGE_LIST_KEYS, [])
    if not raw_nodes:
        raise ValueError(
            f"{path}: no non-empty 'nodes' array found -- is this really a graph.json? "
            "Run graphify (or the tool that produced it) first."
        )
    nodes = [normalize_node(n) for n in raw_nodes]
    edges = [normalize_edge(e) for e in raw_edges]
    return {"nodes": nodes, "edges": edges, "raw": raw}


def parse_out_flag(argv: list[str]) -> tuple[list[str], str | None]:
    """Extract an optional `--out <path>` flag from a CLI argv list.

    Returns (remaining_argv, out_path); out_path is None if --out wasn't given.
    Shared by all three repo-tour CLIs so `--out report.md` behaves identically
    everywhere instead of each script reinventing its own flag parsing.
    """
    argv = list(argv)
    if "--out" in argv:
        idx = argv.index("--out")
        if idx + 1 >= len(argv):
            raise ValueError("--out requires a path argument")
        out_path = argv[idx + 1]
        del argv[idx : idx + 2]
        return argv, out_path
    return argv, None


def write_or_print(text: str, out_path: str | None) -> None:
    """Write `text` to out_path (UTF-8, creating parent directories) if given, else print it.

    Centralizes the UTF-8-safe write so every CLI's `--out` path behaves the
    same way regardless of the console's codepage (see the stdout-encoding
    fix in each script's _main for why this matters on Windows).
    """
    if out_path:
        path = Path(out_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"Wrote {path}")
    else:
        print(text)


def build_adjacency(edges: list[dict], edge_types: set[str] | None = None) -> tuple[dict, dict]:
    """forward[node_id] -> list of edges where node_id is the source.
    reverse[node_id] -> list of edges where node_id is the target.

    edge_types: if given, only include edges whose normalized type is in this set.
    """
    forward: dict[str, list[dict]] = {}
    reverse: dict[str, list[dict]] = {}
    for edge in edges:
        if edge_types is not None and edge["type"] not in edge_types:
            continue
        forward.setdefault(edge["source"], []).append(edge)
        reverse.setdefault(edge["target"], []).append(edge)
    return forward, reverse


def _self_test() -> None:
    # Real graphify node shape (confirmed against graphify/export.py): file_type,
    # source_file, label -- not type/filePath/summary.
    real_shape_node = normalize_node({
        "id": "skills_trading_position_sizer_size_fixed_fractional_size",
        "file_type": "code",
        "source_file": "skills/trading/position-sizer/size.py",
        "label": "fixed_fractional_size",
        "community": 2,
    })
    assert real_shape_node["type"] == "code"
    assert real_shape_node["path"] == "skills/trading/position-sizer/size.py"
    assert real_shape_node["summary"] == "fixed_fractional_size"  # falls back to label
    assert real_shape_node["community"] == 2

    # Nodes using other key-name conventions -- both must normalize the same way
    node_a = normalize_node({"id": "file:a.py", "type": "file", "filePath": "a.py", "summary": "Module A"})
    node_b = normalize_node({"node_id": "file:b.py", "node_type": "file", "path": "b.py"})
    assert node_a["id"] == "file:a.py"
    assert node_a["path"] == "a.py"
    assert node_b["id"] == "file:b.py"
    assert node_b["path"] == "b.py"
    assert node_b["summary"] == ""  # default when no summary-like field present

    # Missing id-like field raises a clear error instead of silently using None
    try:
        normalize_node({"type": "file"})
        assert False, "expected ValueError"
    except ValueError:
        pass

    # Real graphify edge shape: relation + confidence_score, not type/weight
    real_shape_edge = normalize_edge({
        "source": "a_py_foo", "target": "b_py_bar", "relation": "calls", "confidence_score": 0.85,
    })
    assert real_shape_edge["type"] == "calls"
    assert real_shape_edge["weight"] == 0.85

    # Edges using other key-name conventions
    edge = normalize_edge({"from": "file:a.py", "to": "file:b.py", "relation": "imports"})
    assert edge["source"] == "file:a.py"
    assert edge["target"] == "file:b.py"
    assert edge["type"] == "imports"
    assert edge["weight"] == 1  # default

    try:
        normalize_edge({"type": "imports"})
        assert False, "expected ValueError"
    except ValueError:
        pass

    # build_adjacency with a type filter
    edges = [
        normalize_edge({"source": "a", "target": "b", "type": "imports"}),
        normalize_edge({"source": "a", "target": "c", "type": "related"}),
    ]
    forward, reverse = build_adjacency(edges, edge_types={"imports"})
    assert [e["target"] for e in forward["a"]] == ["b"]
    assert "a" not in {e["source"] for e in forward.get("c", [])}  # "related" edge filtered out
    assert reverse["b"][0]["source"] == "a"

    # load_graph resolves the edge list from "links" (graphify's real key) before "edges"
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        links_path = Path(tmpdir) / "links-style.json"
        links_path.write_text(json.dumps({
            "nodes": [{"id": "x", "file_type": "code", "source_file": "x.py", "label": "X"}],
            "links": [{"source": "x", "target": "x", "relation": "self_ref"}],
        }), encoding="utf-8")
        graph = load_graph(str(links_path))
        assert len(graph["nodes"]) == 1
        assert len(graph["edges"]) == 1
        assert graph["edges"][0]["type"] == "self_ref"

    # parse_out_flag: present, absent, and at-the-end-with-no-value cases
    remaining, out_path = parse_out_flag(["graph.json", "--out", "report.md"])
    assert remaining == ["graph.json"]
    assert out_path == "report.md"
    remaining2, out_path2 = parse_out_flag(["graph.json", "file1.py", "file2.py"])
    assert remaining2 == ["graph.json", "file1.py", "file2.py"]
    assert out_path2 is None
    try:
        parse_out_flag(["graph.json", "--out"])
        assert False, "expected ValueError"
    except ValueError:
        pass

    # write_or_print: no out_path prints (can't easily assert stdout here without
    # capturing it, so just confirm it doesn't raise); with out_path it writes UTF-8
    # and creates parent directories that don't exist yet
    write_or_print("hello", None)
    with tempfile.TemporaryDirectory() as tmpdir:
        nested_path = Path(tmpdir) / "nested" / "report.md"
        write_or_print("# Report\n\nSome em dash — text.", str(nested_path))
        assert nested_path.exists()
        assert nested_path.read_text(encoding="utf-8") == "# Report\n\nSome em dash — text."

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
