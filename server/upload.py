from fastapi import UploadFile, HTTPException
from .models.db import Project, File
from uuid import UUID
import aiofiles.os, os
from .config import Settings
config=Settings()

async def upload(proj:Project, file:UploadFile ,id:UUID=None, filename:str=None, size_limit:int=2048*1024):
    if id is None:
        file_model=await File.create(project=proj, is_dir=False, path="", size=0)
        id=file_model.id
    else:
        file_model=await File.get(id=id)
    if filename is None:
        filename=id
    filename=os.path.join(config.storage, str(proj.organization.id), str(proj.id), filename)
    await aiofiles.os.makedirs(os.path.dirname(filename), exist_ok=True)
    if file_model.is_dir:
        if await aiofiles.os.path.exists(filename):
            size_limit=size_limit-file_model.size+await aiofiles.os.path.getsize(filename)
        else:
            size_limit=size_limit-file_model.size
    else:
        file_model.path=filename
    size=0
    async with aiofiles.open(filename, "wb") as upfile:
        while content := await file.read(1024):
            size+=1024
            if size>=size_limit:
                raise HTTPException(402, "File is too large.")
            await upfile.write(content)
    file_model.size+=size
    await file_model.save()
    return file_model