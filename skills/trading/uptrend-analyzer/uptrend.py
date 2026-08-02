#!/usr/bin/env python3
"""uptrend.py -- uptrend participation scoring from a plain CSV, no API key required.

Complements market-breadth-analyzer (price vs. a single MA) with a stricter,
commonly used "stage 2 uptrend" heuristic: price above the 50-day MA AND the
50-day MA above the 200-day MA. This is a well-known screening heuristic
(associated with Stan Weinstein's stage analysis and used in various forms by
CANSLIM/Minervini-style trend-following approaches) -- not a proprietary
formula, and not the only valid definition of "uptrend."

Not financial advice. Run `python3 uptrend.py` for the self-test.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class UptrendResult:
    total: int
    in_uptrend: int
    excluded: int
    pct_uptrend: Decimal


def is_in_uptrend(price, ma50, ma200) -> bool:
    """Stage-2-style uptrend test: price > 50MA and 50MA > 200MA.

    Both legs matter: price above a rising short MA without the short MA
    being above the long MA is often still a base or early recovery, not an
    established uptrend by this definition.
    """
    price = Decimal(str(price))
    ma50 = Decimal(str(ma50))
    ma200 = Decimal(str(ma200))
    return price > ma50 and ma50 > ma200


def compute_uptrend_participation(rows: list[dict]) -> UptrendResult:
    """rows: list of dicts with 'price', 'ma50', 'ma200' keys (numeric strings ok).

    Rows with missing/unparseable data are excluded and counted, not folded
    into either direction.
    """
    total = 0
    in_uptrend = 0
    excluded = 0

    for row in rows:
        total += 1
        try:
            result = is_in_uptrend(row["price"], row["ma50"], row["ma200"])
        except (KeyError, ValueError, TypeError, ArithmeticError):
            excluded += 1
            continue
        if result:
            in_uptrend += 1

    counted = total - excluded
    pct = (Decimal(in_uptrend) / Decimal(counted) * 100) if counted > 0 else Decimal("0")
    return UptrendResult(
        total=total,
        in_uptrend=in_uptrend,
        excluded=excluded,
        pct_uptrend=pct.quantize(Decimal("0.1")),
    )


def _self_test() -> None:
    # Classic uptrend: price > 50MA > 200MA
    assert is_in_uptrend(110, 105, 100) is True
    # Price above 50MA but 50MA below 200MA -- not an established uptrend by this definition
    assert is_in_uptrend(106, 105, 110) is False
    # Price below its own 50MA -- clearly not in uptrend
    assert is_in_uptrend(100, 105, 100) is False
    # Exact equality on either leg does not count (strict >)
    assert is_in_uptrend(105, 105, 100) is False

    rows = [
        {"ticker": "AAA", "price": "110", "ma50": "105", "ma200": "100"},  # uptrend
        {"ticker": "BBB", "price": "106", "ma50": "105", "ma200": "110"},  # not
        {"ticker": "CCC", "price": "120", "ma50": "110", "ma200": "100"},  # uptrend
        {"ticker": "DDD", "price": "bad", "ma50": "105", "ma200": "100"},  # excluded
    ]
    result = compute_uptrend_participation(rows)
    assert result.total == 4
    assert result.excluded == 1
    assert result.in_uptrend == 2
    assert result.pct_uptrend == Decimal("66.7")  # 2 of 3 counted rows

    empty = compute_uptrend_participation([])
    assert empty.pct_uptrend == Decimal("0")

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
