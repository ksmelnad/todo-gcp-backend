from fastapi import APIRouter, Depends
from auth import verify_jwt

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/protected")
async def protected(user: dict = Depends(verify_jwt)):
    return {"status": "ok", "user_id": user["user_id"]}
