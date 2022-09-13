import os
import aiofiles
from uuid import uuid4
from typing import List
from pathlib import Path
from const import STORAGE_PATH
from models import File, FileInfo, User
from fastapi.responses import FileResponse
from dependencies.auth import get_current_user
from dependencies.database import Session, get_session, select
from fastapi import APIRouter, UploadFile, HTTPException, status, Depends, Query


router = APIRouter(prefix="/file", tags=["Files"], dependencies=[Depends(get_current_user)])


@router.post("/upload", response_model=List[File])
async def upload_file(files: List[UploadFile], session: Session = Depends(get_session), user: User = Depends(get_current_user)):

    upload_files = []

    for file in files:
        id = str(uuid4())
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


@router.get("/{id}", response_model=File)
async def get_file(id: str, session: Session = Depends(get_session)):

    file = session.get(File, id)

    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid File ID {id}")

    return file


@router.get("/{id}/download")
async def download_file(id: str, session: Session = Depends(get_session)):

    file = session.get(File, id)

    if not Path(file.path).exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid File ID {id}")

    return FileResponse(file.path, media_type="application/octet-stream", filename=file.name)


@router.get("/", response_model=List[FileInfo])
async def get_files(
    offset: int = Query(default=0, ge=0), limit: int = Query(default=10, ge=0), session: Session = Depends(get_session)
):

    files = session.exec(
        select(File.id, File.name, File.type, File.path, File.creator, File.created, User.email)
        .where(File.creator == User.id)
        .offset(offset)
        .limit(limit)
    ).all()

    return files


@router.delete("/{id}")
async def delete_file(id: str, session: Session = Depends(get_session)):

    file = session.get(File, id)

    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid File ID {id}")

    # delete DB data
    session.delete(file)
    session.commit()

    # delete server file
    os.remove(file.path)

    return {"detail": "success"}
