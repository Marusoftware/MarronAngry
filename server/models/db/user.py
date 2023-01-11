from tortoise.fields import UUIDField, CharField, BooleanField, ReverseRelation, ManyToManyRelation, ManyToManyField, ForeignKeyField
from tortoise.models import Model
from tortoise import Tortoise, fields

class User(Model):
    id = UUIDField(pk=True, description="User ID")
    name = CharField(max_length=1024, unique=True, index=True, description="User short name")
    fullname = CharField(max_length=1024, default="", description="User long name")
    is_dev = BooleanField(default=False, description="Is this user developer?")
    email = CharField(max_length=1024, description="User email")
    password = CharField(max_length=1024, null=True, description="User password")
    otp_key = CharField(max_length=32, null=True, description="OTP Secret Key")
    tokens:ReverseRelation["Token"]
    members:ReverseRelation["OrganizationMember"]

class Organization(Model):
    id = UUIDField(pk=True)
    name = CharField(max_length=1024)
    description = CharField(max_length=2048, default="")
    members:ReverseRelation["OrganizationMember"]
    projects: ReverseRelation["Project"]

class OrganizationMember(Model):
    id=UUIDField(pk=True)
    user=ForeignKeyField("models.User", related_name="members", on_delete=fields.CASCADE)
    is_admin=BooleanField(default=False)
    organization=ForeignKeyField("models.Organization", related_name="members", on_delete=fields.CASCADE)

from .auth import Token
from .task import Project