# Quant Equity Technology Portfolio

This repository contains three end-to-end projects designed for quantitative equity technology teams.
Each project mirrors a real investment engineering workflow: research, optimization, and production-facing monitoring.

## Why this portfolio stands out

- **Quant research depth:** factor construction, IC analysis, transaction costs, and walk-forward validation.
- **Production engineering:** modular Python packages, tests, typed models, and API-first design.
- **Optimization skills:** constrained portfolio construction with practical controls used by portfolio managers.
- **Data + systems mindset:** high-performance local analytics using `duckdb` and vectorized pipelines.
- **Communication quality:** every project includes a recruiter-friendly README with context, decisions, and trade-offs.

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

- Add cloud-native orchestration (e.g., batch jobs and scheduled research pipelines).
- Integrate real data providers and realistic slippage models.
- Add CI/CD with quality gates and benchmark tracking.
