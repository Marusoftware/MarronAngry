from tortoise.fields import UUIDField, CharField, DatetimeField, ForeignKeyField, ReverseRelation, ForeignKeyRelation
from tortoise.models import Model
from tortoise import fields

class Project(Model):
    id=UUIDField(pk=True, description="Project ID")
    name=CharField(max_length=1024, description="Project name")
    description=CharField(max_length=2048, default="", description="Project description")
    organization:ForeignKeyRelation["Organization"]=ForeignKeyField("models.Organization", related_name="projects", on_delete=fields.CASCADE)
    tasks:ReverseRelation["Task"]

class Task(Model):
    id=UUIDField(pk=True, description="Task ID")
    name=CharField(max_length=1024, description="Task name")
    description=CharField(max_length=2048, default="", description="Task description")
    time=DatetimeField(auto_now_add=True, description="When will task finish?")
    project:ForeignKeyRelation[Project]= ForeignKeyField("models.Project", related_name="tasks", on_delete=fields.CASCADE)

from .user import Organization