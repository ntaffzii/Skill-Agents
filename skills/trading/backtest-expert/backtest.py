#!/usr/bin/env python3
"""backtest.py -- long-only backtest engine + a simple moving-average-crossover
signal generator, both pure stdlib (Decimal), no external data source.

Not financial advice. A backtest shows how a rule would have performed on one
specific historical sample -- it does not predict future performance, and it
is vulnerable to overfitting if the rule was tuned using the same data it is
being evaluated on. See SKILL.md "Known limitations".

Run `python3 backtest.py` for the self-test.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Trade:
    entry_date: str
    exit_date: str
    entry_price: Decimal
    exit_price: Decimal
    return_pct: Decimal


@dataclass
class BacktestResult:
    trades: list[Trade]
    total_trades: int
    win_rate: Decimal
    avg_return_pct: Decimal
    total_return_pct: Decimal
    max_drawdown_pct: Decimal
    profit_factor: Decimal | None  # gross profit / gross loss; None if no losing trades to divide by
    open_position_at_end: bool  # True if a "buy" was entered but never closed by a "sell" -- excluded from trades


def run_backtest(bars: list[dict]) -> BacktestResult:
    """Simulate a long-only, one-position-at-a-time strategy.

    bars: chronological list of {"date": str, "price": number, "signal": "buy"|"sell"|"hold"}.
    Enters on "buy" only while flat; exits on "sell" only while in a position.
    A "buy" signal while already in a position, or a "sell" while flat, is a no-op
    (does not open a second position or close a nonexistent one).
    """
    trades: list[Trade] = []
    # equity_curve is marked to market on EVERY bar, not just at trade close -- a
    # position held between "buy" and "sell" can dip well below its final exit
    # value along the way (real drawdown a trader lived through), and bars while
    # holding already carry the price data needed to see that (e.g. a "hold" bar's
    # price). Sampling equity only at trade boundaries would silently miss any
    # intra-trade dip that recovered by the time the position closed.
    equity_curve = [Decimal("1")]  # normalized to start at 1.0
    realized_equity = Decimal("1")  # equity level as of the last closed trade (or start, if none yet)
    in_position = False
    entry_price: Decimal | None = None
    entry_date: str | None = None

    for bar in bars:
        price = Decimal(str(bar["price"]))
        signal = bar.get("signal", "hold")

        if not in_position and signal == "buy":
            in_position = True
            entry_price = price
            entry_date = bar["date"]
            bar_equity = realized_equity  # just entered -- no price move yet this bar
        elif in_position:
            unrealized_pct = (price - entry_price) / entry_price * 100
            bar_equity = realized_equity * (1 + unrealized_pct / 100)
            if signal == "sell":
                trades.append(Trade(entry_date, bar["date"], entry_price, price, unrealized_pct))
                realized_equity = bar_equity
                in_position = False
                entry_price = None
                entry_date = None
        else:
            bar_equity = realized_equity  # flat, nothing to mark

        equity_curve.append(bar_equity)

    total = len(trades)
    wins = [t for t in trades if t.return_pct > 0]
    losses = [t for t in trades if t.return_pct < 0]

    win_rate = (Decimal(len(wins)) / Decimal(total) * 100) if total else Decimal("0")
    avg_return = (sum((t.return_pct for t in trades), Decimal("0")) / Decimal(total)) if total else Decimal("0")
    total_return = (equity_curve[-1] - 1) * 100

    peak = equity_curve[0]
    max_dd = Decimal("0")
    for eq in equity_curve:
        if eq > peak:
            peak = eq
        drawdown = (peak - eq) / peak * 100
        if drawdown > max_dd:
            max_dd = drawdown

    gross_profit = sum((t.return_pct for t in wins), Decimal("0"))
    gross_loss = abs(sum((t.return_pct for t in losses), Decimal("0")))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else None

    return BacktestResult(
        trades=trades,
        total_trades=total,
        win_rate=win_rate.quantize(Decimal("0.1")),
        avg_return_pct=avg_return.quantize(Decimal("0.01")),
        total_return_pct=total_return.quantize(Decimal("0.01")),
        max_drawdown_pct=max_dd.quantize(Decimal("0.01")),
        profit_factor=profit_factor.quantize(Decimal("0.01")) if profit_factor is not None else None,
        open_position_at_end=in_position,
    )


def generate_ma_crossover_signals(prices: list[dict], fast_period: int, slow_period: int) -> list[dict]:
    """Generate buy/sell/hold signals from a simple moving-average crossover.

    prices: chronological list of {"date": str, "price": number}.
    fast_period/slow_period: number of trailing closes (inclusive of the current
    one) each moving average averages over. "buy" fires the first bar the fast
    MA is above the slow MA after not having been (state transitions into
    "above"); "sell" fires the first bar it's below after not having been.
    Bars without enough history for both MAs get "hold". No lookahead: each
    bar's MAs use only that bar and earlier ones.
    """
    if fast_period < 1 or slow_period < 1:
        raise ValueError("fast_period and slow_period must be >= 1")

    closes = [Decimal(str(p["price"])) for p in prices]
    signals: list[dict] = []
    previous_state: str | None = None  # "above" | "below" | "equal" | None (no prior valid comparison)

    for i, p in enumerate(prices):
        if i + 1 < slow_period or i + 1 < fast_period:
            signals.append({**p, "signal": "hold"})
            continue

        fast_ma = sum(closes[i + 1 - fast_period : i + 1]) / Decimal(fast_period)
        slow_ma = sum(closes[i + 1 - slow_period : i + 1]) / Decimal(slow_period)

        if fast_ma > slow_ma:
            state = "above"
        elif fast_ma < slow_ma:
            state = "below"
        else:
            state = "equal"

        if state == "above" and previous_state != "above":
            signal = "buy"
        elif state == "below" and previous_state != "below":
            signal = "sell"
        else:
            signal = "hold"

        signals.append({**p, "signal": signal})
        previous_state = state

    return signals


def _self_test() -> None:
    # --- run_backtest: hand-verified numbers ---
    # Trade 1: enter 100, exit 110 -> +10.00%. Trade 2: enter 110, exit 99 -> -10.00%.
    bars = [
        {"date": "d1", "price": 100, "signal": "hold"},
        {"date": "d2", "price": 100, "signal": "buy"},
        {"date": "d3", "price": 110, "signal": "hold"},
        {"date": "d4", "price": 110, "signal": "sell"},
        {"date": "d5", "price": 110, "signal": "buy"},
        {"date": "d6", "price": 99, "signal": "sell"},
    ]
    result = run_backtest(bars)
    assert result.total_trades == 2
    assert result.trades[0].return_pct == Decimal("10.00")
    assert result.trades[1].return_pct == Decimal("-10.00")
    assert result.win_rate == Decimal("50.0")
    assert result.avg_return_pct == Decimal("0.00")
    # equity: 1 -> 1.10 (after trade 1) -> 0.99 (after trade 2) -> total return -1.00%
    assert result.total_return_pct == Decimal("-1.00")
    # peak 1.10, trough 0.99 -> (1.10-0.99)/1.10 * 100 = 10.00%
    assert result.max_drawdown_pct == Decimal("10.00")
    # gross_profit=10, gross_loss=10 -> profit_factor 1.00
    assert result.profit_factor == Decimal("1.00")
    assert result.open_position_at_end is False

    # Regression: max_drawdown_pct must reflect intra-trade drawdown, not just the
    # entry-to-exit trade return. Enter at 100, dip to 50 intraday (a real ~50%
    # unrealized drawdown), then recover and exit at 110 (+10% trade). A version
    # that only samples equity at trade close would report 0% drawdown here --
    # confirmed as a real bug before this test was added.
    intratrade_dip_bars = [
        {"date": "d1", "price": 100, "signal": "buy"},
        {"date": "d2", "price": 50, "signal": "hold"},
        {"date": "d3", "price": 110, "signal": "sell"},
    ]
    dip_result = run_backtest(intratrade_dip_bars)
    assert dip_result.total_trades == 1
    assert dip_result.trades[0].return_pct == Decimal("10.00")  # the trade itself still nets +10%
    assert dip_result.max_drawdown_pct == Decimal("50.00")  # but drawdown must show the real ~50% dip

    # A trailing "buy" with no matching "sell" is an open position, not a completed trade
    bars_with_open_tail = bars + [{"date": "d7", "price": 105, "signal": "buy"}]
    result2 = run_backtest(bars_with_open_tail)
    assert result2.total_trades == 2  # still 2, the open buy is not counted
    assert result2.open_position_at_end is True

    # No trades at all -> zeros, not a crash, profit_factor is None (no losses to divide by)
    empty_result = run_backtest([{"date": "d1", "price": 100, "signal": "hold"}])
    assert empty_result.total_trades == 0
    assert empty_result.win_rate == Decimal("0")
    assert empty_result.profit_factor is None

    # A "sell" while flat, or a "buy" while already in a position, is a no-op
    noop_bars = [
        {"date": "d1", "price": 100, "signal": "sell"},  # no-op, not in a position
        {"date": "d2", "price": 100, "signal": "buy"},
        {"date": "d3", "price": 105, "signal": "buy"},  # no-op, already in a position
        {"date": "d4", "price": 110, "signal": "sell"},
    ]
    noop_result = run_backtest(noop_bars)
    assert noop_result.total_trades == 1
    assert noop_result.trades[0].entry_price == Decimal("100")  # not re-entered at 105

    # --- generate_ma_crossover_signals: hand-verified crossover sequence ---
    # prices [100,100,110,110,90,90], fast_period=1 (= the price itself), slow_period=2
    prices = [
        {"date": "d1", "price": 100},
        {"date": "d2", "price": 100},
        {"date": "d3", "price": 110},
        {"date": "d4", "price": 110},
        {"date": "d5", "price": 90},
        {"date": "d6", "price": 90},
    ]
    signals = generate_ma_crossover_signals(prices, fast_period=1, slow_period=2)
    assert [s["signal"] for s in signals] == ["hold", "hold", "buy", "hold", "sell", "hold"]

    # Invalid periods rejected, not silently mishandled
    try:
        generate_ma_crossover_signals(prices, fast_period=0, slow_period=2)
        assert False, "expected ValueError"
    except ValueError:
        pass

    # End-to-end: feed generated signals straight into run_backtest
    e2e_bars = generate_ma_crossover_signals(
        [{"date": f"d{i}", "price": p} for i, p in enumerate(
            [100, 100, 110, 110, 90, 90, 120, 120]
        )],
        fast_period=1,
        slow_period=2,
    )
    e2e_result = run_backtest(e2e_bars)
    assert e2e_result.total_trades >= 1  # at least the buy-at-110/sell-at-90 pair completes

    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
