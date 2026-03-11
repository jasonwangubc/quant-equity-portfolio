# Project 3: Regime & Risk Dashboard

## Recruiter value proposition

This project demonstrates **decision-support tooling** for PMs and researchers by combining risk analytics and interactive visualization.

## What it does

- Simulates multi-asset returns with latent calm/stress market states.
- Builds a strategy proxy and benchmark series.
- Detects regimes from rolling return/volatility features using Gaussian Mixture Models.
- Tracks operational risk metrics:
  - rolling volatility
  - drawdown
  - VaR / CVaR
  - stress-shock proxy impact

## Run the dashboard

```bash
streamlit run projects/regime_dashboard/app.py
```

## Core files

- `src/regime_dashboard/data.py`: synthetic market generation.
- `src/regime_dashboard/regime.py`: unsupervised regime detection.
- `src/regime_dashboard/risk.py`: risk metric library.
- `app.py`: Streamlit UI and charts.

## Interview talking points

- Why regime-aware monitoring matters for factor portfolios.
- How to distinguish model confidence from model correctness.
- How to productionize this dashboard with scheduled data refresh and alerting.
