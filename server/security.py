from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from .models.db import Token

oauth=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

async def get_user(token: oauth=Depends()):
    token:Token=await Token.get(token=token).prefetch_related("user")
    return token.user