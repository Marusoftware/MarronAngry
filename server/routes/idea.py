from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends

from ..security import get_user

from ..models.read.user import Member, Idea
from ..models.db import Project, OrganizationMember, User, Idea as IdeaDB
from ..models.write import IdeaCreate, IdeaUpdate
from datetime import datetime, timedelta

router=APIRouter(tags=["idea"])

@router.get("/", response_model=List[Idea])
async def get(prj_id:UUID, user:User=Depends(get_user)):
    prj=await Project.get(id=prj_id).prefetch_related("organization")
    if not await OrganizationMember.exists(organization=prj.organization, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    return [{"id":idea.id, "name":idea.name, "description":idea.description, "project_id":prj.id} for idea in await IdeaDB.filter(project=prj)]

@router.post("/", response_model=Idea)
async def create(idea:IdeaCreate, user:User=Depends(get_user)):
    prj=await Project.get(id=idea.project_id).prefetch_related("organization")
    if not await OrganizationMember.exists(organization=prj.organization, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    idea_db=await IdeaDB.create(name=idea.name, description=idea.description, project=prj)
    return {**dict(idea_db), "project_id":prj.id}

@router.patch("/{idea_id}", response_model=Idea)
async def update(idea_id:UUID, idea:IdeaUpdate, user:User=Depends(get_user)):
    prj=await Project.get(id=idea.project_id).prefetch_related("organization")
    if not await OrganizationMember.exists(organization=prj.organization, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    proj=await IdeaDB.get(id=idea_id)
    proj.update_from_dict(idea.dict(exclude_none=True))
    await proj.save()
    return {**dict(proj), "project_id":prj.id}

@router.delete("/{idea_id}")
async def delete(idea_id:UUID, user:User=Depends(get_user)):
    idea=await IdeaDB.get(id=idea_id).prefetch_related("project__organization")
    if not await OrganizationMember.exists(organization=idea.project.organization, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    await idea.delete()