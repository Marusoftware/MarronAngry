from tortoise.fields import UUIDField, CharField, DatetimeField, ForeignKeyField, ReverseRelation
from tortoise.models import Model
from tortoise import fields

class Project(Model):
    id=UUIDField(pk=True)
    name=CharField(max_length=1024)
    description=CharField(max_length=2048, default="")
    organization=ForeignKeyField("models.Organization", related_name="projects", on_delete=fields.CASCADE)
    tasks:ReverseRelation["Task"]

class Task(Model):
    id=UUIDField(pk=True)
    name=CharField(max_length=1024)
    description=CharField(max_length=2048, default="")
    time=DatetimeField(auto_now_add=True)
    project= ForeignKeyField("models.Project", related_name="tasks", on_delete=fields.CASCADE)