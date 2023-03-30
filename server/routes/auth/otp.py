from fastapi import APIRouter, Depends, Request
from passlib.totp import TOTP, InvalidTokenError
from ...models.db import Token as TokenDB, TokenType, User as UserDB
from ...models.response.user import Token
from ...models.request import OTPCreate
from ...security import get_user
import secrets

router=APIRouter()

@router.put("/", response_model=OTPCreate)
async def otpSetup(user:UserDB =Depends(get_user)):
    totp=TOTP(new=True)
    user.otp_key=totp.base32_key
    user.otp_recovery="".join([str(secrets.choice(list(range(10)))) for i in range(6)])
    await user.save()
    return {"otp_url":totp.to_uri(label=user.email, issuer="Marron"), "otp_recovery":user.otp_recovery}

@router.post("/", response_model=Token)
async def otpAuth(request:Request, pre_token:str, token:str):
    db_token=await TokenDB.get_or_none(token=pre_token, token_type=TokenType.pre).prefetch_related("user")
    user=db_token.user
    totp=TOTP(key=user.otp_key)
    await db_token.delete()
    try:
        totp.match(token=token)
    except InvalidTokenError:
        if user.otp_recovery == token:
            user.otp_recovery="".join([str(secrets.choice(list(range(10)))) for i in range(6)])
            await user.save()
        else:
            raise InvalidTokenError
    db_token=await TokenDB.create(token=secrets.token_hex(32), token_type=TokenType.pre, user=user)
    if "users" not in request.session:
        request.session["users"]=[]
    request.session["users"].append({"name":user.name, "id":str(user.id), "token":db_token.token})
    return {"access_token": db_token.token, "token_type": "bearer", "user_id":str(user.id)}

@router.delete("/")
async def otpDelete(user:UserDB =Depends(get_user)):
    user.otp_key=None
    user.otp_recovery=None
    await user.save()