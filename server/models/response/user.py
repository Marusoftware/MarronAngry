from typing import List
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime 

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

class Member(BaseModel):
    id:UUID
    is_admin:bool
    user_id:UUID

class Organization(BaseModel):
    id:UUID
    name:str
    description:str
    members:List[Member]

class Project(BaseModel):
    id:UUID
    name:str
    description:str
    organization_id:UUID
    members:List[Member]

class Task(BaseModel):
    id:UUID
    name:str
    description:str
    project_id:UUID
    time:datetime
    members:List[Member]