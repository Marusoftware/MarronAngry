from tortoise import fields
from tortoise.models import Model
from tortoise.fields import UUIDField, CharField, BooleanField, OneToOneField, OneToOneRelation, ReverseRelation, ForeignKeyRelation, DatetimeField

class User(Model):
    id = UUIDField(pk=True, description="User ID")
    name = CharField(max_length=1024, unique=True, index=True, description="User short name")
    fullname = CharField(max_length=1024, default="", description="User long name")
    is_dev = BooleanField(default=False, description="Is this user developer?")
    email = CharField(max_length=1024, description="User email")
    auth:OneToOneRelation["Auth"]

class Auth(Model):
    user:OneToOneRelation[User] = OneToOneField("models.User", related_name="auth", on_delete=fields.CASCADE, back_populates="auth", pk=True)
    password = CharField(max_length=1024, null=True, description="User password")
    oauths:ReverseRelation["OAuth"]

class OAuth(Model):
    id = UUIDField(pk=True, description="OAuth ID")
    provider = CharField(max_length=100, description="OAuth Provider")
    token1 = CharField(max_length=200)
    token2 = CharField(max_length=200)
    is_oauth2 = BooleanField(default=False)
    expires_at = DatetimeField(null=True)
    auth:ForeignKeyRelation[Auth] = fields.ForeignKeyField("models.Auth", related_name="oauths", to_field="user", on_delete=fields.CASCADE)