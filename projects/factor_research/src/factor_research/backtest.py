"""Long-short backtesting engine with turnover-aware costs."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class BacktestResult:
    """Container for backtest time series."""

    history: pd.DataFrame
    weights: dict[pd.Timestamp, pd.Series]


def _build_weights(cross_section: pd.DataFrame, signal_col: str, long_q: float, short_q: float) -> pd.Series:
    ranked = cross_section.sort_values(signal_col)
    n_assets = len(ranked)
    n_short = max(1, int(np.floor(n_assets * short_q)))
    n_long = max(1, int(np.floor(n_assets * long_q)))

    short_assets = ranked.head(n_short)["asset"].tolist()
    long_assets = ranked.tail(n_long)["asset"].tolist()

    weights = pd.Series(0.0, index=cross_section["asset"].values)
    weights.loc[long_assets] = 0.5 / n_long
    weights.loc[short_assets] = -0.5 / n_short
    return weights


def run_long_short_backtest(
    factor_data: pd.DataFrame,
    signal_col: str = "composite_signal",
    long_q: float = 0.15,
    short_q: float = 0.15,
    transaction_cost_bps: float = 10.0,
) -> BacktestResult:
    """Run monthly long-short strategy and account for turnover costs."""
    grouped = factor_data.groupby("date", sort=True)
    prior_weights = pd.Series(dtype=float)
    history_rows: list[dict[str, float | pd.Timestamp]] = []
    all_weights: dict[pd.Timestamp, pd.Series] = {}

    for date, cross_section in grouped:
        data = cross_section[["asset", signal_col, "forward_return"]].dropna()
        if len(data) < 20:
            continue

        weights = _build_weights(data, signal_col=signal_col, long_q=long_q, short_q=short_q)
        aligned_prev = prior_weights.reindex(weights.index).fillna(0.0)
        turnover = float((weights - aligned_prev).abs().sum())
        gross_return = float((weights * data.set_index("asset")["forward_return"]).sum())
        net_return = gross_return - (transaction_cost_bps / 10_000.0) * turnover

        history_rows.append(
            {
                "date": date,
                "gross_return": gross_return,
                "net_return": net_return,
                "turnover": turnover,
                "long_count": int((weights > 0).sum()),
                "short_count": int((weights < 0).sum()),
            }
        )
        all_weights[pd.Timestamp(date)] = weights
        prior_weights = weights

    history = pd.DataFrame(history_rows).sort_values("date").reset_index(drop=True)
    history["equity_curve"] = (1.0 + history["net_return"]).cumprod()
    return BacktestResult(history=history, weights=all_weights)
