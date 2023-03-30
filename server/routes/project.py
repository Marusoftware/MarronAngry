from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends

from ..security import get_user

from ..models.response.user import Project, Member
from ..models.db import Project as ProjectDB, Organization, OrganizationMember, User
from ..models.request import ProjectCreate, ProjectUpdate

router=APIRouter(tags=["project"])

@router.get("/", response_model=List[Project])
async def get(org_id:UUID, user:User=Depends(get_user)):
    org=await Organization.get(id=org_id)
    if not await OrganizationMember.exists(organization=org, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    return [{"id":project.id, "name":project.name, "description":project.description, "organization_id":org_id, "members":[Member(id=member.id, is_admin=member.is_admin, user_id=member.user.id) for member in project.members]} for project in  await ProjectDB.filter(organization=org).prefetch_related("members__user")]

@router.post("/", response_model=Project)
async def create(project:ProjectCreate, user:User=Depends(get_user)):
    org=await Organization.get(id=project.organization_id)
    member=await OrganizationMember.get_or_none(organization=org, user=user, is_admin=True)
    if member is None:
        raise HTTPException(status_code=400, detail="No permission to do it.")
    project_db=await ProjectDB.create(name=project.name, description=project.description, organization=org)
    await project_db.members.add(member)
    return {**dict(project_db), "organization_id":project.organization_id, "members":[Member(id=member.id, is_admin=member.is_admin, user_id=user.id)]}

@router.put("/{proj_id}/user", response_model=Member)
async def add_user(proj_id:UUID, user_id:UUID, user:User=Depends(get_user)):
    proj=await ProjectDB.get(id=proj_id).prefetch_related("organization")
    if not await OrganizationMember.exists(organization=proj.organization, user=user, is_admin=True) and user_id!=user.id:
        raise HTTPException(status_code=400, detail="No permission to do it.")
    member=await OrganizationMember.get(user=await User.get(id=user_id), organization=proj.organization)
    await proj.members.add(member)
    return member

@router.delete("/{proj_id}/user", response_model=Member)
async def del_user(proj_id:UUID, user_id:UUID, user:User=Depends(get_user)):
    proj=await ProjectDB.get(id=proj_id).prefetch_related("organization")
    if not await OrganizationMember.exists(organization=proj.organization, user=user, is_admin=True) and user_id!=user.id:
        raise HTTPException(status_code=400, detail="No permission to do it.")
    member=await OrganizationMember.get(user=await User.get(id=user_id), organization=proj.organization)
    await proj.members.remove(member)
    return member

@router.patch("/{proj_id}", response_model=Project)
async def update(proj_id:UUID, project:ProjectUpdate, user:User=Depends(get_user)):
    org=await Organization.get(id=project.organization_id)
    if not await OrganizationMember.exists(organization=org, user=user, is_admin=True):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    proj=await ProjectDB.get(id=proj_id).prefetch_related("members__user")
    proj.update_from_dict(project.dict(exclude_none=True))
    await proj.save()
    return {**dict(proj), "organization_id":project.organization_id, "members":[Member(id=member.id, is_admin=member.is_admin, user_id=member.user.id) for member in proj.members]}

@router.delete("/{proj_id}")
async def delete(proj_id:UUID, user:User=Depends(get_user)):
    proj=await ProjectDB.get(id=proj_id).prefetch_related("organization")
    if not await OrganizationMember.exists(organization=proj.organization, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    await proj.delete()