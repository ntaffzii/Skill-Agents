#!/usr/bin/env python3
"""build_onboarding.py -- generate an onboarding Markdown doc from a graphify-out/graph.json.

Finds "hub" modules (highest total edge degree -- the most-connected nodes,
a reasonable proxy for "things worth understanding early") computed directly
from the edge list, so this does not depend on graphify's own intermediate
analysis files (god_nodes, community labels), which are deleted after each
graphify run and are not guaranteed to be present.

Run `python3 build_onboarding.py` for the self-test, or
`python3 build_onboarding.py <graph.json> "<Project Name>"` for a real doc.
"""
from __future__ import annotations

import sys
from collections import Counter

from build_tour import topological_tour
from graph_adapter import load_graph, parse_out_flag, write_or_print


def compute_degree(edges: list[dict]) -> Counter:
    degree: Counter = Counter()
    for edge in edges:
        degree[edge["source"]] += 1
        degree[edge["target"]] += 1
    return degree


def top_hub_nodes(nodes: list[dict], edges: list[dict], limit: int = 5) -> list[dict]:
    degree = compute_degree(edges)
    by_id = {n["id"]: n for n in nodes}
    ranked = sorted(by_id.keys(), key=lambda nid: (-degree.get(nid, 0), nid))
    return [{"node": by_id[nid], "degree": degree.get(nid, 0)} for nid in ranked[:limit]]


def group_by_community(nodes: list[dict]) -> dict:
    groups: dict = {}
    for node in nodes:
        groups.setdefault(node["community"], []).append(node)
    return groups


def render_onboarding_doc(project_name: str, nodes: list[dict], edges: list[dict], hub_limit: int = 5, tour_limit: int = 20) -> str:
    hubs = top_hub_nodes(nodes, edges, hub_limit)
    tour = topological_tour(nodes, edges)

    lines = [f"# Onboarding: {project_name}", ""]
    lines.append(f"Generated from a graph with {len(nodes)} nodes and {len(edges)} edges.")
    lines.append("")
    lines.append("## Start here — most-connected modules")
    lines.append("")
    if hubs:
        for hub in hubs:
            node = hub["node"]
            summary = f" — {node['summary']}" if node["summary"] else ""
            lines.append(f"- **{node['id']}** (connections: {hub['degree']}){summary}")
    else:
        lines.append("_No nodes found._")
    lines.append("")

    if tour:
        lines.append("## Suggested reading order")
        lines.append("")
        by_id = {n["id"]: n for n in nodes}
        for i, item in enumerate(tour[:tour_limit], 1):
            node = by_id[item["id"]]
            flag = "" if item["resolved_by"] == "topological" else " _(part of a dependency cycle)_"
            summary = f" — {node['summary']}" if node["summary"] else ""
            lines.append(f"{i}. {item['id']}{summary}{flag}")
        if len(tour) > tour_limit:
            lines.append(
                f"- ... and {len(tour) - tour_limit} more — the onboarding doc only lists the "
                f"first {tour_limit} for readability. Run `python3 build_tour.py <graph.json> "
                f"--out TOUR.md` against the same graph for the complete {len(tour)}-entry order."
            )
        lines.append("")

    return "\n".join(lines)


def _self_test() -> None:
    nodes = [
        {"id": "core", "summary": "Core utilities", "community": 0, "raw": {}},
        {"id": "api", "summary": "API layer", "community": 0, "raw": {}},
        {"id": "ui", "summary": "UI components", "community": 1, "raw": {}},
    ]
    edges = [
        {"source": "api", "target": "core", "type": "imports", "weight": 1, "raw": {}},
        {"source": "ui", "target": "api", "type": "imports", "weight": 1, "raw": {}},
        {"source": "ui", "target": "core", "type": "related", "weight": 1, "raw": {}},
    ]

    degree = compute_degree(edges)
    assert degree["core"] == 2  # targeted by api and ui
    assert degree["api"] == 2   # source of one, target of one
    assert degree["ui"] == 2

    hubs = top_hub_nodes(nodes, edges, limit=2)
    assert len(hubs) == 2
    assert {h["node"]["id"] for h in hubs} <= {"core", "api", "ui"}

    groups = group_by_community(nodes)
    assert len(groups[0]) == 2  # core + api are both community 0
    assert len(groups[1]) == 1  # ui is community 1

    doc = render_onboarding_doc("Test Project", nodes, edges)
    assert "# Onboarding: Test Project" in doc
    assert "## Start here" in doc
    assert "## Suggested reading order" in doc
    assert "core" in doc  # the foundational, no-dependency node should appear
    assert "more" not in doc  # only 3 nodes, well under the default tour_limit=20 -- no truncation message

    # Truncation message: with more nodes than tour_limit, the doc must point
    # somewhere actionable (build_tour.py), not just say "see the full graph"
    # with no indication of how -- this exact gap was reported after a real run.
    many_nodes = [{"id": f"n{i}", "summary": "", "community": 0, "raw": {}} for i in range(25)]
    truncated_doc = render_onboarding_doc("Big Project", many_nodes, [], tour_limit=20)
    assert "... and 5 more" in truncated_doc
    assert "build_tour.py" in truncated_doc
    assert "--out" in truncated_doc

    # Empty graph doesn't crash, produces a doc that says so
    empty_doc = render_onboarding_doc("Empty Project", [], [])
    assert "No nodes found" in empty_doc

    print("All self-tests passed.")


def _main() -> None:
    # Force UTF-8 stdout: on Windows, redirecting output to a file (`> onboarding.md`)
    # can otherwise pick up the console's legacy codepage and write invalid UTF-8
    # bytes for non-ASCII characters (e.g. the em dash used throughout this doc).
    sys.stdout.reconfigure(encoding="utf-8")
    argv, out_path = parse_out_flag(sys.argv[1:])
    if len(argv) < 1:
        print('Usage: python3 build_onboarding.py <graph.json> "<Project Name>" [--out onboarding.md]')
        raise SystemExit(1)
    graph = load_graph(argv[0])
    project_name = argv[1] if len(argv) > 1 else "Project"
    write_or_print(render_onboarding_doc(project_name, graph["nodes"], graph["edges"]), out_path)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        _main()
    else:
        _self_test()
