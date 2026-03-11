"""Run concise outputs from all portfolio projects."""

from __future__ import annotations

from pprint import pprint

from factor_research.pipeline import run_research_pipeline
from optimizer_api.models import MeanVarianceRequest, RiskParityRequest
from optimizer_api.optimize import solve_mean_variance, solve_risk_parity
from regime_dashboard.data import generate_synthetic_market_data
from regime_dashboard.risk import summarize_risk


def run_factor_research() -> None:
    result = run_research_pipeline(db_path="data/showcase_factor_research.duckdb")
    print("\n[1/3] Factor Research Lab")
    for k, v in result.summary.items():
        print(f"{k:>24}: {v: .4f}")


def run_optimizer() -> None:
    covariance = [
        [0.040, 0.012, 0.010, 0.013],
        [0.012, 0.030, 0.011, 0.012],
        [0.010, 0.011, 0.025, 0.009],
        [0.013, 0.012, 0.009, 0.035],
    ]
    mv = MeanVarianceRequest(
        expected_returns=[0.10, 0.08, 0.06, 0.07],
        covariance=covariance,
        risk_aversion=5.0,
        min_weight=0.0,
        max_weight=0.5,
        turnover_penalty=0.05,
        current_weights=[0.25, 0.25, 0.25, 0.25],
    )
    rp = RiskParityRequest(covariance=covariance)
    print("\n[2/3] Portfolio Optimizer API Engines")
    print("Mean-Variance:")
    pprint(solve_mean_variance(mv))
    print("Risk-Parity:")
    pprint(solve_risk_parity(rp))


def run_risk_dashboard_backend() -> None:
    df = generate_synthetic_market_data(n_assets=50, n_days=900, seed=17)
    summary = summarize_risk(df["strategy"])
    print("\n[3/3] Regime & Risk Dashboard Analytics")
    for k, v in summary.items():
        print(f"{k:>24}: {v: .4f}")


if __name__ == "__main__":
    run_factor_research()
    run_optimizer()
    run_risk_dashboard_backend()
