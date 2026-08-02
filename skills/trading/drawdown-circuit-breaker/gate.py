#!/usr/bin/env python3
"""gate.py -- drawdown-based risk gate: reduce or halt new position-taking after equity falls from its peak.

A circuit breaker is a mechanical rule, not a prediction -- it does not know
whether a further decline is coming. It exists to enforce a pre-committed
discipline (cut risk when losing, rather than deciding in the moment) since
that decision is well documented as being harder to make well under stress
than to set in advance. Not financial advice.

Run `python3 gate.py` for the self-test.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class GateResult:
    drawdown_pct: Decimal
    action: str  # "full_size" | "reduced_size" | "halt_new_positions"
    size_multiplier: Decimal  # multiply normal position size by this


DEFAULT_THRESHOLDS = (
    # (drawdown_pct_trigger, action, size_multiplier) -- sorted by severity below
    (Decimal("10"), "reduced_size", Decimal("0.5")),
    (Decimal("15"), "halt_new_positions", Decimal("0")),
)


def compute_drawdown_pct(peak_equity, current_equity) -> Decimal:
    peak_equity = Decimal(str(peak_equity))
    current_equity = Decimal(str(current_equity))
    if peak_equity <= 0:
        raise ValueError("peak_equity must be positive")
    if current_equity > peak_equity:
        # current equity is a new high -- drawdown is 0, not negative
        return Decimal("0")
    return ((peak_equity - current_equity) / peak_equity * 100).quantize(Decimal("0.01"))


def evaluate_drawdown_gate(peak_equity, current_equity, thresholds=DEFAULT_THRESHOLDS) -> GateResult:
    """Evaluate the configured drawdown thresholds against current drawdown.

    thresholds: iterable of (trigger_pct, action, size_multiplier), most
    severe last-matching threshold wins (a -18% drawdown matches both the
    10% and 15% triggers here; the 15% one -- the more severe -- governs).
    Defaults are illustrative starting points, not a validated rule set;
    tune them to the user's own risk tolerance and strategy history.
    """
    drawdown_pct = compute_drawdown_pct(peak_equity, current_equity)

    action = "full_size"
    size_multiplier = Decimal("1")
    for trigger_pct, trigger_action, trigger_multiplier in sorted(thresholds, key=lambda t: t[0]):
        if drawdown_pct >= trigger_pct:
            action = trigger_action
            size_multiplier = trigger_multiplier

    return GateResult(drawdown_pct=drawdown_pct, action=action, size_multiplier=size_multiplier)


def _self_test() -> None:
    # No drawdown
    r = evaluate_drawdown_gate(peak_equity=100_000, current_equity=100_000)
    assert r.drawdown_pct == Decimal("0.00")
    assert r.action == "full_size"
    assert r.size_multiplier == Decimal("1")

    # New equity high -- drawdown is 0, not negative
    r_new_high = evaluate_drawdown_gate(peak_equity=100_000, current_equity=105_000)
    assert r_new_high.drawdown_pct == Decimal("0")

    # 8% drawdown -- below the 10% trigger, still full size
    r_small = evaluate_drawdown_gate(peak_equity=100_000, current_equity=92_000)
    assert r_small.action == "full_size"

    # 12% drawdown -- crosses the 10% trigger, reduced size
    r_med = evaluate_drawdown_gate(peak_equity=100_000, current_equity=88_000)
    assert r_med.drawdown_pct == Decimal("12.00")
    assert r_med.action == "reduced_size"
    assert r_med.size_multiplier == Decimal("0.5")

    # 18% drawdown -- crosses both triggers, most severe (halt) governs
    r_severe = evaluate_drawdown_gate(peak_equity=100_000, current_equity=82_000)
    assert r_severe.action == "halt_new_positions"
    assert r_severe.size_multiplier == Decimal("0")

    # Invalid peak equity is rejected, not silently mishandled
    try:
        compute_drawdown_pct(peak_equity=0, current_equity=100)
        assert False, "expected ValueError"
    except ValueError:
        pass

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
