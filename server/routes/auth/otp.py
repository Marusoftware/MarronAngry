from fastapi import APIRouter
from passlib.totp import TOTP
from ...models.db.auth import Token

router=APIRouter()

@router.put("/")
async def setup():
    totp=TOTP(new=True)
    return totp.to_uri(label="User", issuer="Marron")

@router.post("/")
async def auth():
    totp=TOTP(key="")