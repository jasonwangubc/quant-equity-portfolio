"""Factor construction and normalization."""

from __future__ import annotations

import numpy as np
import pandas as pd


def _cross_sectional_zscore(series: pd.Series) -> pd.Series:
    std = series.std(ddof=0)
    if std == 0 or np.isnan(std):
        return pd.Series(0.0, index=series.index)
    return (series - series.mean()) / std


def build_factor_scores(panel: pd.DataFrame) -> pd.DataFrame:
    """Build standardized factors and a composite signal."""
    df = panel.sort_values(["asset", "date"]).copy()

    df["momentum_12_1"] = (
        df.groupby("asset")["monthly_return"]
        .rolling(window=12, min_periods=6)
        .apply(lambda x: np.prod(1.0 + x[:-1]) - 1.0 if len(x) > 1 else np.nan, raw=True)
        .reset_index(level=0, drop=True)
    )
    df["volatility_12m"] = (
        df.groupby("asset")["monthly_return"]
        .rolling(window=12, min_periods=6)
        .std()
        .reset_index(level=0, drop=True)
    )
    df["value_factor"] = np.log(df["book_to_market"].clip(lower=1e-6))
    df["quality_factor"] = np.log(df["earnings_yield"].clip(lower=1e-6))
    df["low_vol_factor"] = -df["volatility_12m"]

    factor_cols = ["value_factor", "momentum_12_1", "quality_factor", "low_vol_factor"]
    for col in factor_cols:
        z_col = f"{col}_z"
        df[z_col] = df.groupby("date")[col].transform(_cross_sectional_zscore)

    z_cols = [f"{col}_z" for col in factor_cols]
    df["composite_signal"] = df[z_cols].mean(axis=1)
    return df.dropna(subset=["composite_signal", "forward_return"]).reset_index(drop=True)
