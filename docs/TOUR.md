# Guided Tour

Dependency-ordered reading list, 100 entries.

1. `drawdown_circuit_breaker_gate_compute_drawdown_pct` — compute_drawdown_pct()
2. `drawdown_circuit_breaker_gate_evaluate_drawdown_gate` — evaluate_drawdown_gate()
3. `drawdown_circuit_breaker_gate_gateresult` — GateResult
4. `drawdown_circuit_breaker_gate_py_decimal` — Decimal
5. `drawdown_circuit_breaker_gate` — gate.py
6. `drawdown_circuit_breaker_gate_rationale_44` — Evaluate the configured drawdown thresholds against current drawdown.      thres
7. `drawdown_circuit_breaker_gate_self_test` — _self_test()
8. `exposure_coach_posture` — posture.py
9. `exposure_coach_posture_evaluate_posture` — evaluate_posture()
10. `exposure_coach_posture_postureresult` — PostureResult
11. `exposure_coach_posture_rationale_29` — Combine three inputs into a market-posture read.      breadth_pct / uptrend_pct:
12. `exposure_coach_posture_self_test` — _self_test()
13. `external_tradermonty_claude_trading_skills` — tradermonty/claude-trading-skills (GitHub repo, MIT)
14. `market_breadth_analyzer_breadth_breadthresult` — BreadthResult
15. `market_breadth_analyzer_breadth_classify_breadth` — classify_breadth()
16. `market_breadth_analyzer_breadth_compute_breadth` — compute_breadth()
17. `market_breadth_analyzer_breadth_compute_breadth_from_csv` — compute_breadth_from_csv()
18. `market_breadth_analyzer_breadth_py_decimal` — Decimal
19. `market_breadth_analyzer_breadth` — breadth.py
20. `market_breadth_analyzer_breadth_rationale_33` — rows: list of dicts with at least `price_field` and `ma_field` keys (numeric str
21. `market_breadth_analyzer_breadth_rationale_67` — Convenience wrapper: parse CSV text (header row required) and score it.
22. `market_breadth_analyzer_breadth_rationale_73` — Rough, configurable bands for talking about a breadth reading in plain language.
23. `market_breadth_analyzer_breadth_self_test` — _self_test()
24. `position_sizer_size_atr_based_size` — atr_based_size()
25. `position_sizer_size_atr_based_stop` — atr_based_stop()
26. `position_sizer_size_fixed_fractional_size` — fixed_fractional_size()
27. `position_sizer_size_kelly_fraction` — kelly_fraction()
28. `position_sizer_size_py_decimal` — Decimal
29. `position_sizer_size` — size.py
30. `position_sizer_size_rationale_31` — Risk a fixed percentage of account equity on this trade.      risk_pct: e.g. Dec
31. `position_sizer_size_rationale_61` — Compute a stop price a chosen multiple of ATR below entry (long trade).      ATR
32. `position_sizer_size_rationale_74` — Convenience wrapper: derive the stop from ATR, then size with the same risk budg
33. `position_sizer_size_rationale_80` — Kelly criterion fraction of capital to risk, from historical win/loss stats.
34. `position_sizer_size_self_test` — _self_test()
35. `position_sizer_size_sizeresult` — SizeResult
36. `skills_trading_dividend_value_screener_skill` — Dividend / Value Screener Skill
37. `skills_trading_dividend_value_screener_skill_debt_equity` — Debt/Equity Ratio
38. `skills_trading_dividend_value_screener_skill_dividend_growth_streak` — Dividend Growth Streak
39. `skills_trading_dividend_value_screener_skill_payout_ratio` — Payout Ratio (Dividend Sustainability)
40. `skills_trading_dividend_value_screener_skill_pe_ratio` — P/E Ratio
41. `skills_trading_dividend_value_screener_skill_yield_trap` — Yield Trap
42. `skills_trading_drawdown_circuit_breaker_gate_compute_drawdown_pct` — compute_drawdown_pct(peak_equity, current_equity)
43. `skills_trading_drawdown_circuit_breaker_gate_default_thresholds` — DEFAULT_THRESHOLDS
44. `skills_trading_drawdown_circuit_breaker_gate_evaluate_drawdown_gate` — evaluate_drawdown_gate(peak_equity, current_equity, thresholds)
45. `skills_trading_drawdown_circuit_breaker_skill` — Drawdown Circuit Breaker Skill
46. `skills_trading_drawdown_circuit_breaker_skill_drawdown_formula` — Drawdown Percentage Formula
47. `skills_trading_drawdown_circuit_breaker_skill_mechanical_rule_rationale` — Rationale: Mechanical Rules Over In-the-Moment Judgment
48. `skills_trading_drawdown_circuit_breaker_skill_size_multiplier_table` — Drawdown Threshold / Size Multiplier Table
49. `skills_trading_exposure_coach_posture_evaluate_posture` — evaluate_posture(breadth_pct, uptrend_pct, drawdown_action)
50. `skills_trading_exposure_coach_skill` — Exposure Coach Skill
51. `skills_trading_exposure_coach_skill_exposure_ceiling` — Exposure Ceiling
52. `skills_trading_exposure_coach_skill_priority_rule` — Rationale: Drawdown State Overrides Favorable Market Read
53. `skills_trading_market_breadth_analyzer_breadth_classify_breadth` — classify_breadth(pct_above)
54. `skills_trading_market_breadth_analyzer_breadth_compute_breadth` — compute_breadth(rows, price_field, ma_field)
55. `skills_trading_market_breadth_analyzer_breadth_compute_breadth_from_csv` — compute_breadth_from_csv(csv_text, ...)
56. `skills_trading_market_breadth_analyzer_skill` — Market Breadth Analyzer Skill
57. `skills_trading_market_breadth_analyzer_skill_breadth_definition` — Market Breadth Definition
58. `skills_trading_market_breadth_analyzer_skill_interpretation_bands` — Breadth Interpretation Bands
59. `skills_trading_portfolio_manager_skill` — Portfolio Manager Skill
60. `skills_trading_portfolio_manager_skill_concentration_check` — Concentration Check
61. `skills_trading_portfolio_manager_skill_payout_ratio_check` — Portfolio Dividend Payout Ratio Check
62. `skills_trading_portfolio_manager_skill_rebalance_triggers` — Rebalance Triggers
63. `skills_trading_position_sizer_size_atr_based_size` — atr_based_size(account_equity, risk_pct, entry_price, atr, multiplier)
64. `skills_trading_position_sizer_size_atr_based_stop` — atr_based_stop(entry_price, atr, multiplier)
65. `skills_trading_position_sizer_size_fixed_fractional_size` — fixed_fractional_size(account_equity, risk_pct, entry_price, stop_price)
66. `skills_trading_position_sizer_size_kelly_fraction` — kelly_fraction(win_rate, avg_win, avg_loss)
67. `skills_trading_position_sizer_skill` — Position Sizer Skill
68. `skills_trading_position_sizer_skill_atr_stop_concept` — ATR-Based Stop
69. `skills_trading_position_sizer_skill_fixed_fractional_sizing` — Fixed-Fractional Sizing
70. `skills_trading_position_sizer_skill_kelly_criterion_concept` — Kelly Criterion
71. `skills_trading_skill` — Trading Skills (Router)
72. `skills_trading_trader_memory_core_journal_schema` — Trade Journal Entry Schema (journal-schema.yaml)
73. `skills_trading_trader_memory_core_journal_stats_compute_r_multiple` — compute_r_multiple(entry, stop, exit_price)
74. `skills_trading_trader_memory_core_journal_stats_compute_trade_stats` — compute_trade_stats(trades)
75. `skills_trading_trader_memory_core_skill` — Trader Memory Core Skill
76. `skills_trading_trader_memory_core_skill_expectancy_concept` — Expectancy
77. `skills_trading_trader_memory_core_skill_r_multiple_concept` — R-Multiple
78. `skills_trading_trader_memory_core_skill_win_rate_concept` — Win Rate
79. `skills_trading_uptrend_analyzer_skill` — Uptrend Analyzer Skill
80. `skills_trading_uptrend_analyzer_skill_canslim_method` — CANSLIM Method
81. `skills_trading_uptrend_analyzer_skill_minervini_trend_template` — Minervini-Style Trend Template
82. `skills_trading_uptrend_analyzer_skill_stage_2_definition` — Stage 2 Uptrend Definition
83. `skills_trading_uptrend_analyzer_skill_weinstein_stage_analysis` — Stan Weinstein's Stage Analysis
84. `skills_trading_uptrend_analyzer_uptrend_compute_uptrend_participation` — compute_uptrend_participation(rows)
85. `skills_trading_uptrend_analyzer_uptrend_is_in_uptrend` — is_in_uptrend(price, ma50, ma200)
86. `trader_memory_core_journal_stats_compute_r_multiple` — compute_r_multiple()
87. `trader_memory_core_journal_stats_compute_trade_stats` — compute_trade_stats()
88. `trader_memory_core_journal_stats_py_decimal` — Decimal
89. `trader_memory_core_journal_stats` — journal_stats.py
90. `trader_memory_core_journal_stats_rationale_31` — R-multiple: how many multiples of the initial risk (entry-to-stop distance)
91. `trader_memory_core_journal_stats_rationale_48` — trades: list of dicts, each with an 'r_multiple' key (Decimal-like).      Use co
92. `trader_memory_core_journal_stats_self_test` — _self_test()
93. `trader_memory_core_journal_stats_tradestats` — TradeStats
94. `uptrend_analyzer_uptrend` — uptrend.py
95. `uptrend_analyzer_uptrend_compute_uptrend_participation` — compute_uptrend_participation()
96. `uptrend_analyzer_uptrend_is_in_uptrend` — is_in_uptrend()
97. `uptrend_analyzer_uptrend_rationale_28` — Stage-2-style uptrend test: price > 50MA and 50MA > 200MA.      Both legs matter
98. `uptrend_analyzer_uptrend_rationale_41` — rows: list of dicts with 'price', 'ma50', 'ma200' keys (numeric strings ok).
99. `uptrend_analyzer_uptrend_self_test` — _self_test()
100. `uptrend_analyzer_uptrend_uptrendresult` — UptrendResult