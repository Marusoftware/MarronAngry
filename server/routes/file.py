from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends, UploadFile
from fastapi.responses import FileResponse

from ..upload import upload

from ..models.db.project import Project, OrganizationMember, File
from ..models.read.user import User
from ..security import get_user
import aiofiles.os, os

router=APIRouter(tags=["file"])

@router.trace("/{full_path:path}", response_model=List[str])
async def ls(prj_id:UUID, full_path:str, user:User=Depends(get_user)):
    prj=await Project.get(id=prj_id).prefetch_related("organization")
    if not await OrganizationMember.exists(organization=prj.organization, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    file=await File.get(id=prj.default_storage)
    return list(await aiofiles.os.scandir(os.path.join(file.path, full_path)))

@router.post("/{full_path:path}", response_model=None)
async def put(prj_id:UUID, full_path:str, user:User=Depends(get_user), file:UploadFile=None):
    prj=await Project.get(id=prj_id).prefetch_related("organization")
    if not await OrganizationMember.exists(organization=prj.organization, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    file_db=await File.get(id=prj.default_storage)
    await upload(prj, file, filename=full_path)

@router.get("/{full_path:path}", response_class=FileResponse, responses={200: {"content": {"*/*": {"schema": {"type": "string", "format": "binary"}}}}})
async def get(prj_id:UUID, full_path:str, user:User=Depends(get_user)):
    prj=await Project.get(id=prj_id).prefetch_related("organization")
    if not await OrganizationMember.exists(organization=prj.organization, user=user):
        raise HTTPException(status_code=400, detail="No permission to do it.")
    file=await File.get(id=prj.default_storage)
    return FileResponse(os.path.join(file.path, full_path))