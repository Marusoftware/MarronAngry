from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends

from ..security import get_user

from ..models.read.user import Project
from ..models.db import Project as ProjectDB, Organization, OrganizationMember, User
from ..models.write import ProjectCreate, ProjectUpdate

router=APIRouter(tags=["project"])

@router.get("/", response_model=List[Project])
async def get(org_id:UUID, user:User=Depends(get_user)):
    org=await Organization.get(id=org_id)
    if not await OrganizationMember.exists(organization=org, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    return {**dict(await ProjectDB.filter(organization=org))}

@router.post("/", response_model=Project)
async def create(project:ProjectCreate, user:User=Depends(get_user)):
    org=await Organization.get(id=project.organization_id)
    if not await OrganizationMember.exists(organization=org, user=user, is_admin=True):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    return {**dict(await ProjectDB.create(name=project.name, description=project.description, organization=await Organization.get(id=project.organization_id))), "organization_id":project.organization_id}

@router.patch("/{proj_id}")
async def update(proj_id:UUID, project:ProjectUpdate, user:User=Depends(get_user)):
    org=await Organization.get(id=project.organization_id)
    if not await OrganizationMember.exists(organization=org, user=user, is_admin=True):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    proj=await ProjectDB.get(id=proj_id)
    proj.update_from_dict(project.dict(exclude_none=True))
    await proj.save()
    return proj

@router.delete("/{proj_id}")
async def delete(proj_id:UUID, user:User=Depends(get_user)):
    proj=await ProjectDB.get(id=proj_id)
    if not await OrganizationMember.exists(organization=proj.organization, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    await proj.delete()