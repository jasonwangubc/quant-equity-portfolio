import numpy as np

from factor_research.data import UniverseConfig, generate_synthetic_equity_panel
from factor_research.factors import build_factor_scores
from factor_research.pipeline import run_research_pipeline


def test_factor_scores_have_expected_columns() -> None:
    panel = generate_synthetic_equity_panel(UniverseConfig(n_assets=60, n_months=36, seed=1))
    factor_data = build_factor_scores(panel)

    required_cols = {
        "value_factor_z",
        "momentum_12_1_z",
        "quality_factor_z",
        "low_vol_factor_z",
        "composite_signal",
        "forward_return",
    }
    assert required_cols.issubset(set(factor_data.columns))
    assert not factor_data.empty


def test_research_pipeline_generates_stable_summary() -> None:
    result = run_research_pipeline(db_path="data/test_factor_research.duckdb")
    assert result.backtest.history["net_return"].notna().all()
    assert np.isfinite(result.summary["annualized_return"])
    assert np.isfinite(result.summary["average_rank_ic"])
