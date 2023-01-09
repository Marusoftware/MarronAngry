from fastapi import APIRouter, Depends, Request
from passlib.totp import TOTP
from ...models.db import Token, TokenType
from ...security import get_user
import secrets

router=APIRouter()

@router.put("/")
async def setup(user: get_user=Depends()):
    totp=TOTP(new=True)
    user.key=totp.key
    await user.save()
    return totp.to_uri(label="User", issuer="Marron")

@router.post("/")
async def auth(request:Request, pre_token:str, token:str):
    db_token=await Token.get_or_none(token=pre_token, token_type=TokenType.pre).prefetch_related("user")
    user=db_token.user
    totp=TOTP(key=user.otp_key)
    await db_token.delete()
    totp.verify(token=token)
    db_token=await Token.create(token=secrets.token_hex(32), token_type=TokenType.pre, user=user)
    if "users" not in request.session:
        request.session["users"]=[]
    request.session["users"].append({"name":user.name, "id":str(user.id), "token":db_token.token})
    return {"access_token": db_token.token, "token_type": "bearer", "user_id":str(user.id)}