# Project 1: Factor Research Lab

## Recruiter value proposition

This project demonstrates how I would support a quant equity team from **data engineering to signal validation**:
- Build a repeatable panel dataset.
- Engineer cross-sectional factors.
- Run cost-aware backtests.
- Report PM-relevant diagnostics.

## What it does

1. Generates a synthetic multi-asset monthly equity panel.
2. Stores the panel in `duckdb` for reproducible analytics workflows.
3. Constructs factor signals:
   - Value (`book_to_market`)
   - Momentum (`12-1`)
   - Quality (`earnings_yield`)
   - Low Volatility (inverse trailing vol)
4. Runs a long-short decile-style strategy with turnover and transaction costs.
5. Outputs summary metrics including annualized return, volatility, Sharpe, drawdown, and rank IC.

## Key files

- `src/factor_research/data.py`: synthetic panel + DuckDB persistence.
- `src/factor_research/factors.py`: factor definitions and z-score normalization.
- `src/factor_research/backtest.py`: long-short engine with turnover.
- `src/factor_research/metrics.py`: performance and IC diagnostics.
- `src/factor_research/pipeline.py`: full orchestration function.

## Run it

```bash
python scripts/run_factor_research_demo.py
```

The script writes data to `data/factor_research.duckdb` and prints strategy stats.

## Interview talking points

- Why rank IC is used alongside PnL metrics.
- How turnover-aware costs change research conclusions.
- How to transition this pipeline to a cloud batch system.
