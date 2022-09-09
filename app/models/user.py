from enum import IntEnum
from typing import Optional
from pydantic import EmailStr
from datetime import datetime
from sqlmodel import SQLModel, Field


class Status(IntEnum):
    enable = 1
    disable = 0


class Role(IntEnum):
    root = 0
    admin = 1
    common = 2


class UserBase(SQLModel):
    name: str = Field(min_length=2, max_length=20, regex=r"^[a-zA-Z0-9 \-_]*$")
    email: EmailStr = Field(unique=True)
    role: Role = Role.common
    status: Status = Status.enable


class UserCreate(UserBase):
    password: str


class UserInfo(UserBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    creator: int = 0


class User(UserCreate, UserInfo, table=True):
    created: datetime = datetime.utcnow()
    updated: datetime = datetime.utcnow()


class ResetPwd(SQLModel):
    password: str
