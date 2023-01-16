from enum import Enum
from tortoise.fields import OneToOneRelation, OneToOneField, CharField, ReverseRelation, UUIDField, BooleanField, DatetimeField, ForeignKeyField, ForeignKeyRelation, CharEnumField
from tortoise.models import Model
from tortoise import fields
from .user import User

class TokenType(Enum):
    bearer="bearer"
    pre="pre"

class Token(Model):
    token = CharField(pk=True, max_length=200, description="Token")
    token_type = CharEnumField(TokenType, description="Token Type", max_length=10)
    user:ForeignKeyRelation[User] = ForeignKeyField("models.User", related_name="tokens", to_field="id", on_delete=fields.CASCADE)