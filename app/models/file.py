from uuid import UUID
from enum import IntEnum
from datetime import datetime
from sqlmodel import SQLModel, Field


class FileType(IntEnum):
    text = 0
    image = 1
    video = 2
    audio = 3


class File(SQLModel, table=True):
    id: UUID = Field(primary_key=True)
    name: str
    type: str
    path: str
    creator: int = Field(foreign_key="user.id")
    created: datetime = datetime.utcnow()


class FileInfo(File, table=False):
    email: str
