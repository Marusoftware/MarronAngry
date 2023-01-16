from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from ..security import get_user
from ..models.read.user import User, UserOpen
from ..models.write import UserCreate
from ..models.db import User as UserDB
from .auth.passwd import crypt

router=APIRouter(tags=["user"])

@router.get("/me", response_model=User)
async def me(user:UserDB=Depends(get_user)):
    return user

@router.get("/{id}", response_model=UserOpen)
async def get(id:UUID):
    return await UserDB.get(id=id)

@router.delete("/me")
async def delete_me(user:UserDB=Depends(get_user), password:str=None):
    if user.password is not None and password is None:
        raise HTTPException(status_code=400, detail="Password is wrong")
    if user.password is not None:
        if not crypt.verify(password, user.password):
            raise HTTPException(status_code=400, detail="Password is wrong")
    await user.delete()

@router.put("/me", response_model=User)
async def update_me(user:UserCreate, user_db:UserDB=Depends(get_user)):
    user=user.dict()
    user["password"]=crypt.hash(user["password"])
    await user_db.update_from_dict(user)
    return user_db