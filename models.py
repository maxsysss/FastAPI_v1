from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class Book(BaseModel):
    id: UUID;
    title: str;
    author:str;
    year: int;
    description: Optional[str] = None;

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1);
    author: str = Field(..., min_length=1);
    year: int = Field(..., ge=0, le=2100);
    description: Optional[str] = Field(None, max_length=300);