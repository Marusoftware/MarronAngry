from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name:str
    fullname:str
    email:EmailStr
    password:str

class OrganizationCreate(BaseModel):
    name:str
    description:str

class OTPCreate(BaseModel):
    otp_url:str
    otp_recovery:str