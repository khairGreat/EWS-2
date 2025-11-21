from fastapi import FastAPI
from data_loader import df


app = FastAPI()


# entry point
@app.get("/")
def root():
    print("Root endpoint called")
    return "Welcome"


@app.get("/info")
def get_info():
    return {"data_shape": df.shape}


@app.get("/forecast/{horizon}")
def get_forecast(horizon: int):
    print("Forecast endpoint called")
    return "forecast"
