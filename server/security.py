from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from .models.db import Token, TokenType

oauth=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin")

async def get_user(token: oauth=Depends()):
    token:Token=await Token.get(token=token, token_type=TokenType.bearer).prefetch_related("user")
    return token.user