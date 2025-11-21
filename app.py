from fastapi import FastAPI
from api.controller import router

app = FastAPI()
# entry point


@app.get("/")
def root():
    return "Welcome hahaha"


app.include_router(router)
