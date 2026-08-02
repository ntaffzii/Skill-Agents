#!/usr/bin/env python3
"""size.py -- risk-based position sizing (fixed-fractional and ATR-based).

Pure arithmetic on numbers you supply -- no market data, no dependencies.
Not financial advice: this calculates how many shares fit a chosen risk
budget, it does not tell you whether to take the trade.

Run `python3 size.py` for the self-test.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class SizeResult:
    shares: int
    dollar_risk_per_share: Decimal
    total_risk_amount: Decimal
    actual_risk_amount: Decimal  # shares * dollar_risk_per_share (<= total_risk_amount due to rounding down)
    position_value: Decimal


def fixed_fractional_size(
    account_equity,
    risk_pct,
    entry_price,
    stop_price,
) -> SizeResult:
    """Risk a fixed percentage of account equity on this trade.

    risk_pct: e.g. Decimal("0.01") for 1%. entry_price must differ from
    stop_price (a zero-distance stop can't be sized). Shares are floored
    (rounded down) so actual dollar risk never exceeds the budget.
    """
    account_equity = Decimal(str(account_equity))
    risk_pct = Decimal(str(risk_pct))
    entry_price = Decimal(str(entry_price))
    stop_price = Decimal(str(stop_price))

    dollar_risk_per_share = abs(entry_price - stop_price)
    if dollar_risk_per_share == 0:
        raise ValueError("entry_price and stop_price must differ")

    total_risk_amount = account_equity * risk_pct
    shares = int(total_risk_amount / dollar_risk_per_share)  # floor
    actual_risk_amount = Decimal(shares) * dollar_risk_per_share
    position_value = Decimal(shares) * entry_price

    return SizeResult(
        shares=shares,
        dollar_risk_per_share=dollar_risk_per_share,
        total_risk_amount=total_risk_amount,
        actual_risk_amount=actual_risk_amount,
        position_value=position_value,
    )


def atr_based_stop(entry_price, atr, multiplier=2.0) -> Decimal:
    """Compute a stop price a chosen multiple of ATR below entry (long trade).

    ATR-based stops scale the stop distance to the security's own recent
    volatility instead of a fixed percentage -- a common alternative to a
    flat percentage stop.
    """
    entry_price = Decimal(str(entry_price))
    atr = Decimal(str(atr))
    multiplier = Decimal(str(multiplier))
    return entry_price - (atr * multiplier)


def atr_based_size(account_equity, risk_pct, entry_price, atr, multiplier=2.0) -> SizeResult:
    """Convenience wrapper: derive the stop from ATR, then size with the same risk budget as fixed_fractional_size."""
    stop_price = atr_based_stop(entry_price, atr, multiplier)
    return fixed_fractional_size(account_equity, risk_pct, entry_price, stop_price)


def kelly_fraction(win_rate, avg_win, avg_loss) -> Decimal:
    """Kelly criterion fraction of capital to risk, from historical win/loss stats.

    win_rate: 0-1. avg_win/avg_loss: average $ or R-multiple magnitudes (both positive).
    Returns the theoretical optimal fraction -- in practice, traders commonly
    use a fraction of this (e.g. "half Kelly") because the formula is highly
    sensitive to estimation error in win_rate/avg_win/avg_loss. This function
    does not apply that discount for you; treat the raw result as an upper
    bound, not a recommendation.
    """
    win_rate = Decimal(str(win_rate))
    avg_win = Decimal(str(avg_win))
    avg_loss = Decimal(str(avg_loss))
    if avg_loss == 0:
        raise ValueError("avg_loss must be nonzero")
    b = avg_win / avg_loss
    fraction = win_rate - ((1 - win_rate) / b)
    return fraction


def _self_test() -> None:
    # $100,000 account, risk 1%, entry 50, stop 48 -> $2/share risk, $1000 budget -> 500 shares
    r = fixed_fractional_size(100_000, Decimal("0.01"), 50, 48)
    assert r.shares == 500
    assert r.dollar_risk_per_share == Decimal("2")
    assert r.total_risk_amount == Decimal("1000")
    assert r.actual_risk_amount == Decimal("1000")
    assert r.position_value == Decimal("25000")

    # Rounding down: budget doesn't divide evenly
    r2 = fixed_fractional_size(10_000, Decimal("0.01"), 33, 30)  # $100 budget / $3 risk = 33.33 -> 33 shares
    assert r2.shares == 33
    assert r2.actual_risk_amount == Decimal("99")  # <= budget, never exceeds it

    # Zero-distance stop is rejected, not silently divided by zero
    try:
        fixed_fractional_size(10_000, Decimal("0.01"), 50, 50)
        assert False, "expected ValueError"
    except ValueError:
        pass

    # ATR-based stop and sizing
    stop = atr_based_stop(entry_price=100, atr=5, multiplier=2)
    assert stop == Decimal("90")
    r3 = atr_based_size(100_000, Decimal("0.01"), entry_price=100, atr=5, multiplier=2)
    assert r3.dollar_risk_per_share == Decimal("10")  # 2x ATR of 5
    assert r3.shares == 100  # $1000 budget / $10 risk

    # Kelly fraction: 55% win rate, 1.5:1 avg win/loss
    k = kelly_fraction(win_rate=Decimal("0.55"), avg_win=Decimal("150"), avg_loss=Decimal("100"))
    # b = 1.5, f = 0.55 - 0.45/1.5 = 0.55 - 0.3 = 0.25
    assert k == Decimal("0.25")

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
