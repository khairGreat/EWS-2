from fastapi import APIRouter
from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse

from api.data_loader import df
from api.model_loader import model
from api.utils import recursive_forecast, create_feature


router = APIRouter()


# entry point
@router.get("/")
def root():
    print("Root endpoint called")
    return "Welcome"


@router.get("/info")
def get_info():
    return {"data_shape": df.shape}


@router.get("/forecast/{horizon}")
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
