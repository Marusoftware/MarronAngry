from uuid import UUID, uuid4
from sqlalchemy import Unicode
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, SecretStr
from sqlalchemy_utils import PasswordType, EmailType, UUIDType, force_auto_coercion

force_auto_coercion()

class User(SQLModel, table=True):
    __tablename__="user"
    id:UUID = Field(sa_type=UUIDType(), default_factory=uuid4, primary_key=True, index=True, nullable=False, unique=True, description="User ID")
    name:str = Field(sa_type=Unicode(1024), index=True, nullable=False, unique=True, description="User short name")
    fullname:str = Field(sa_type=Unicode(1024), default="", nullable=False, description="User long name")
    is_dev:bool = Field(default=False, nullable=False, description="Is this user developer?")
    email:"Email" = Relationship(back_populates="user", sa_relationship_kwargs={"uselist":False})
    auth:"Auth" = Relationship(back_populates="user", sa_relationship_kwargs={"uselist":False})

class Email(SQLModel, table=True):
    __tablename__="email"
    email:EmailStr = Field(sa_type=EmailType, primary_key=True, index=True, nullable=False, unique=True, description="User email")
    is_marusoftware:bool = Field(default=False, nullable=False, description="Is this email marusoftware's?")
    user_id:UUID = Field(foreign_key="user.id", description="User ID")
    user:User = Relationship(back_populates="email")

class Auth(SQLModel, table=True):
    __tablename__="auth"
    user_id:UUID = Field(primary_key=True, unique=True, default=None, description="User ID", foreign_key="user.id")
    password:SecretStr = Field(sa_type=PasswordType(max_length=1024, schemes=['pbkdf2_sha512','md5_crypt'], deprecated=['md5_crypt']), nullable=True, description="User password")