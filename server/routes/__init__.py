from fastapi import APIRouter

router=APIRouter()
from .sso import router as sso
router.include_router(sso, prefix="/sso")