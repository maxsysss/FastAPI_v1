## 2.4. Basic CRUD Operations

# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Usuario
from database import init_db
from deps import get_db
from pydantic import BaseModel

app = FastAPI()

# Run this once at startup
@app.on_event("startup")
async def on_startup():
    await init_db()

# Pydantic Schemas


class criarUsuario(BaseModel):
    nome: str
    email: str
    
class lerUsuario(BaseModel):
    id_usuario: int
    nome: str
    email: str
    class Config:
        from_attributes = True

# criar usuario
@app.post("/usuarios/", response_model=lerUsuario)
async def create_usuario(usuario: criarUsuario, db: AsyncSession = Depends(get_db)):
    db_usuario = Usuario(nome=usuario.nome, email=usuario.email)
    db.add(db_usuario)
    await db.commit()
    await db.refresh(db_usuario)
    return db_usuario

# ler usuarios
@app.get("/usuarios/", response_model=list[lerUsuario])
async def get_usuarios(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario))
    return result.scalars().all()
# Get usuario by ID
@app.get("/usuarios/{usuario_id}", response_model=lerUsuario)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.id_usuario == usuario_id))
    usuario = result.scalar_one_or_none()
    if usuario is None:
        raise HTTPException(status_code=404, detail="usuario not found")
    return usuario

# Delete user
@app.delete("/usuarios/{usuario_id}")
async def delete_user(usuario_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.id_usuario == usuario_id))
    usuario = result.scalar_one_or_none()
    if usuario is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(usuario)
    await db.commit()
    return {"message": "User deleted"}