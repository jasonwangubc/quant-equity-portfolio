"""End-to-end pipeline for factor research workflow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from factor_research.backtest import BacktestResult, run_long_short_backtest
from factor_research.data import (
    UniverseConfig,
    generate_synthetic_equity_panel,
    persist_panel_to_duckdb,
)
from factor_research.factors import build_factor_scores
from factor_research.metrics import compute_information_coefficient, summarize_performance


@dataclass
class ResearchOutput:
    """Main output artifacts from the pipeline."""

    panel: pd.DataFrame
    factor_data: pd.DataFrame
    backtest: BacktestResult
    information_coefficient: pd.DataFrame
    summary: dict[str, float]


def run_research_pipeline(db_path: str | Path = "data/factor_research.duckdb") -> ResearchOutput:
    """Run synthetic data creation, signal construction, backtest, and reporting."""
    panel = generate_synthetic_equity_panel(UniverseConfig())
    persist_panel_to_duckdb(panel, db_path=db_path)

    factor_data = build_factor_scores(panel)
    backtest = run_long_short_backtest(factor_data)
    ic_frame = compute_information_coefficient(factor_data)
    summary = summarize_performance(backtest.history, ic_frame)

    return ResearchOutput(
        panel=panel,
        factor_data=factor_data,
        backtest=backtest,
        information_coefficient=ic_frame,
        summary=summary,
    )
