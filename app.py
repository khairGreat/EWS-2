from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.controller import router
from api.utils.lifespan import lifespan


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",  # React dev
    "http://127.0.0.1:3000",
    "http://localhost:5173", "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return "Welcome hahaha"


app.include_router(router)
