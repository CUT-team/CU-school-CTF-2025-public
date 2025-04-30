from fastapi import APIRouter

router = APIRouter(tags=["ping"])


@router.get("/ping")
async def ping():
    return {"ping": "pong"}
