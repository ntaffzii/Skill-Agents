#!/usr/bin/env python3
"""diff_impact.py -- what does a set of changed files affect, per a graphify-out/graph.json?

For each changed file, walks the graph *backward* along dependency edges
(imports/depends_on/requires/calls) -- i.e. finds nodes that depend on the
changed file, not what the changed file depends on -- since those are the
things whose behavior could break from this change. Grouped by hop distance
so directly-affected code is distinguished from further ripple effects.

This does not run or execute anything -- it is a read-only report over the
existing graph. It does not replace actually running the test suite.

Run `python3 diff_impact.py` for the self-test, or
`python3 diff_impact.py <graph.json> <changed_file1> [changed_file2 ...]`
for a real report (get the changed-file list from `git diff --name-only`).
"""
from __future__ import annotations

import sys

from graph_adapter import build_adjacency, load_graph

IMPACT_EDGE_TYPES = {"imports", "depends_on", "requires", "calls"}


def find_node_by_path(nodes: list[dict], file_path: str) -> list[dict]:
    """Match a file path against node['path'], tolerant of relative-vs-absolute
    and leading-slash differences (endswith in both directions)."""
    matches = []
    for node in nodes:
        node_path = node["path"]
        if not node_path:
            continue
        if node_path == file_path or node_path.endswith(file_path) or file_path.endswith(node_path):
            matches.append(node)
    return matches


def impact_of_changed_files(
    nodes: list[dict],
    edges: list[dict],
    changed_paths: list[str],
    max_hops: int = 2,
    edge_types: set[str] = IMPACT_EDGE_TYPES,
) -> dict:
    _, reverse = build_adjacency(edges, edge_types)

    result: dict = {}
    for path in changed_paths:
        matches = find_node_by_path(nodes, path)
        if not matches:
            result[path] = {"matched_node": None, "impacted": {}}
            continue

        start_id = matches[0]["id"]
        visited = {start_id: 0}
        frontier = [start_id]
        hop = 0
        while frontier and hop < max_hops:
            hop += 1
            next_frontier = []
            for nid in frontier:
                for edge in reverse.get(nid, []):
                    source = edge["source"]
                    if source not in visited:
                        visited[source] = hop
                        next_frontier.append(source)
            frontier = next_frontier

        impacted_by_hop: dict[int, list[str]] = {}
        for nid, h in visited.items():
            if nid == start_id:
                continue
            impacted_by_hop.setdefault(h, []).append(nid)
        for h in impacted_by_hop:
            impacted_by_hop[h].sort()

        result[path] = {"matched_node": start_id, "impacted": impacted_by_hop}
    return result


def render_impact_report(result: dict) -> str:
    lines = ["# Diff Impact Report", ""]
    for path, info in result.items():
        lines.append(f"## {path}")
        if info["matched_node"] is None:
            lines.append("- No matching node found in the graph (new file, or graph is stale — consider re-running graphify).")
            lines.append("")
            continue
        lines.append(f"- Graph node: `{info['matched_node']}`")
        if not info["impacted"]:
            lines.append("- No dependents found — nothing else in the graph depends on this file.")
        else:
            for hop in sorted(info["impacted"]):
                label = "Directly depends on this file" if hop == 1 else f"{hop} hops away (transitive)"
                lines.append(f"- {label}: {', '.join(info['impacted'][hop])}")
        lines.append("")
    return "\n".join(lines)


def _self_test() -> None:
    # A depends on B, B depends on C, D depends on A (chain: D -> A -> B -> C)
    nodes = [
        {"id": "A", "path": "a.py"},
        {"id": "B", "path": "b.py"},
        {"id": "C", "path": "c.py"},
        {"id": "D", "path": "d.py"},
    ]
    edges = [
        {"source": "A", "target": "B", "type": "imports"},
        {"source": "B", "target": "C", "type": "imports"},
        {"source": "D", "target": "A", "type": "imports"},
    ]

    result = impact_of_changed_files(nodes, edges, ["b.py"], max_hops=2)
    info = result["b.py"]
    assert info["matched_node"] == "B"
    assert info["impacted"] == {1: ["A"], 2: ["D"]}

    # max_hops=1 stops before reaching D
    shallow = impact_of_changed_files(nodes, edges, ["b.py"], max_hops=1)
    assert shallow["b.py"]["impacted"] == {1: ["A"]}

    # A file with no dependents
    leaf_result = impact_of_changed_files(nodes, edges, ["d.py"])
    assert leaf_result["d.py"]["impacted"] == {}

    # A file not present in the graph at all
    missing_result = impact_of_changed_files(nodes, edges, ["nonexistent.py"])
    assert missing_result["nonexistent.py"]["matched_node"] is None

    # find_node_by_path tolerates a relative vs. project-relative path mismatch
    matches = find_node_by_path(nodes, "./b.py".lstrip("./"))
    assert matches[0]["id"] == "B"

    report = render_impact_report(result)
    assert "b.py" in report
    assert "Directly depends on this file: A" in report
    assert "2 hops away (transitive): D" in report

    missing_report = render_impact_report(missing_result)
    assert "No matching node found" in missing_report

    print("All self-tests passed.")


def _main() -> None:
    # Force UTF-8 stdout: on Windows, redirecting output to a file (`> impact.md`) can
    # otherwise pick up the console's legacy codepage and write invalid UTF-8 bytes.
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        print("Usage: python3 diff_impact.py <graph.json> <changed_file1> [changed_file2 ...]")
        raise SystemExit(1)
    graph = load_graph(sys.argv[1])
    changed_paths = sys.argv[2:]
    result = impact_of_changed_files(graph["nodes"], graph["edges"], changed_paths)
    print(render_impact_report(result))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        _main()
    else:
        _self_test()
