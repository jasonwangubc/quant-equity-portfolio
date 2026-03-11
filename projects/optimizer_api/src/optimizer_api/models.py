"""Pydantic models for optimization requests and responses."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class MeanVarianceRequest(BaseModel):
    expected_returns: list[float] = Field(..., description="Expected asset returns.")
    covariance: list[list[float]] = Field(..., description="Asset covariance matrix.")
    risk_aversion: float = Field(5.0, gt=0.0, description="Risk aversion coefficient.")
    min_weight: float = Field(0.0, ge=0.0, le=1.0)
    max_weight: float = Field(0.2, gt=0.0, le=1.0)
    turnover_penalty: float = Field(0.0, ge=0.0)
    current_weights: list[float] | None = Field(
        default=None, description="Optional reference portfolio for turnover control."
    )

    @model_validator(mode="after")
    def validate_shapes(self) -> "MeanVarianceRequest":
        n = len(self.expected_returns)
        if n == 0:
            raise ValueError("expected_returns must not be empty.")
        if len(self.covariance) != n or any(len(row) != n for row in self.covariance):
            raise ValueError("covariance must be square and align with expected_returns.")
        if self.current_weights is not None and len(self.current_weights) != n:
            raise ValueError("current_weights length must match expected_returns length.")
        if self.min_weight > self.max_weight:
            raise ValueError("min_weight cannot be greater than max_weight.")
        return self


class RiskParityRequest(BaseModel):
    covariance: list[list[float]]
    max_iterations: int = Field(400, ge=50, le=5000)
    tolerance: float = Field(1e-8, gt=0.0, le=1e-3)

    @model_validator(mode="after")
    def validate_covariance(self) -> "RiskParityRequest":
        n = len(self.covariance)
        if n == 0 or any(len(row) != n for row in self.covariance):
            raise ValueError("covariance must be a non-empty square matrix.")
        return self


class OptimizationResponse(BaseModel):
    method: Literal["mean_variance", "risk_parity"]
    weights: list[float]
    expected_return: float
    expected_volatility: float
    objective_value: float
