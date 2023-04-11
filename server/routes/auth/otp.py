from fastapi import APIRouter, Depends, Request, HTTPException
from passlib.totp import TOTP, InvalidTokenError
from ...models.db import Token as TokenDB, TokenType, User as UserDB, OTPStatus
from ...models.response.user import Token
from ...models.request import OTPCreate
from ...security import get_user
import secrets

router=APIRouter()

@router.put("/", response_model=OTPCreate)
async def otpSetup(user:UserDB =Depends(get_user)):
    totp=TOTP(new=True)
    user.otp_key=totp.base32_key
    user.otp_recovery=",".join(["".join([str(secrets.choice(list(range(10)))) for i in range(6)]) for i in range(12)])
    user.otp_status=OTPStatus.verify
    await user.save()
    return {"otp_url":totp.to_uri(label=user.email, issuer="Marron"), "otp_recovery":user.otp_recovery.split(",")}

@router.post("/verify")
async def otpVerify( recovery_key:str, user:UserDB = Depends(get_user)):
    if user.otp_status==OTPStatus.verify:
        if recovery_key in user.otp_recovery.split(","):
            user.otp_status=OTPStatus.working
            await user.save()
        else:
            raise HTTPException(status_code=400, detail="Token is not correct.")
    else:
        raise HTTPException(status_code=404, detail="Verify is not needed.")

@router.post("/", response_model=Token)
async def otpAuth(request:Request, pre_token:str, token:str):
    db_token=await TokenDB.get_or_none(token=pre_token, token_type=TokenType.pre).prefetch_related("user")
    if db_token is None:
        raise HTTPException(status_code=400, detail="Pre auth token expired.")
    user=db_token.user
    if user.otp_status != OTPStatus.working:
        raise HTTPException(status_code=400, detail="Your OTP is not verifyed.")
    totp=TOTP(key=user.otp_key)
    await db_token.delete()
    try:
        totp.match(token=token)
    except InvalidTokenError:
        otp_recovery=user.otp_recovery.split(",")
        if token in otp_recovery:
            otp_recovery.remove(token)
            user.otp_recovery=otp_recovery
            user.otp_status=OTPStatus.recovered
            await user.save()
        else:
            raise HTTPException(status_code=400, detail="Token is not correct.")
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