from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


RouletteNumber = Annotated[
    int,
    Field(
        ge=0,
        le=36,
    ),
]


PredictionStrategy = Literal[
    "v1",
    "baseline_random",
    "baseline_frequency",
    "baseline_hot",
    "baseline_cold",
    "ml_logistic_regression",
    "ml_random_forest",
    "ml_gradient_boosting",
    "ml_xgboost",
]


class StrictRequestModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class SessionResponse(BaseModel):
    session_id: UUID
    status: str
    initial_spin_count: int
    started_at: datetime
    ended_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class InitialSpinsRequest(
    StrictRequestModel
):
    spins: list[RouletteNumber] = Field(
        min_length=10,
        max_length=15,
    )


class AddSpinRequest(
    StrictRequestModel
):
    number: RouletteNumber


class SpinResponse(BaseModel):
    spin_id: UUID
    session_id: UUID
    spin_index: int
    number: int
    spin_type: str
    spun_at: datetime | None = None
    created_at: datetime | None = None


class SessionStatisticsResponse(BaseModel):
    session_id: UUID
    spin_count: int
    statistics: dict[str, Any]


class PredictionRequest(
    StrictRequestModel
):
    strategy: PredictionStrategy = "v1"

    recent_window: int = Field(
        default=10,
        ge=1,
    )


class PredictionResponse(BaseModel):
    prediction_run_id: UUID
    session_id: UUID
    strategy: str
    prediction_for_spin_index: int
    input_spin_count: int
    recent_window: int | None = None
    model_version_id: UUID | None = None
    predictions: dict[str, Any]
    number_probabilities: list[dict] | None = None


class StoredPredictionResponse(BaseModel):
    prediction_run: dict[str, Any]
    prediction_items: list[
        dict[str, Any]
    ]


class EvaluationResponse(BaseModel):
    session_id: UUID
    evaluation_count: int
    evaluations: list[
        dict[str, Any]
    ]


class ComparisonResponse(BaseModel):
    session_id: UUID
    strategy_count: int
    strategies: dict[str, Any]


class MLPerformanceResponse(BaseModel):
    session_id: UUID
    model_count: int
    models: list[
        dict[str, Any]
    ]


class ModelsResponse(BaseModel):
    model_version_count: int
    models: list[
        dict[str, Any]
    ]