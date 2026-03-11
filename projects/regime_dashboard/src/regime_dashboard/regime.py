"""Regime detection helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture


def detect_regimes(
    benchmark_returns: pd.Series,
    n_regimes: int = 3,
    lookback: int = 20,
    seed: int = 11,
) -> pd.DataFrame:
    """Cluster market conditions using rolling return and volatility features."""
    series = benchmark_returns.astype(float)
    frame = pd.DataFrame(
        {
            "return_1d": series,
            "return_20d": series.rolling(lookback).mean(),
            "vol_20d": series.rolling(lookback).std(),
        }
    ).dropna()

    model = GaussianMixture(n_components=n_regimes, random_state=seed, covariance_type="full")
    model.fit(frame.values)
    labels = model.predict(frame.values)
    probs = model.predict_proba(frame.values)

    output = frame.copy()
    output["regime"] = labels
    output["confidence"] = probs.max(axis=1)

    # Stable ordering: regime 0 = lowest vol.
    vol_by_regime = output.groupby("regime")["vol_20d"].mean().sort_values()
    mapping = {old: new for new, old in enumerate(vol_by_regime.index)}
    output["regime"] = output["regime"].map(mapping).astype(int)
    return output.reset_index().rename(columns={"index": "date"})
