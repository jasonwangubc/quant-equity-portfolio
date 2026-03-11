import numpy as np

from optimizer_api.models import MeanVarianceRequest, RiskParityRequest
from optimizer_api.optimize import solve_mean_variance, solve_risk_parity


def sample_covariance() -> list[list[float]]:
    return [
        [0.040, 0.012, 0.010, 0.013],
        [0.012, 0.030, 0.011, 0.012],
        [0.010, 0.011, 0.025, 0.009],
        [0.013, 0.012, 0.009, 0.035],
    ]


def test_mean_variance_weights_respect_constraints() -> None:
    request = MeanVarianceRequest(
        expected_returns=[0.10, 0.08, 0.06, 0.07],
        covariance=sample_covariance(),
        risk_aversion=5.0,
        min_weight=0.0,
        max_weight=0.5,
        turnover_penalty=0.1,
        current_weights=[0.25, 0.25, 0.25, 0.25],
    )
    result = solve_mean_variance(request)
    weights = np.asarray(result["weights"])
    assert np.isclose(weights.sum(), 1.0, atol=1e-8)
    assert (weights >= -1e-10).all()
    assert (weights <= 0.5 + 1e-10).all()


def test_risk_parity_weights_sum_to_one() -> None:
    request = RiskParityRequest(covariance=sample_covariance())
    result = solve_risk_parity(request)
    weights = np.asarray(result["weights"])
    assert np.isclose(weights.sum(), 1.0, atol=1e-8)
    assert (weights > 0).all()
