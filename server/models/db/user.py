from tortoise.fields import UUIDField, CharField, BooleanField, ReverseRelation, ManyToManyRelation, ManyToManyField
from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = UUIDField(pk=True, description="User ID")
    name = CharField(max_length=1024, unique=True, index=True, description="User short name")
    fullname = CharField(max_length=1024, default="", description="User long name")
    is_dev = BooleanField(default=False, description="Is this user developer?")
    email = CharField(max_length=1024, description="User email")
    password = CharField(max_length=1024, null=True, description="User password")
    otp_key = CharField(max_length=32, null=True, description="OTP Secret Key")
    tokens:ReverseRelation["Token"]
    organizations:ManyToManyRelation["Organization"]

class Organization(Model):
    id = UUIDField(pk=True)
    name = CharField(max_length=1024)
    description = CharField(max_length=2048, default="")
    users:ManyToManyRelation[User]=ManyToManyField("models.User", related_name="organaizations", on_delete=fields.CASCADE)
    projects: ReverseRelation["Project"]

from .auth import Token
from .task import Project