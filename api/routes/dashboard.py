from fastapi import APIRouter
import pandas as pd

from api.utils.dashboard_utils import (
    pest_sum,
    average_pest_count,
    above_threshold_level,
    economic_damage,
    action_rate,
    most_affected_field_stage,
    current_field_stage,
)
from api._pydanticModel import KPIRequest
from api.data_loader import df


dashboard_router = APIRouter(prefix="/dashboard")


@dashboard_router.get("/")
def dashboard_root():
    return {"success": True, "message": "At dashboard router"}


@dashboard_router.post(
    "/kpi",
    summary="KPI Response",
    description="Compute key performance indicators (KPIs) for a given date range, season, and stage.",
)
def dashboard_kpi(request: KPIRequest):
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
    

