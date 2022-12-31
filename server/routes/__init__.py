from fastapi import APIRouter

router=APIRouter()
from .auth.sso import router as sso
router.include_router(sso, prefix="/sso")
from .auth.otp import router as otp
router.include_router(otp, prefix="/otp")
from .user import router as user
router.include_router(user, prefix="/user")