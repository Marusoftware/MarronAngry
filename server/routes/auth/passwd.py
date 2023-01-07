from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from ...models.db.user import User
from ...models.db.auth import Token, TokenType
import secrets
from passlib.context import CryptContext

crypt=CryptContext(schemes=["bcrypt"], deprecated="auto")

router=APIRouter()

oauth=OAuth2PasswordBearer(tokenUrl="token")

@router.post("/signin")
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    user=await User.get_or_none(name=form_data.username).prefetch_related("auth")
    if user is None:
        raise HTTPException(status_code=400, detail="Password or Username is wrong.")
    if user.auth.password is not None:
        if not crypt.verify(form_data.password,user.auth.password):
            raise HTTPException(status_code=400, detail="Password or Username is wrong.")
        if user.auth.otp_key is not None:
            token=await Token.create(token=secrets.token_hex(32), token_type=TokenType.pre)
            return {"access_token": token.token, "token_type": "pre"}
        else:
            token=await Token.create(token=secrets.token_hex(32), token_type=TokenType.pre)
            return {"access_token": token.token, "token_type": "bearer"}

@router.post("/signup")
async def signup():
    await User.create()
