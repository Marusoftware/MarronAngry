from tortoise.fields import UUIDField, CharField, BooleanField, ReverseRelation, ForeignKeyField, ForeignKeyRelation, ManyToManyRelation, CharEnumField
from tortoise.models import Model
from tortoise import fields
from enum import Enum

class OTPStatus(Enum):
    inactive="inactive"
    verify="verify"
    working="working"
    recovered="recovered"

class User(Model):
    id = UUIDField(pk=True, description="User ID")
    name = CharField(max_length=1024, description="User short name")
    is_dev = BooleanField(default=False, description="Is this user developer?")
    email = CharField(max_length=1024, description="User email")
    password = CharField(max_length=1024, null=True, description="User password")
    otp_key = CharField(max_length=32, null=True, description="OTP Secret Key")
    otp_recovery = CharField(max_length=(6+1)*12, null=True, description="OTP Recovery Key")
    otp_status = CharEnumField(OTPStatus, default=OTPStatus.inactive.value)
    tokens:ReverseRelation["Token"]
    members:ReverseRelation["OrganizationMember"]

class Organization(Model):
    id = UUIDField(pk=True, description="Organization ID")
    name = CharField(max_length=1024, description="Organization Name")
    description = CharField(max_length=2048, default="", description="Organization description")
    members:ReverseRelation["OrganizationMember"]
    projects: ReverseRelation["Project"]

class OrganizationMember(Model):
    id=UUIDField(pk=True, description="Organization Member ID")
    user:ForeignKeyRelation[User]=ForeignKeyField("models.User", related_name="members", on_delete=fields.CASCADE)
    is_admin=BooleanField(default=False, description="Is this Org member admin?")
    organization:ForeignKeyRelation[Organization]=ForeignKeyField("models.Organization", related_name="members", on_delete=fields.CASCADE)
    projects:ManyToManyRelation["Project"]
    tasks:ManyToManyRelation["Task"]

from .auth import Token
from .task import Project, Task