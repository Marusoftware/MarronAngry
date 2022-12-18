from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from sqlalchemy import Unicode
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, SecretStr
from sqlalchemy_utils import PasswordType, EmailType, UUIDType, force_auto_coercion

force_auto_coercion()

class User(SQLModel, table=True):
    __tablename__="user"
    id:UUID = Field(default_factory=uuid4, primary_key=True, description="User ID")
    name:str = Field(index=True, unique=True, description="User short name")
    fullname:str = Field(default="", description="User long name")
    is_dev:bool = Field(default=False, description="Is this user developer?")
    email:"Email" = Relationship(back_populates="user", sa_relationship_kwargs={"uselist":False})
    auth:"Auth" = Relationship(back_populates="user", sa_relationship_kwargs={"uselist":False})

class Email(SQLModel, table=True):
    __tablename__="email"
    user_id:UUID = Field(primary_key=True, foreign_key="user.id", description="User ID")
    email:EmailStr = Field(sa_type=EmailType, description="User email")
    is_marusoftware:bool = Field(default=False, description="Is this email marusoftware's?")
    user:User = Relationship(back_populates="email")

class Auth(SQLModel, table=True):
    __tablename__="auth"
    user_id:UUID = Field(primary_key=True, description="User ID", foreign_key="user.id")
    password:Optional[SecretStr] = Field(sa_type=PasswordType(max_length=1024, schemes=['pbkdf2_sha512','md5_crypt'], deprecated=['md5_crypt']), nullable=True, description="User password")
    user:User = Relationship(back_populates="auth")
    oauths:List["OAuth"] = Relationship(back_populates="auth")

class OAuth(SQLModel, table=True):
    __tablename__="oauth"
    id:UUID = Field(sa_type=UUIDType(), default_factory=uuid4, primary_key=True, index=True, nullable=False, description="OAuth ID")
    provider:str = Field(sa_type=Unicode(100), index=True, description="OAuth Provider")
    token1:str = Field(max_length=200)
    token2:str = Field(max_length=200)
    is_oauth2:bool
    expires_at:datetime=Field(nullable=True)
    auth:Auth = Relationship(back_populates="oauths")
    user_id:UUID = Field(foreign_key="auth.user_id", default=None)