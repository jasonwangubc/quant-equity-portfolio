"""FastAPI app exposing optimization endpoints."""

from __future__ import annotations

from fastapi import FastAPI

from optimizer_api.models import MeanVarianceRequest, OptimizationResponse, RiskParityRequest
from optimizer_api.optimize import solve_mean_variance, solve_risk_parity

app = FastAPI(
    title="Quant Portfolio Optimizer API",
    description="Constrained portfolio optimization service for quant equity workflows.",
    version="1.0.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/optimize/mean-variance", response_model=OptimizationResponse)
def optimize_mean_variance(request: MeanVarianceRequest) -> OptimizationResponse:
    result = solve_mean_variance(request)
    return OptimizationResponse(method="mean_variance", **result)


@app.post("/optimize/risk-parity", response_model=OptimizationResponse)
def optimize_risk_parity(request: RiskParityRequest) -> OptimizationResponse:
    result = solve_risk_parity(request)
    return OptimizationResponse(method="risk_parity", **result)
