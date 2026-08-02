# Onboarding: Skill-Agents — Trading Skills

Generated from a graph with 100 nodes and 164 edges.

## Start here — most-connected modules

- **skills_trading_position_sizer_skill** (connections: 12) — Position Sizer Skill
- **skills_trading_drawdown_circuit_breaker_skill** (connections: 10) — Drawdown Circuit Breaker Skill
- **skills_trading_skill** (connections: 9) — Trading Skills (Router)
- **skills_trading_trader_memory_core_skill** (connections: 9) — Trader Memory Core Skill
- **skills_trading_dividend_value_screener_skill** (connections: 8) — Dividend / Value Screener Skill

## Suggested reading order

1. drawdown_circuit_breaker_gate_compute_drawdown_pct — compute_drawdown_pct()
2. drawdown_circuit_breaker_gate_evaluate_drawdown_gate — evaluate_drawdown_gate()
3. drawdown_circuit_breaker_gate_gateresult — GateResult
4. drawdown_circuit_breaker_gate_py_decimal — Decimal
5. drawdown_circuit_breaker_gate — gate.py
6. drawdown_circuit_breaker_gate_rationale_44 — Evaluate the configured drawdown thresholds against current drawdown.      thres
7. drawdown_circuit_breaker_gate_self_test — _self_test()
8. exposure_coach_posture — posture.py
9. exposure_coach_posture_evaluate_posture — evaluate_posture()
10. exposure_coach_posture_postureresult — PostureResult
11. exposure_coach_posture_rationale_29 — Combine three inputs into a market-posture read.      breadth_pct / uptrend_pct:
12. exposure_coach_posture_self_test — _self_test()
13. external_tradermonty_claude_trading_skills — tradermonty/claude-trading-skills (GitHub repo, MIT)
14. market_breadth_analyzer_breadth_breadthresult — BreadthResult
15. market_breadth_analyzer_breadth_classify_breadth — classify_breadth()
16. market_breadth_analyzer_breadth_compute_breadth — compute_breadth()
17. market_breadth_analyzer_breadth_compute_breadth_from_csv — compute_breadth_from_csv()
18. market_breadth_analyzer_breadth_py_decimal — Decimal
19. market_breadth_analyzer_breadth — breadth.py
20. market_breadth_analyzer_breadth_rationale_33 — rows: list of dicts with at least `price_field` and `ma_field` keys (numeric str
- ... and 80 more — the onboarding doc only lists the first 20 for readability. Run `python3 build_tour.py <graph.json> --out TOUR.md` against the same graph for the complete 100-entry order.
