from fastapi.testclient import TestClient

from optimizer_api.api import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_mean_variance_endpoint() -> None:
    payload = {
        "expected_returns": [0.10, 0.08, 0.06, 0.07],
        "covariance": [
            [0.040, 0.012, 0.010, 0.013],
            [0.012, 0.030, 0.011, 0.012],
            [0.010, 0.011, 0.025, 0.009],
            [0.013, 0.012, 0.009, 0.035],
        ],
        "risk_aversion": 5.0,
        "min_weight": 0.0,
        "max_weight": 0.5,
        "turnover_penalty": 0.1,
        "current_weights": [0.25, 0.25, 0.25, 0.25],
    }
    response = client.post("/optimize/mean-variance", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["method"] == "mean_variance"
    assert abs(sum(body["weights"]) - 1.0) < 1e-8
