from uuid import UUID
from fastapi import APIRouter
from ..models.db.user import User

router=APIRouter(tags=["user"])

@router.get("/me")
async def me():
    return await User.get_or_none()

@router.get("/{id}")
async def get(id:UUID):
    await User.get_or_none(id=id)