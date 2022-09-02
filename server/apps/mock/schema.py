from typing import List, Union
from pydantic import BaseModel


class BaseItem(BaseModel):
    title: str
    description: Union[str, None] = None


class CreateItem(BaseItem):
    pass


class Item(BaseItem):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    email: str


class CreateUser(BaseUser):
    password: str


class User(BaseUser):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
