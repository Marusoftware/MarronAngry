from fastapi import APIRouter, Depends, Request
from passlib.totp import TOTP
from ...models.db import Token as TokenDB, TokenType
from ...models.read.user import Token
from ...security import get_user
import secrets

router=APIRouter()

@router.put("/", response_model=str)
async def otpSetup(user: get_user=Depends()):
    totp=TOTP(new=True)
    user.otp_key=totp.base32_key
    await user.save()
    return totp.to_uri(label=user.email).replace('"',"")

@router.post("/", response_model=Token)
async def otpAuth(request:Request, pre_token:str, token:str):
    db_token=await TokenDB.get_or_none(token=pre_token, token_type=TokenType.pre).prefetch_related("user")
    user=db_token.user
    totp=TOTP(key=user.otp_key)
    await db_token.delete()
    totp.match(token=token)
    db_token=await TokenDB.create(token=secrets.token_hex(32), token_type=TokenType.pre, user=user)
    if "users" not in request.session:
        request.session["users"]=[]
    request.session["users"].append({"name":user.name, "id":str(user.id), "token":db_token.token})
    return {"access_token": db_token.token, "token_type": "bearer", "user_id":str(user.id)}