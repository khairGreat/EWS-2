from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import pandas as pd

from api.data_loader import df
from api.model_loader import model
from api.utils.forecast_utils import create_feature, recursive_forecast
from api._pydanticModel import FilterAll
from api.utils.dashboard_utils import (
    pest_sum,
    average_pest_count,
    above_threshold_level,
    economic_damage,
    dashboard_filter,
    action_rate,
    most_affected_field_stage,
    current_field_stage,
)

router = APIRouter()


@router.get(
    "/",
    summary="Root Endpoint",
    description="Returns a welcome message to confirm the API is running.",
    response_description="A welcome message string.",
)
def root():

    return "Welcome"


@router.get(
    "/info",
    summary="Dataset Information",
    description="Returns information about the loaded dataset, such as number of rows and columns.",
    response_description="Shape of the dataset as (rows, columns).",
)
def get_info():

    return {"data_shape": df.shape}


@router.get(
    "/forecast/{horizon}",
    summary="Generate Forecast",
    description="Generates a recursive forecast for the specified horizon (number of future steps).",
    response_description="Forecast results as a list of predicted values.",
)
def get_forecast(horizon: int):

    print("Forecast endpoint called")

    features = create_feature(df)[0]
    pred = recursive_forecast(model, features, horizon)

    if features is None or pred is None:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "error_message": "Features could not be created or Forecasting error",
            },
        )

    return {"success": True, "data": pred}


@router.post(
    "/kpi",
    summary="KPI Response",
    description="Compute key performance indicators (KPIs) for a given date range, season, and stage.",
)
def kpi_response(request: FilterAll):

    start_date = pd.to_datetime(request.start)
    end_date = pd.to_datetime(request.end)
    season = request.season
    field_stage = request.field_stage

    return {
        "success": True,
        "data": {
            "pest_sum": pest_sum(df, start_date, end_date, season, field_stage),
            "average_pest_count": average_pest_count(
                df, start_date, end_date, season, field_stage
            ),
            "above_threshold%": above_threshold_level(
                df, start_date, end_date, season, field_stage
            ),
            "economic_damage%": economic_damage(
                df, start_date, end_date, season, field_stage
            ),
            "action_rate%": action_rate(df, start_date, end_date, season, field_stage),
            "most_affected_field_stage": most_affected_field_stage(
                df, start_date, end_date, season
            ),
            "current_field_stage": current_field_stage(
                df, start_date, end_date, season
            ),
        },
    }


@router.get(
    "/filters",
    summary="Dashboard Filters",
    description="Retrieve filter options for the dashboard such as seasons, field stages, and pest types.",
    response_description="Available dashboard filter options.",
)
def filtering():

    return {"success": True, "data": dashboard_filter(df)}
