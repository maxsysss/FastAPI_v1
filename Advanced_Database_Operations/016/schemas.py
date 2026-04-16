from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase): pass

class Item(ItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase): pass

class User(UserBase):
    id: int
    items: List[Item] = []
    model_config = ConfigDict(from_attributes=True)

class UserItemCount(BaseModel):
    name: str
    item_count: int