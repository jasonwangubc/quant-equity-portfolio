"""Regime dashboard package."""

from regime_dashboard.data import generate_synthetic_market_data
from regime_dashboard.regime import detect_regimes
from regime_dashboard.risk import summarize_risk

__all__ = ["generate_synthetic_market_data", "detect_regimes", "summarize_risk"]
