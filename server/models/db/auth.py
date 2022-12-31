from enum import Enum
from tortoise.fields import OneToOneRelation, OneToOneField, CharField, ReverseRelation, UUIDField, BooleanField, DatetimeField, ForeignKeyField, ForeignKeyRelation, CharEnumField
from tortoise.models import Model
from tortoise import fields
from .user import User

class Auth(Model):
    user:OneToOneRelation[User] = OneToOneField("models.User", related_name="auth", on_delete=fields.CASCADE, back_populates="auth", pk=True)
    password = CharField(max_length=1024, null=True, description="User password")
    otp_key = CharField(max_length=32, null=True, description="OTP Secret Key")
    oauths:ReverseRelation["OAuth"]
    tokens:ReverseRelation["Token"]

class OAuth(Model):
    id = UUIDField(pk=True, description="OAuth ID")
    provider = CharField(max_length=100, description="OAuth Provider")
    token1 = CharField(max_length=200)
    token2 = CharField(max_length=200)
    is_oauth2 = BooleanField(default=False)
    expires_at = DatetimeField(null=True)
    auth:ForeignKeyRelation[Auth] = ForeignKeyField("models.Auth", related_name="oauths", to_field="user", on_delete=fields.CASCADE)

class TokenType(Enum):
    bearer="bearer"
    pre="pre"

class Token(Model):
    token = CharField(pk=True, max_length=200)
    token_type = CharEnumField(TokenType, description="Token Type", max_length=10)
    auth:ForeignKeyRelation[Auth] = ForeignKeyField("models.Auth", related_name="tokens", to_field="user", on_delete=fields.CASCADE)