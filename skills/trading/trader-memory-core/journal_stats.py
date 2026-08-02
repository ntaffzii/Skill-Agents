#!/usr/bin/env python3
"""journal_stats.py -- compute win rate, average R-multiple, and expectancy from a closed-trade log.

Pure arithmetic over a list of trades the user supplies (e.g. loaded from a
local YAML/CSV journal, see SKILL.md for the schema). No market data, no
dependencies. Not financial advice -- this summarizes past results, it does
not predict future ones.

Run `python3 journal_stats.py` for the self-test.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class TradeStats:
    total_trades: int
    wins: int
    losses: int
    breakeven: int
    win_rate: Decimal
    avg_r_multiple: Decimal
    avg_win_r: Decimal
    avg_loss_r: Decimal
    expectancy_r: Decimal  # expected R-multiple per trade, given this sample's win rate and avg win/loss


def compute_r_multiple(entry, stop, exit_price) -> Decimal:
    """R-multiple: how many multiples of the initial risk (entry-to-stop distance)
    this trade made or lost. R = (exit - entry) / (entry - stop) for a long trade.

    A positive R means a win, negative means a loss, magnitude independent
    of position size -- this is what makes R-multiples comparable across
    trades with different share counts.
    """
    entry = Decimal(str(entry))
    stop = Decimal(str(stop))
    exit_price = Decimal(str(exit_price))
    risk_per_share = entry - stop
    if risk_per_share == 0:
        raise ValueError("entry and stop must differ to compute an R-multiple")
    return ((exit_price - entry) / risk_per_share).quantize(Decimal("0.01"))


def compute_trade_stats(trades: list[dict]) -> TradeStats:
    """trades: list of dicts, each with an 'r_multiple' key (Decimal-like).

    Use compute_r_multiple() first if the journal stores entry/stop/exit
    instead of a precomputed r_multiple.
    """
    r_multiples = [Decimal(str(t["r_multiple"])) for t in trades]
    total = len(r_multiples)

    wins = [r for r in r_multiples if r > 0]
    losses = [r for r in r_multiples if r < 0]
    breakeven = total - len(wins) - len(losses)

    win_rate = (Decimal(len(wins)) / Decimal(total)) if total > 0 else Decimal("0")
    avg_r = (sum(r_multiples) / Decimal(total)) if total > 0 else Decimal("0")
    avg_win_r = (sum(wins) / Decimal(len(wins))) if wins else Decimal("0")
    avg_loss_r = (sum(losses) / Decimal(len(losses))) if losses else Decimal("0")

    # Expectancy: win_rate * avg_win - loss_rate * |avg_loss|, in R-multiples
    loss_rate = (Decimal(len(losses)) / Decimal(total)) if total > 0 else Decimal("0")
    expectancy = (win_rate * avg_win_r) + (loss_rate * avg_loss_r)  # avg_loss_r is already negative

    return TradeStats(
        total_trades=total,
        wins=len(wins),
        losses=len(losses),
        breakeven=breakeven,
        win_rate=(win_rate * 100).quantize(Decimal("0.1")),
        avg_r_multiple=avg_r.quantize(Decimal("0.01")),
        avg_win_r=avg_win_r.quantize(Decimal("0.01")),
        avg_loss_r=avg_loss_r.quantize(Decimal("0.01")),
        expectancy_r=expectancy.quantize(Decimal("0.01")),
    )


def _self_test() -> None:
    # R-multiple: entry 50, stop 48 (risk = 2/share), exit 54 -> +4/2 = +2R
    assert compute_r_multiple(entry=50, stop=48, exit_price=54) == Decimal("2.00")
    # Loss: exit 47 -> -3/2 = -1.5R
    assert compute_r_multiple(entry=50, stop=48, exit_price=47) == Decimal("-1.50")
    # Breakeven at entry -> 0R
    assert compute_r_multiple(entry=50, stop=48, exit_price=50) == Decimal("0.00")

    trades = [
        {"r_multiple": "2.0"},   # win
        {"r_multiple": "-1.0"},  # loss
        {"r_multiple": "1.5"},   # win
        {"r_multiple": "-1.0"},  # loss
        {"r_multiple": "0.0"},   # breakeven
    ]
    stats = compute_trade_stats(trades)
    assert stats.total_trades == 5
    assert stats.wins == 2
    assert stats.losses == 2
    assert stats.breakeven == 1
    assert stats.win_rate == Decimal("40.0")  # 2 of 5
    assert stats.avg_win_r == Decimal("1.75")  # (2.0 + 1.5) / 2
    assert stats.avg_loss_r == Decimal("-1.00")
    # expectancy = 0.4 * 1.75 + 0.4 * (-1.00) = 0.7 - 0.4 = 0.30
    assert stats.expectancy_r == Decimal("0.30")

    empty = compute_trade_stats([])
    assert empty.total_trades == 0
    assert empty.win_rate == Decimal("0")

    # Zero-risk trade rejected, not silently divided by zero
    try:
        compute_r_multiple(entry=50, stop=50, exit_price=52)
        assert False, "expected ValueError"
    except ValueError:
        pass

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
