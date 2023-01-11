from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from ..security import get_user
from ..models.write import OrganizationCreate
from ..models.db import Organization as OrganizationDB, OrganizationMember, User as UserDB
from ..models.read.user import Organization, Member

router=APIRouter(tags=["organization"])

@router.post("/", response_model=Organization)
async def create(organization:OrganizationCreate, user:get_user=Depends()):
    org=await OrganizationDB.create(**organization.dict())
    mem=await OrganizationMember.create(user=user, is_admin=True, organization=org)
    mem=Member(id=mem.id, is_admin=mem.is_admin, user_id=user.id)
    org=Organization(id=org.id, name=org.name, description=org.description, members=[mem])
    return org

@router.get("/", response_model=List[Organization])
async def get_us(user:get_user=Depends()):
    orgs=[]
    for me in await OrganizationMember.filter(user=user).prefetch_related("organization__members__user"):
        orgs.append(Organization(id=me.organization.id, name=me.organization.name, description=me.organization.description, members=[
            Member(id=member.id, is_admin=member.is_admin, user_id=member.user.id) async for member in me.organization.members
        ]))
    return orgs

@router.post("/{org_id}/user")
async def add_user(org_id:UUID, user_id:UUID, user:get_user=Depends()):
    organization=await OrganizationDB.get(id=org_id)
    if not await organization.members.filter(user=user, is_admin=True).exists():
        raise HTTPException(status_code=400, detail="No permission to do it.")
    await OrganizationMember.create(user=await UserDB.get(id=user_id), organization=organization)

@router.delete("/{org_id}/")
async def delete(org_id:UUID, user:get_user=Depends()):
    organization=await OrganizationDB.get(id=org_id)
    if not await organization.members.filter(user=user, is_admin=True).exists():
        raise HTTPException(status_code=400, detail="No permission to do it.")
    await organization.delete()
    