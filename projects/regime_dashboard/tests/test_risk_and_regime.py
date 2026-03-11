import numpy as np
import pandas as pd

from regime_dashboard.data import generate_synthetic_market_data
from regime_dashboard.regime import detect_regimes
from regime_dashboard.risk import summarize_risk, var_cvar


def test_var_cvar_are_ordered() -> None:
    rng = np.random.default_rng(7)
    returns = pd.Series(rng.normal(0.0002, 0.01, size=1000))
    var95, cvar95 = var_cvar(returns, alpha=0.95)
    assert var95 > 0
    assert cvar95 >= var95


def test_regime_detection_returns_valid_labels() -> None:
    df = generate_synthetic_market_data(n_assets=30, n_days=600, seed=17)
    regimes = detect_regimes(df["benchmark"], n_regimes=3, seed=17)
    assert not regimes.empty
    assert regimes["regime"].between(0, 2).all()


def test_risk_summary_keys_exist() -> None:
    df = generate_synthetic_market_data(n_assets=30, n_days=600, seed=17)
    summary = summarize_risk(df["strategy"])
    assert {"annualized_return", "annualized_volatility", "sharpe_ratio", "max_drawdown"}.issubset(
        summary.keys()
    )
