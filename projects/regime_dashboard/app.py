"""Streamlit app for market regime and risk monitoring."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from regime_dashboard.data import generate_synthetic_market_data
from regime_dashboard.regime import detect_regimes
from regime_dashboard.risk import drawdown_series, rolling_volatility, summarize_risk

st.set_page_config(page_title="Regime & Risk Dashboard", layout="wide")
st.title("Quant Strategy Regime & Risk Dashboard")
st.caption("Synthetic data demo for portfolio monitoring workflows.")

with st.sidebar:
    st.header("Simulation Controls")
    n_assets = st.slider("Number of assets", min_value=20, max_value=200, value=80, step=10)
    n_days = st.slider("Number of trading days", min_value=500, max_value=2500, value=1250, step=50)
    n_regimes = st.slider("Detected regimes", min_value=2, max_value=5, value=3, step=1)
    seed = st.number_input("Random seed", min_value=1, max_value=10000, value=11)

df = generate_synthetic_market_data(n_assets=n_assets, n_days=n_days, seed=int(seed))
df["date"] = pd.to_datetime(df["date"])
regimes = detect_regimes(df["benchmark"], n_regimes=n_regimes, seed=int(seed))
risk_summary = summarize_risk(df["strategy"])

metric_cols = st.columns(6)
metric_cols[0].metric("Ann Return", f"{risk_summary['annualized_return']:.2%}")
metric_cols[1].metric("Ann Vol", f"{risk_summary['annualized_volatility']:.2%}")
metric_cols[2].metric("Sharpe", f"{risk_summary['sharpe_ratio']:.2f}")
metric_cols[3].metric("Max Drawdown", f"{risk_summary['max_drawdown']:.2%}")
metric_cols[4].metric("VaR 95%", f"{risk_summary['var_95']:.2%}")
metric_cols[5].metric("CVaR 95%", f"{risk_summary['cvar_95']:.2%}")

left, right = st.columns(2)

with left:
    cumulative = (1.0 + df[["benchmark", "strategy"]]).cumprod()
    cumulative["date"] = df["date"]
    fig = px.line(
        cumulative,
        x="date",
        y=["benchmark", "strategy"],
        title="Cumulative Performance",
        labels={"value": "Growth of $1", "variable": "Series"},
    )
    st.plotly_chart(fig, use_container_width=True)

    vol_df = pd.DataFrame(
        {
            "date": df["date"],
            "strategy_vol_63d": rolling_volatility(df["strategy"], window=63),
        }
    ).dropna()
    fig_vol = px.line(vol_df, x="date", y="strategy_vol_63d", title="Rolling 63D Annualized Volatility")
    st.plotly_chart(fig_vol, use_container_width=True)

with right:
    dd = pd.DataFrame({"date": df["date"], "drawdown": drawdown_series(df["strategy"])})
    fig_dd = px.area(dd, x="date", y="drawdown", title="Strategy Drawdown")
    st.plotly_chart(fig_dd, use_container_width=True)

    merged = regimes.merge(df[["date", "benchmark"]], on="date", how="left")
    fig_regime = px.scatter(
        merged,
        x="date",
        y="benchmark",
        color=merged["regime"].astype(str),
        opacity=0.7,
        title="Detected Market Regimes on Benchmark Returns",
        labels={"color": "Regime"},
    )
    st.plotly_chart(fig_regime, use_container_width=True)

st.subheader("Regime Distribution")
regime_counts = regimes["regime"].value_counts().sort_index()
st.bar_chart(regime_counts)
