# Quant Equity Portfolio

This repository contains three Python projects related to quantitative equity workflows:
- factor research and backtesting
- portfolio optimization via API
- regime/risk monitoring dashboard

All projects use synthetic data, run locally, and include tests.

## Projects

### 1) Factor Research Lab (`projects/factor_research`)

Builds a synthetic equity panel, computes factor signals, runs a long-short backtest, and reports summary metrics.

Main features:
- factor construction (value, momentum, quality, low volatility)
- turnover-aware returns with transaction cost assumptions
- rank IC, Sharpe, drawdown, hit rate, and turnover summaries

Run:
```bash
python scripts/run_factor_research_demo.py
```

### 2) Portfolio Optimizer API (`projects/optimizer_api`)

FastAPI service for constrained portfolio optimization.

Main features:
- mean-variance optimization with weight bounds and turnover penalty
- risk-parity allocation
- typed request/response models and API tests

Run API:
```bash
python projects/optimizer_api/main.py
```

Docs:
- http://127.0.0.1:8000/docs

Run examples:
```bash
python scripts/run_optimizer_examples.py
```

### 3) Regime & Risk Dashboard (`projects/regime_dashboard`)

Streamlit dashboard for viewing market regimes and strategy risk metrics.

Main features:
- rolling volatility and drawdown charts
- VaR/CVaR metrics
- regime labeling using a Gaussian Mixture Model

Run:
```bash
streamlit run projects/regime_dashboard/app.py
```

## Setup

Requirements:
- Python 3.10+

Install:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

Run tests:
```bash
pytest
```

Run all demos at once:
```bash
python scripts/showcase.py
```

## Repository Layout

```text
projects/
  factor_research/
  optimizer_api/
  regime_dashboard/
scripts/
data/
```
