"""Synthetic market and strategy return generation."""

from __future__ import annotations

import numpy as np
import pandas as pd


def generate_synthetic_market_data(
    n_assets: int = 80,
    n_days: int = 1250,
    start_date: str = "2020-01-01",
    seed: int = 11,
) -> pd.DataFrame:
    """Create a synthetic daily return panel with latent market regimes."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start_date, periods=n_days)

    # Two-state process: calm and stressed markets.
    transition = np.array([[0.97, 0.03], [0.15, 0.85]])
    state = 0
    states = []
    for _ in range(n_days):
        states.append(state)
        state = int(rng.choice([0, 1], p=transition[state]))

    states_array = np.array(states)
    market_mean = np.where(states_array == 0, 0.00045, -0.0009)
    market_vol = np.where(states_array == 0, 0.008, 0.022)
    market_returns = rng.normal(market_mean, market_vol)

    rows: dict[str, np.ndarray] = {}
    for i in range(n_assets):
        beta = rng.normal(1.0, 0.2)
        alpha = rng.normal(0.00005, 0.0002)
        idio_vol = rng.uniform(0.006, 0.02)
        idio = rng.normal(0.0, idio_vol, n_days)
        rows[f"asset_{i+1:03d}"] = alpha + beta * market_returns + idio

    df = pd.DataFrame(rows, index=dates)
    df.index.name = "date"
    df["benchmark"] = market_returns
    df["strategy"] = df.drop(columns=["benchmark"]).mean(axis=1)
    df["simulated_state"] = states_array
    return df.reset_index()
