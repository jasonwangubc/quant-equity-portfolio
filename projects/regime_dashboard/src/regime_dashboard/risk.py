"""Risk metric calculations for dashboard analytics."""

from __future__ import annotations

import numpy as np
import pandas as pd


def rolling_volatility(returns: pd.Series, window: int = 63) -> pd.Series:
    return returns.rolling(window).std() * np.sqrt(252)


def drawdown_series(returns: pd.Series) -> pd.Series:
    equity = (1.0 + returns).cumprod()
    peak = equity.cummax()
    return equity / peak - 1.0


def var_cvar(returns: pd.Series, alpha: float = 0.95) -> tuple[float, float]:
    losses = -returns.dropna()
    if losses.empty:
        return np.nan, np.nan
    var = float(np.quantile(losses, alpha))
    cvar = float(losses[losses >= var].mean())
    return var, cvar


def stress_scenario_impact(returns: pd.Series, shock: float) -> float:
    """Approximate one-day PnL impact under an exogenous shock."""
    beta_proxy = float(np.clip(returns.corr(returns.shift(1)), -1.0, 1.0))
    return beta_proxy * shock


def summarize_risk(returns: pd.Series) -> dict[str, float]:
    dd = drawdown_series(returns)
    var95, cvar95 = var_cvar(returns, alpha=0.95)
    ann_ret = float((1.0 + returns).prod() ** (252 / len(returns)) - 1.0)
    ann_vol = float(returns.std(ddof=0) * np.sqrt(252))
    sharpe = ann_ret / ann_vol if ann_vol > 0 else np.nan
    return {
        "annualized_return": ann_ret,
        "annualized_volatility": ann_vol,
        "sharpe_ratio": float(sharpe),
        "max_drawdown": float(dd.min()),
        "var_95": var95,
        "cvar_95": cvar95,
        "shock_minus_5pct": stress_scenario_impact(returns, shock=-0.05),
    }
