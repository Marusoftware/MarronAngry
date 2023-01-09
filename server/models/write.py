from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name:str
    fullname:str
    email:EmailStr
    password:str