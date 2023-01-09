from uuid import UUID
from fastapi import APIRouter, Depends
from ..security import get_user
from ..models.read.user import User

router=APIRouter(tags=["user"])

@router.get("/me", response_model=User)
async def me(user:get_user=Depends()):
    return user

@router.get("/{id}")
async def get(id:UUID):
    await User.get_or_none(id=id)