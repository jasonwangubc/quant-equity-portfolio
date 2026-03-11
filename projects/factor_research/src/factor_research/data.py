"""Synthetic data generation and local storage helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd


@dataclass(frozen=True)
class UniverseConfig:
    """Configuration for synthetic equity universe generation."""

    n_assets: int = 250
    n_months: int = 120
    start_date: str = "2015-01-31"
    seed: int = 42


def generate_synthetic_equity_panel(config: UniverseConfig) -> pd.DataFrame:
    """Create a monthly equity panel with features and one-step-ahead returns."""
    rng = np.random.default_rng(config.seed)
    dates = pd.date_range(config.start_date, periods=config.n_months, freq="ME")
    assets = [f"EQ{i:04d}" for i in range(1, config.n_assets + 1)]

    quality = rng.normal(0.0, 1.0, config.n_assets)
    value = rng.normal(0.0, 1.0, config.n_assets)
    market_beta = rng.normal(1.0, 0.2, config.n_assets)

    market_shock = rng.normal(0.005, 0.03, size=config.n_months)
    value_shock = rng.normal(0.001, 0.02, size=config.n_months)
    quality_shock = rng.normal(0.0015, 0.02, size=config.n_months)

    records: list[dict[str, float | str | pd.Timestamp]] = []
    for i, asset in enumerate(assets):
        price = 50.0 * np.exp(rng.normal(0.0, 0.2))
        shares_out = np.exp(rng.normal(18.5, 0.5))
        book_value = max(1.0, price * shares_out * np.exp(-1.5 + 0.4 * value[i]))
        earnings = max(1.0, book_value * np.exp(-2.2 + 0.3 * quality[i]))

        prev_ret = float(rng.normal(0.0, 0.02))
        idio_scale = float(np.clip(rng.normal(0.03, 0.008), 0.01, 0.08))
        for t, date in enumerate(dates):
            idio = rng.normal(0.0, idio_scale)
            style_alpha = 0.0025 * value[i] + 0.0030 * quality[i]
            momentum_alpha = 0.10 * prev_ret
            ret = (
                market_beta[i] * market_shock[t]
                + 0.25 * value[i] * value_shock[t]
                + 0.30 * quality[i] * quality_shock[t]
                + style_alpha
                + momentum_alpha
                + idio
            )
            ret = float(np.clip(ret, -0.35, 0.35))
            prev_ret = ret
            price *= 1.0 + ret
            price = max(price, 1.0)

            book_growth = rng.normal(0.004 + 0.003 * quality[i], 0.01)
            earnings_growth = rng.normal(0.006 + 0.004 * quality[i], 0.015)
            book_value *= 1.0 + book_growth
            earnings *= 1.0 + earnings_growth

            records.append(
                {
                    "date": date,
                    "asset": asset,
                    "price": price,
                    "shares_outstanding": shares_out,
                    "market_cap": price * shares_out,
                    "book_value": book_value,
                    "earnings": earnings,
                    "monthly_return": ret,
                }
            )

    panel = pd.DataFrame.from_records(records).sort_values(["asset", "date"]).reset_index(drop=True)
    panel["forward_return"] = panel.groupby("asset")["monthly_return"].shift(-1)
    panel["log_market_cap"] = np.log(panel["market_cap"].clip(lower=1.0))
    panel["book_to_market"] = panel["book_value"] / panel["market_cap"].clip(lower=1.0)
    panel["earnings_yield"] = panel["earnings"] / panel["market_cap"].clip(lower=1.0)

    return panel.dropna(subset=["forward_return"]).reset_index(drop=True)


def persist_panel_to_duckdb(panel: pd.DataFrame, db_path: str | Path, table_name: str = "equity_panel") -> None:
    """Persist panel data to DuckDB to demonstrate analytics-oriented local storage."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(db_path)) as conn:
        conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM panel")


def load_panel_from_duckdb(db_path: str | Path, table_name: str = "equity_panel") -> pd.DataFrame:
    """Load panel data from DuckDB."""
    with duckdb.connect(str(db_path)) as conn:
        result = conn.execute(f"SELECT * FROM {table_name} ORDER BY asset, date").fetch_df()
    result["date"] = pd.to_datetime(result["date"])
    return result
