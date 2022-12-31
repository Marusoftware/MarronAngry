from pydantic import BaseModel

class UserCreate(BaseModel):
    name:str
    fullname:str
    email:str