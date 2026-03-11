# Project 2: Portfolio Optimizer API

## Recruiter value proposition

This service shows how I would ship an optimization engine to researchers and PMs as a **reliable internal platform component**, not just a notebook.

## What it does

- Exposes optimization endpoints with typed schemas and validation.
- Supports:
  - **Mean-variance optimization** with practical constraints:
    - long-only bounds
    - max weight limits
    - turnover penalty vs. current holdings
  - **Risk parity optimization** for diversified risk contribution.
- Returns weights and portfolio diagnostics in a consistent response model.

## Endpoints

- `GET /health`
- `POST /optimize/mean-variance`
- `POST /optimize/risk-parity`

## Run locally

```bash
python projects/optimizer_api/main.py
```

Interactive docs:
- <http://127.0.0.1:8000/docs>

## Example payload (mean-variance)

```json
{
  "expected_returns": [0.10, 0.08, 0.06, 0.07],
  "covariance": [
    [0.040, 0.012, 0.010, 0.013],
    [0.012, 0.030, 0.011, 0.012],
    [0.010, 0.011, 0.025, 0.009],
    [0.013, 0.012, 0.009, 0.035]
  ],
  "risk_aversion": 6.0,
  "min_weight": 0.0,
  "max_weight": 0.45,
  "turnover_penalty": 0.05,
  "current_weights": [0.25, 0.25, 0.25, 0.25]
}
```

## Interview talking points

- Why turnover penalties matter in real implementation.
- How to validate optimizer requests defensively.
- How this API can plug into a nightly rebalance orchestration pipeline.
