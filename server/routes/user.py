from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from ..security import get_user
from ..models.read.user import User, UserOpen
from ..models.write import UserUpdate
from ..models.db import User as UserDB, Project as ProjectDB, File as FileDB
from .auth.passwd import crypt
from ..upload import upload
import mimetypes, os

router=APIRouter(tags=["user"])

@router.put("/logo", response_model=bool)
async def set_logo(user:UserDB=Depends(get_user), image:UploadFile=None):
    if not image.content_type in ["image/png","image/jpeg"]:
        raise HTTPException(500, "File type is not allowed.")
    user.logo=(await upload(proj=await ProjectDB.get(name=user.name).prefetch_related("organization"), file=image, id=user.logo, filename=".logo"+os.path.splitext(image.filename)[1])).id
    await user.save()
    return True

@router.get("/logo/me", response_class=FileResponse, responses={200: {"content": {"image/*": {"schema": {"type": "string", "format": "binary"}}}}})
async def me_logo(user:UserDB=Depends(get_user)):
    if user.logo is None:
        raise HTTPException(404, "")
    else:
        path=(await FileDB.get(id=user.logo)).path
        return FileResponse(path, media_type=mimetypes.guess_type(path)[0])

@router.get("/logo/{id}", response_class=FileResponse, responses={200: {"content": {"image/*": {"schema": {"type": "string", "format": "binary"}}}}})
async def get_logo(id:UUID):
    user=await UserDB.get(id=id)
    if user.logo is None:
        raise HTTPException(404, "")
    else:
        path=(await FileDB.get(id=user.logo)).path
        return FileResponse(path, media_type=mimetypes.guess_type(path)[0])

@router.get("/me", response_model=User)
async def me(user:UserDB=Depends(get_user)):
    return user

@router.get("/{id}", response_model=UserOpen)
async def get(id:UUID):
    return await UserDB.get(id=id)

@router.delete("/me")
async def delete_me(user:UserDB=Depends(get_user), password:str=None):
    if user.password is not None and password is None:
        raise HTTPException(status_code=400, detail="Password is wrong")
    if user.password is not None:
        if not crypt.verify(password, user.password):
            raise HTTPException(status_code=400, detail="Password is wrong")
    await user.delete()

@router.patch("/me", response_model=User)
async def update_me(user:UserUpdate, user_db:UserDB=Depends(get_user)):
    update_dict=user.dict()
    if (user.oldPassword is not None and user.newPassword is not None):
        if crypt.verify(user.oldPassword, user_db.password):
            update_dict["password"]=crypt.hash(user.newPassword)
    elif user_db.password is None and user.newPassword is not None:
        update_dict["password"]=crypt.hash(user.newPassword)
    def checkUpdate(item):
        key, value=item
        if key in ["oldPassword", "newPassword"]:
            return False
        elif value is None:
            return False
        else:
            return True
    update_dict=dict(filter(checkUpdate, update_dict.items()))
    user_db.update_from_dict(update_dict)
    await user_db.save()
    return user_db