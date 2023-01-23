from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name:str
    fullname:str
    email:EmailStr
    password:str

class UserUpdate(BaseModel):
    name:str=None
    fullname:str=None
    email:EmailStr=None
    oldPassword:str=None
    newPassword:str=None

class OrganizationCreate(BaseModel):
    name:str
    description:str

class OrganizationUpdate(BaseModel):
    name:str=None
    description:str=None

class OTPCreate(BaseModel):
    otp_url:str
    otp_recovery:str

class ProjectCreate(BaseModel):
    name:str
    description:str
    organization_id:UUID

class ProjectUpdate(ProjectCreate):
    name:str=None
    description:str=None
    organization_id:UUID=None