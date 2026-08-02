#!/usr/bin/env python3
"""posture.py -- combine breadth, uptrend participation, and drawdown state into one market-posture read.

This is a rule-based aggregator over the outputs of market-breadth-analyzer,
uptrend-analyzer, and drawdown-circuit-breaker -- it does not fetch or
compute those inputs itself. Not financial advice: this is one configurable
heuristic for summarizing "how much new risk does today's data support,"
not a signal to act on mechanically.

Run `python3 posture.py` for the self-test.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class PostureResult:
    exposure_ceiling: str  # "high" | "moderate" | "low" | "minimal"
    reasons: list[str]


def evaluate_posture(
    breadth_pct,
    uptrend_pct,
    drawdown_action: str = "full_size",
) -> PostureResult:
    """Combine three inputs into a market-posture read.

    breadth_pct / uptrend_pct: Decimal-like percentages (0-100), from
    market-breadth-analyzer and uptrend-analyzer respectively.
    drawdown_action: the `action` field from drawdown-circuit-breaker's
    GateResult ("full_size" | "reduced_size" | "halt_new_positions") --
    the account's own risk state always overrides a favorable market read.
    """
    breadth_pct = Decimal(str(breadth_pct))
    uptrend_pct = Decimal(str(uptrend_pct))
    reasons: list[str] = []

    # Account-level risk gate takes priority over market conditions --
    # a favorable market doesn't override a personal drawdown rule.
    if drawdown_action == "halt_new_positions":
        return PostureResult(
            exposure_ceiling="minimal",
            reasons=["drawdown circuit breaker is active (halt_new_positions) -- overrides market read"],
        )

    if breadth_pct >= 60 and uptrend_pct >= 50:
        ceiling = "high"
        reasons.append(f"broad breadth ({breadth_pct}%) and strong uptrend participation ({uptrend_pct}%)")
    elif breadth_pct >= 40 and uptrend_pct >= 30:
        ceiling = "moderate"
        reasons.append(f"moderate breadth ({breadth_pct}%) and uptrend participation ({uptrend_pct}%)")
    else:
        ceiling = "low"
        reasons.append(f"narrow breadth ({breadth_pct}%) and/or weak uptrend participation ({uptrend_pct}%)")

    if drawdown_action == "reduced_size":
        # Cap the ceiling by one notch when the account is already in a drawdown-reduced state
        downgrade = {"high": "moderate", "moderate": "low", "low": "minimal"}
        reasons.append("drawdown circuit breaker is in reduced_size state -- capped one notch")
        ceiling = downgrade[ceiling]

    return PostureResult(exposure_ceiling=ceiling, reasons=reasons)


def _self_test() -> None:
    r = evaluate_posture(breadth_pct=70, uptrend_pct=60)
    assert r.exposure_ceiling == "high"

    r2 = evaluate_posture(breadth_pct=45, uptrend_pct=35)
    assert r2.exposure_ceiling == "moderate"

    r3 = evaluate_posture(breadth_pct=20, uptrend_pct=10)
    assert r3.exposure_ceiling == "low"

    # Favorable market read, but drawdown gate halts -- account risk state wins
    r4 = evaluate_posture(breadth_pct=80, uptrend_pct=70, drawdown_action="halt_new_positions")
    assert r4.exposure_ceiling == "minimal"

    # Favorable market read, but reduced_size downgrades one notch
    r5 = evaluate_posture(breadth_pct=70, uptrend_pct=60, drawdown_action="reduced_size")
    assert r5.exposure_ceiling == "moderate"  # would be "high", downgraded to "moderate"

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
