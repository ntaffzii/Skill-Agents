#!/usr/bin/env python3
"""build_tour.py -- dependency-ordered reading tour from a graphify-out/graph.json.

Orders nodes so foundational modules (things nothing else needs to understand
first) come before the modules that build on them -- a topological sort over
"depends on" edges (imports/depends_on/requires), read as: an edge
source -> target means "source depends on target", so target should be
understood first.

Real codebases have circular imports, so a full topological sort isn't always
possible. Nodes involved in a cycle are appended afterward, ordered by fewest
remaining unresolved dependencies -- each result entry says whether it was
placed by true topological order or by the cycle fallback, so that
distinction is never hidden.

Run `python3 build_tour.py` for the self-test, or
`python3 build_tour.py <graph.json>` to print a tour for a real graph.
"""
from __future__ import annotations

import sys

from graph_adapter import build_adjacency, load_graph

DEPENDENCY_EDGE_TYPES = {"imports", "imports_from", "depends_on", "requires"}


def topological_tour(nodes: list[dict], edges: list[dict], edge_types: set[str] = DEPENDENCY_EDGE_TYPES) -> list[dict]:
    node_ids = [n["id"] for n in nodes]
    node_id_set = set(node_ids)

    # dep_count[x] = number of not-yet-resolved dependencies x still has
    # dependents[y] = list of nodes that depend on y (so y must resolve before them)
    dep_count = {nid: 0 for nid in node_ids}
    dependents: dict[str, list[str]] = {nid: [] for nid in node_ids}

    for edge in edges:
        if edge["type"] not in edge_types:
            continue
        source, target = edge["source"], edge["target"]
        if source not in node_id_set or target not in node_id_set:
            continue  # dangling edge referencing a node outside this node list -- skip defensively
        if source == target:
            continue  # self-loop -- not a real ordering constraint
        dep_count[source] += 1
        dependents[target].append(source)

    ready = sorted(nid for nid in node_ids if dep_count[nid] == 0)
    order: list[dict] = []
    resolved: set[str] = set()

    while ready:
        nid = ready.pop(0)
        order.append({"id": nid, "resolved_by": "topological"})
        resolved.add(nid)
        newly_ready = []
        for dependent in dependents.get(nid, []):
            dep_count[dependent] -= 1
            if dep_count[dependent] == 0:
                newly_ready.append(dependent)
        ready = sorted(ready + newly_ready)

    # Cycle fallback: remaining nodes ordered by fewest unresolved deps, then id, for determinism
    remaining = sorted((nid for nid in node_ids if nid not in resolved), key=lambda nid: (dep_count[nid], nid))
    for nid in remaining:
        order.append({"id": nid, "resolved_by": "cycle_fallback"})

    return order


def _self_test() -> None:
    # Linear chain: A imports B, B imports C -- C has no deps, should come first
    nodes = [{"id": "A"}, {"id": "B"}, {"id": "C"}]
    edges = [
        {"source": "A", "target": "B", "type": "imports"},
        {"source": "B", "target": "C", "type": "imports"},
    ]
    order = topological_tour(nodes, edges)
    assert [item["id"] for item in order] == ["C", "B", "A"]
    assert all(item["resolved_by"] == "topological" for item in order)

    # No dependencies at all -- order falls back to id sort, all "topological" (trivially, dep_count=0 for all)
    isolated_nodes = [{"id": "Z"}, {"id": "Y"}]
    isolated_order = topological_tour(isolated_nodes, [])
    assert [item["id"] for item in isolated_order] == ["Y", "Z"]

    # Circular import: A imports B, B imports A -- neither can resolve, both go to cycle_fallback
    cyclic_nodes = [{"id": "A"}, {"id": "B"}]
    cyclic_edges = [
        {"source": "A", "target": "B", "type": "imports"},
        {"source": "B", "target": "A", "type": "imports"},
    ]
    cyclic_order = topological_tour(cyclic_nodes, cyclic_edges)
    assert {item["id"] for item in cyclic_order} == {"A", "B"}
    assert all(item["resolved_by"] == "cycle_fallback" for item in cyclic_order)

    # Dangling edge (target not in node list) is skipped, not a crash
    dangling_order = topological_tour([{"id": "A"}], [{"source": "A", "target": "ghost", "type": "imports"}])
    assert [item["id"] for item in dangling_order] == ["A"]

    # "imports_from" is graphify's real AST edge type for a Python import
    # (confirmed against a live graphify-out/graph.json, not "imports")
    real_type_order = topological_tour(
        [{"id": "A"}, {"id": "B"}],
        [{"source": "A", "target": "B", "type": "imports_from"}],
    )
    assert [item["id"] for item in real_type_order] == ["B", "A"]

    # Non-dependency edge types (e.g. "related") are ignored for ordering purposes --
    # both nodes have zero *dependency* edges, so both resolve immediately, in id order
    unrelated_order = topological_tour(
        [{"id": "A"}, {"id": "B"}],
        [{"source": "A", "target": "B", "type": "related"}],
    )
    assert [item["id"] for item in unrelated_order] == ["A", "B"]
    assert [item["resolved_by"] for item in unrelated_order] == ["topological", "topological"]

    print("All self-tests passed.")


def _main() -> None:
    # Force UTF-8 stdout: on Windows, redirecting output to a file (`> tour.md`) can
    # otherwise pick up the console's legacy codepage and write invalid UTF-8 bytes
    # for non-ASCII characters (e.g. the em dash used in node summaries below).
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print("Usage: python3 build_tour.py <graph.json>")
        raise SystemExit(1)
    graph = load_graph(sys.argv[1])
    order = topological_tour(graph["nodes"], graph["edges"])
    by_id = {n["id"]: n for n in graph["nodes"]}
    for i, item in enumerate(order, 1):
        node = by_id[item["id"]]
        flag = "" if item["resolved_by"] == "topological" else "  [part of a dependency cycle]"
        summary = f" -- {node['summary']}" if node["summary"] else ""
        print(f"{i}. {item['id']}{summary}{flag}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        _main()
    else:
        _self_test()
