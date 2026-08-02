#!/usr/bin/env python3
"""breadth.py -- market breadth scoring from a plain CSV, no API key required.

Breadth measures how many stocks in a universe are participating in a move,
as opposed to a cap-weighted index being carried by a handful of large names.
This module computes the simplest, most common breadth statistic: the
percentage of tickers trading above a given moving average.

Not financial advice. This is a descriptive statistic over data you supply;
it does not fetch live prices, does not predict future returns, and a single
breadth reading is a weak signal in isolation -- see SKILL.md.

Run `python3 breadth.py` for the self-test.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal
from io import StringIO


@dataclass
class BreadthResult:
    total: int
    above: int
    below: int
    excluded: int  # rows with missing/unparseable data, reported not silently dropped
    pct_above: Decimal


def compute_breadth(rows: list[dict], price_field: str = "price", ma_field: str = "ma200") -> BreadthResult:
    """rows: list of dicts with at least `price_field` and `ma_field` keys (numeric strings ok).

    Returns the count and percentage of rows where price > moving average.
    Rows with missing or non-numeric values are excluded and counted, not
    silently treated as "below" -- a data-quality issue should be visible,
    not folded into the score.
    """
    total = 0
    above = 0
    excluded = 0

    for row in rows:
        total += 1
        try:
            price = Decimal(str(row[price_field]))
            ma = Decimal(str(row[ma_field]))
        except (KeyError, ValueError, TypeError, ArithmeticError):
            excluded += 1
            continue
        if price > ma:
            above += 1

    counted = total - excluded
    pct_above = (Decimal(above) / Decimal(counted) * 100) if counted > 0 else Decimal("0")
    return BreadthResult(
        total=total,
        above=above,
        below=counted - above,
        excluded=excluded,
        pct_above=pct_above.quantize(Decimal("0.1")),
    )


def compute_breadth_from_csv(csv_text: str, price_field: str = "price", ma_field: str = "ma200") -> BreadthResult:
    """Convenience wrapper: parse CSV text (header row required) and score it."""
    reader = csv.DictReader(StringIO(csv_text))
    return compute_breadth(list(reader), price_field=price_field, ma_field=ma_field)


def classify_breadth(pct_above: Decimal) -> str:
    """Rough, configurable bands for talking about a breadth reading in plain language.

    These thresholds are a starting heuristic, not a calibrated model --
    tune them against your own universe's history before relying on them.
    """
    if pct_above >= 70:
        return "broad participation"
    if pct_above >= 50:
        return "moderate participation"
    if pct_above >= 30:
        return "narrow participation"
    return "weak participation"


def _self_test() -> None:
    rows = [
        {"ticker": "AAA", "price": "105", "ma200": "100"},   # above
        {"ticker": "BBB", "price": "95", "ma200": "100"},    # below
        {"ticker": "CCC", "price": "110", "ma200": "100"},   # above
        {"ticker": "DDD", "price": "100", "ma200": "100"},   # equal -> below (strict >)
        {"ticker": "EEE", "price": "n/a", "ma200": "100"},   # excluded, bad data
    ]
    result = compute_breadth(rows)
    assert result.total == 5
    assert result.excluded == 1
    assert result.above == 2
    assert result.below == 2
    assert result.pct_above == Decimal("50.0")  # 2 of 4 counted rows

    assert classify_breadth(Decimal("75")) == "broad participation"
    assert classify_breadth(Decimal("55")) == "moderate participation"
    assert classify_breadth(Decimal("35")) == "narrow participation"
    assert classify_breadth(Decimal("10")) == "weak participation"

    csv_text = "ticker,price,ma200\nAAA,105,100\nBBB,95,100\n"
    csv_result = compute_breadth_from_csv(csv_text)
    assert csv_result.total == 2
    assert csv_result.pct_above == Decimal("50.0")

    # Empty input doesn't divide by zero
    empty = compute_breadth([])
    assert empty.total == 0
    assert empty.pct_above == Decimal("0")

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
