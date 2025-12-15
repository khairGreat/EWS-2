from fastapi import APIRouter


operational_router = APIRouter(prefix="/operational")


@operational_router.get("/")
def operational_root():
    return {"success": True, "message": "At operational router"}
