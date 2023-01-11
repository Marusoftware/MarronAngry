from pydantic import BaseModel, EmailStr
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id:UUID

class User(BaseModel):
    id:UUID
    name:str
    fullname:str
    is_dev:bool
    email:EmailStr

class UserOpen(BaseModel):
    id:UUID
    name:str
    is_dev:bool
