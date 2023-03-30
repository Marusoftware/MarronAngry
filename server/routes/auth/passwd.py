from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, Request

from ...security import oauth, get_user
from ...models.response.user import User, Token
from ...models.request import UserCreate
from ...models.db.user import User as UserDB
from ...models.db.auth import Token as TokenDB, TokenType
import secrets
from passlib.context import CryptContext

from tortoise.expressions import Q

crypt=CryptContext(schemes=["bcrypt"], deprecated="auto")

router=APIRouter()

@router.post("/signin", response_model=Token)
async def signin(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user=await UserDB.get_or_none(Q(name=form_data.username) | Q(email=form_data.username))
    if user is None:
        raise HTTPException(status_code=400, detail="Password or Username is wrong.")
    if user.password is not None:
        if not crypt.verify(form_data.password,user.password):
            raise HTTPException(status_code=400, detail="Password or Username is wrong.")
        if user.otp_key is not None:
            token=await TokenDB.create(token=secrets.token_hex(32), token_type=TokenType.pre, user=user)
            return {"access_token": token.token, "token_type": "pre", "user_id":str(user.id)}
        else:
            token=await TokenDB.create(token=secrets.token_hex(32), token_type=TokenType.bearer, user=user)
            if "users" not in request.session:
                request.session["users"]=[]
            request.session["users"].append({"name":user.name, "id":str(user.id), "token":token.token})
            return {"access_token": token.token, "token_type": "bearer", "user_id":str(user.id)}

@router.post("/signup", response_model=User)
async def signup(user:UserCreate):
    return await UserDB.create(name=user.name, fullname=user.fullname, email=user.email, password=crypt.hash(user.password), is_dev=False)

@router.post("/signout")
async def signout(request:Request, token:str =Depends(oauth)):
    if "users" in request.session:
        request.session["users"]=[user for user in request.session["users"] if user["token"]!=token]
    await TokenDB.filter(token=token).delete()