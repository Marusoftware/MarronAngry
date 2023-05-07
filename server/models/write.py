from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime

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

class TaskCreate(BaseModel):
    name:str
    description:str
    start:datetime
    end:datetime
    project_id:UUID

class TaskUpdate(TaskCreate):
    name:str=None
    description:str=None
    start:datetime=None
    end:datetime=None
    project_id:UUID=None

class IdeaCreate(BaseModel):
    name:str
    description:str
    project_id:UUID

class IdeaUpdate(IdeaCreate):
    name:str=None
    description:str=None
    project_id:UUID=None