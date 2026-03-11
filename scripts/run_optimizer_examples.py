"""Run local examples for optimization engines."""

from __future__ import annotations

from pprint import pprint

from optimizer_api.models import MeanVarianceRequest, RiskParityRequest
from optimizer_api.optimize import solve_mean_variance, solve_risk_parity


def main() -> None:
    covariance = [
        [0.040, 0.012, 0.010, 0.013],
        [0.012, 0.030, 0.011, 0.012],
        [0.010, 0.011, 0.025, 0.009],
        [0.013, 0.012, 0.009, 0.035],
    ]

    mv = MeanVarianceRequest(
        expected_returns=[0.10, 0.08, 0.06, 0.07],
        covariance=covariance,
        risk_aversion=5.0,
        min_weight=0.0,
        max_weight=0.5,
        turnover_penalty=0.05,
        current_weights=[0.25, 0.25, 0.25, 0.25],
    )
    rp = RiskParityRequest(covariance=covariance)

    print("Mean-Variance Result")
    pprint(solve_mean_variance(mv))
    print("\nRisk-Parity Result")
    pprint(solve_risk_parity(rp))


if __name__ == "__main__":
    main()
