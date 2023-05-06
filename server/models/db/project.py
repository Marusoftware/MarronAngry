from tortoise.fields import UUIDField, CharField, DatetimeField, ForeignKeyField, ReverseRelation, ForeignKeyRelation, ManyToManyField, ManyToManyRelation, BigIntField, TextField, BooleanField, OneToOneNullableRelation, OneToOneField
from tortoise.models import Model
from tortoise import fields

class Project(Model):
    id=UUIDField(pk=True, description="Project ID")
    name=CharField(max_length=1024, description="Project name")
    description=CharField(max_length=2048, default="", description="Project description")
    members:ManyToManyRelation["OrganizationMember"]=ManyToManyField("models.OrganizationMember", related_name="projects", on_delete=fields.CASCADE)
    organization:ForeignKeyRelation["Organization"]=ForeignKeyField("models.Organization", related_name="projects", on_delete=fields.CASCADE)
    logo=UUIDField(null=True)
    tasks:ReverseRelation["Task"]
    ideas:ReverseRelation["Idea"]
    files:ReverseRelation["File"]

class Task(Model):
    id=UUIDField(pk=True, description="Task ID")
    name=CharField(max_length=1024, description="Task name")
    description=TextField(default="", description="Task description")
    time=DatetimeField(auto_now_add=True, description="When will task finish?")
    members:ManyToManyRelation["OrganizationMember"]=ManyToManyField("models.OrganizationMember", related_name="tasks", on_delete=fields.CASCADE)
    project:ForeignKeyRelation[Project]= ForeignKeyField("models.Project", related_name="tasks", on_delete=fields.CASCADE)

class Idea(Model):
    id=UUIDField(pk=True, description="Idea ID")
    name=CharField(max_length=1024)
    description=TextField(default="")
    project:ForeignKeyRelation[Project]= ForeignKeyField("models.Project", related_name="ideas", on_delete=fields.CASCADE)
    
class File(Model):
    id=UUIDField(pk=True, description="File ID")
    size=BigIntField()
    path=CharField(max_length=1024)
    is_dir=BooleanField()
    project:ForeignKeyRelation[Project]= ForeignKeyField("models.Project", related_name="files", on_delete=fields.CASCADE)


from .user import Organization, OrganizationMember