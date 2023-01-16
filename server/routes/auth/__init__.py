from typing import List
from fastapi import APIRouter, Request

from ...models.read.user import Token

from .otp import router as otp
from .passwd import router as login
from .sso import router as sso

router=APIRouter(tags=["auth"])
router.include_router(sso, prefix="/sso")
router.include_router(otp, prefix="/otp")
router.include_router(login)

@router.get("/session", response_model=List[Token])
async def session(request:Request):
    if not "users" in request.session:
        return []
    return [ Token(access_token=user["token"], token_type="bearer", user_id=user["id"]) for user in request.session["users"]]