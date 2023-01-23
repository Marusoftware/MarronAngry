from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends

from ..security import get_user

from ..models.read.user import Member, Task
from ..models.db import Project, Organization, OrganizationMember, User, Task as TaskDB
from ..models.write import TaskCreate, TaskUpdate

router=APIRouter(tags=["task"])

@router.get("/", response_model=List[Task])
async def get(prj_id:UUID, user:User=Depends(get_user)):
    prj=await Project.get(id=prj_id).prefetch_related("organization")
    if not await OrganizationMember.exists(organization=prj.organization, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    return [{"id":task.id, "name":task.name, "description":task.description, "time":task.time, "project_id":prj.id, "members":[Member(id=member.id, is_admin=member.is_admin, user_id=member.user.id) for member in prj.members]} for task in  await TaskDB.filter(project=prj).prefetch_related("members__user")]

@router.post("/", response_model=Task)
async def create(task:TaskCreate, user:User=Depends(get_user)):
    prj=await Project.get(id=task.project_id).prefetch_related("organization")
    member=await OrganizationMember.get_or_none(organization=prj.organization, user=user)
    if member is None:
        raise HTTPException(status_code=400, detail="No permission to do it.")
    task_db=await TaskDB.create(name=task.name, description=task.description, project=prj)
    await task_db.members.add(member)
    return {**dict(task_db), "project_id":prj.id, "members":[Member(id=member.id, is_admin=member.is_admin, user_id=user.id)]}

@router.patch("/{task_id}", response_model=Task)
async def update(task_id:UUID, task:TaskUpdate, user:User=Depends(get_user)):
    prj=await Project.get(id=task.project_id).prefetch_related("organization")
    if not await OrganizationMember.exists(organization=prj.organization, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    proj=await TaskDB.get(id=task_id).prefetch_related("members__user")
    proj.update_from_dict(task.dict(exclude_none=True))
    await proj.save()
    return {**dict(proj), "project_id":prj.id, "members":[Member(id=member.id, is_admin=member.is_admin, user_id=member.user.id) for member in proj.members]}

@router.delete("/{task_id}")
async def delete(task_id:UUID, user:User=Depends(get_user)):
    task=await TaskDB.get(id=task_id).prefetch_related("project__organization")
    if not await OrganizationMember.exists(organization=task.project.organization, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    await task.delete()