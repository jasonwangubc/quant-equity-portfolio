"""Optimization engines for quantitative portfolio construction."""

from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

from optimizer_api.models import MeanVarianceRequest, RiskParityRequest


def _to_numpy(matrix: list[list[float]]) -> np.ndarray:
    return np.asarray(matrix, dtype=float)


def _portfolio_stats(weights: np.ndarray, mu: np.ndarray, cov: np.ndarray) -> tuple[float, float]:
    expected_return = float(weights @ mu)
    variance = float(weights @ cov @ weights)
    volatility = float(np.sqrt(max(variance, 0.0)))
    return expected_return, volatility


def solve_mean_variance(request: MeanVarianceRequest) -> dict[str, float | list[float]]:
    """Solve a constrained mean-variance objective with optional turnover penalty."""
    mu = np.asarray(request.expected_returns, dtype=float)
    cov = _to_numpy(request.covariance)
    n = len(mu)

    initial = np.full(n, 1.0 / n)
    current = (
        np.asarray(request.current_weights, dtype=float)
        if request.current_weights is not None
        else np.zeros(n, dtype=float)
    )
    bounds = [(request.min_weight, request.max_weight)] * n
    constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]

    def objective(weights: np.ndarray) -> float:
        risk = request.risk_aversion * float(weights @ cov @ weights)
        ret = float(weights @ mu)
        turnover_cost = request.turnover_penalty * float(np.sum((weights - current) ** 2))
        return risk - ret + turnover_cost

    result = minimize(
        objective,
        x0=initial,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"ftol": 1e-10, "maxiter": 1000, "disp": False},
    )
    if not result.success:
        raise ValueError(f"Optimization failed: {result.message}")

    weights = np.asarray(result.x, dtype=float)
    expected_return, expected_vol = _portfolio_stats(weights, mu, cov)
    return {
        "weights": weights.tolist(),
        "expected_return": expected_return,
        "expected_volatility": expected_vol,
        "objective_value": float(result.fun),
    }


def solve_risk_parity(request: RiskParityRequest) -> dict[str, float | list[float]]:
    """Compute long-only risk parity weights using iterative rebalancing."""
    cov = _to_numpy(request.covariance)
    n = cov.shape[0]
    weights = np.full(n, 1.0 / n)
    target_rc = np.full(n, 1.0 / n)

    for _ in range(request.max_iterations):
        marginal = cov @ weights
        portfolio_var = float(weights @ marginal)
        if portfolio_var <= 0:
            raise ValueError("Non-positive portfolio variance encountered.")

        risk_contrib = weights * marginal / portfolio_var
        error = risk_contrib - target_rc
        if float(np.linalg.norm(error, ord=2)) < request.tolerance:
            break

        # Multiplicative update keeps weights positive and stable.
        adjustment = target_rc / np.clip(risk_contrib, 1e-12, None)
        weights *= adjustment ** 0.5
        weights = np.clip(weights, 1e-12, None)
        weights /= weights.sum()

    mu = np.zeros(n, dtype=float)
    expected_return, expected_vol = _portfolio_stats(weights, mu, cov)
    objective = float(np.sum((risk_contrib - target_rc) ** 2))
    return {
        "weights": weights.tolist(),
        "expected_return": expected_return,
        "expected_volatility": expected_vol,
        "objective_value": objective,
    }
