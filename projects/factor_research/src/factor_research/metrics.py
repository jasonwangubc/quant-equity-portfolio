"""Research metrics for portfolio managers and quant researchers."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _max_drawdown(equity_curve: pd.Series) -> float:
    running_peak = equity_curve.cummax()
    drawdown = equity_curve / running_peak - 1.0
    return float(drawdown.min())


def compute_information_coefficient(data: pd.DataFrame, signal_col: str = "composite_signal") -> pd.DataFrame:
    """Compute monthly rank IC between signal and next-period return."""
    ic = (
        data.groupby("date")
        .apply(
            lambda x: x[signal_col].corr(x["forward_return"], method="spearman"),
            include_groups=False,
        )
        .rename("rank_ic")
        .reset_index()
    )
    return ic.dropna()


def summarize_performance(backtest_history: pd.DataFrame, ic_frame: pd.DataFrame) -> dict[str, float]:
    """Generate concise summary statistics."""
    if backtest_history.empty:
        raise ValueError("Backtest history is empty.")

    rets = backtest_history["net_return"]
    ann_return = float((1.0 + rets).prod() ** (12 / len(rets)) - 1.0)
    ann_vol = float(rets.std(ddof=0) * np.sqrt(12))
    sharpe = ann_return / ann_vol if ann_vol > 0 else np.nan
    hit_rate = float((rets > 0).mean())

    summary = {
        "annualized_return": ann_return,
        "annualized_volatility": ann_vol,
        "sharpe_ratio": float(sharpe),
        "max_drawdown": _max_drawdown(backtest_history["equity_curve"]),
        "hit_rate": hit_rate,
        "average_turnover": float(backtest_history["turnover"].mean()),
        "average_rank_ic": float(ic_frame["rank_ic"].mean()),
        "ic_information_ratio": float(
            ic_frame["rank_ic"].mean() / ic_frame["rank_ic"].std(ddof=0)
            if ic_frame["rank_ic"].std(ddof=0) > 0
            else np.nan
        ),
    }
    return summary
