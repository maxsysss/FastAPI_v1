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
    title: str = Field(..., min_length=1)      # Título: obrigatório, mínimo 1 caractere
    author: str = Field(..., min_length=1)     # Autor: obrigatório, mínimo 1 caractere
    year: int = Field(..., ge=0, le=2100)      # Ano: obrigatório, entre 0 e 2100
    description: Optional[str] = Field(None, max_length=300)  # Descrição: opcional, máximo 300