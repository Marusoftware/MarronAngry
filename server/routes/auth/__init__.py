from fastapi import APIRouter

from .otp import router as otp
from .passwd import router as login
from .sso import router as sso

router=APIRouter(tags=["auth"])
router.include_router(sso, prefix="/sso")
router.include_router(otp, prefix="/otp")
router.include_router(login)