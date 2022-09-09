import aiofiles
from uuid import uuid4
from typing import List
from pathlib import Path
from const import STORAGE_PATH
from models import File, FileInfo, User
from dependencies.auth import get_current_user
from fastapi import APIRouter, UploadFile, Depends
from dependencies.database import Session, get_session, select


router = APIRouter(prefix="/file", tags=["Files"], dependencies=[Depends(get_current_user)])


@router.post("/upload", response_model=List[File])
async def upload_file(files: List[UploadFile], session: Session = Depends(get_session), user: User = Depends(get_current_user)):

    upload_files = []

    for file in files:
        id = uuid4()
        suffix = ".".join(Path(file.filename).suffixes)
        path = f"{STORAGE_PATH}/{id}{suffix}"

        async with aiofiles.open(path, "wb") as f:
            while data := await file.read(1024):
                await f.write(data)

        file = File(id=id, name=file.filename, type=file.content_type, path=path, creator=user.id)

        session.add(file)
        session.commit()
        session.refresh(file)

        upload_files.append(file)

    return upload_files


@router.get("/", response_model=List[FileInfo])
async def get_file(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):

    files = session.exec(
        select(File.id, File.name, File.type, File.path, File.creator, File.created, User.email)
        .where(File.creator == User.id)
        .offset(offset)
        .limit(limit)
    ).all()

    return files
