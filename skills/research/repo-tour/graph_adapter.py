#!/usr/bin/env python3
"""graph_adapter.py -- schema-tolerant loader/normalizer for a graphify-style graph.json.

Why defensive parsing: this module's field-name list was inferred from
graphify's own SKILL.md (which shows intermediate extraction shapes like
{"id": ..., "source": ..., "target": ...}) rather than confirmed against a
real graphify-out/graph.json export -- no sample was available when this was
written. Rather than hard-code one assumed schema and silently mis-parse a
differently-shaped export, every field lookup tries several common key name
variants and fails loudly (ValueError) if none match, instead of guessing.

Run `python3 graph_adapter.py` for the self-test (uses synthetic data, not a
real graph export -- see SKILL.md "Known limitations").
"""
from __future__ import annotations

import json
from pathlib import Path

NODE_ID_KEYS = ["id", "node_id", "name"]
NODE_TYPE_KEYS = ["type", "node_type", "kind"]
NODE_PATH_KEYS = ["filePath", "file_path", "path", "source_location", "location"]
NODE_SUMMARY_KEYS = ["summary", "description", "label"]
NODE_COMMUNITY_KEYS = ["community", "cluster", "community_id"]

EDGE_SOURCE_KEYS = ["source", "from", "src", "start"]
EDGE_TARGET_KEYS = ["target", "to", "dst", "end"]
EDGE_TYPE_KEYS = ["type", "edge_type", "relation", "kind"]
EDGE_WEIGHT_KEYS = ["weight", "confidence"]


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
    raw_edges = raw.get("edges", [])
    if not raw_nodes:
        raise ValueError(
            f"{path}: no non-empty 'nodes' array found -- is this really a graph.json? "
            "Run graphify (or the tool that produced it) first."
        )
    nodes = [normalize_node(n) for n in raw_nodes]
    edges = [normalize_edge(e) for e in raw_edges]
    return {"nodes": nodes, "edges": edges, "raw": raw}


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
    # Nodes using different key-name conventions -- both must normalize the same way
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

    # Edges using different key-name conventions
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

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
