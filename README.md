# Quant Equity Technology Portfolio

This repo has three projects built for quantitative equity technology roles.
Together they cover the main workflow: research, portfolio construction, and risk monitoring.

## Why I built these

- **End-to-end projects:** each one is runnable and tested, not just a notebook snippet.
- **Practical quant problems:** factor quality, turnover-aware backtests, optimization constraints, and risk diagnostics.
- **Clean engineering basics:** modular Python code, typed models, tests, and clear folder structure.
- **Tooling that matches the domain:** `duckdb` for local analytics, FastAPI for internal services, Streamlit for PM/research visibility.
- **Readable docs:** every project has a short README that explains assumptions, decisions, and possible extensions.

## Projects

1. **Factor Research Lab** (`projects/factor_research`)
   - Builds a synthetic equity universe.
   - Computes multiple factors (value, momentum, quality, low volatility).
   - Runs a long-short backtest with turnover and cost-aware execution.
   - Produces PM-facing analytics (Sharpe, drawdown, IC, hit rate, turnover).

2. **Portfolio Optimizer API** (`projects/optimizer_api`)
   - FastAPI service for constrained portfolio optimization.
   - Includes mean-variance optimization with turnover penalty and risk-parity weights.
   - Uses typed request/response schemas and unit tests.

3. **Regime & Risk Dashboard** (`projects/regime_dashboard`)
   - Streamlit app for regime detection and risk diagnostics.
   - Includes rolling volatility, drawdown, VaR, CVaR, and stress scenario analysis.
   - Helps researchers and PMs understand strategy behavior through market shifts.

## Quickstart

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
pytest
```

### Run project demos

```bash
python scripts/showcase.py
python scripts/run_factor_research_demo.py
python scripts/run_optimizer_examples.py
streamlit run projects/regime_dashboard/app.py
```

## Project structure

```text
projects/
  factor_research/
  optimizer_api/
  regime_dashboard/
scripts/
data/
```

## Future upgrades

- Add scheduled batch runs so research and reporting update automatically.
- Plug in real market data and more realistic slippage/impact assumptions.
- Add CI checks and lightweight performance tracking over time.
