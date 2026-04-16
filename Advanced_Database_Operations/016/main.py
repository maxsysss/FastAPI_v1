from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)  # Create tables on startup

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user_with_items(db, user, ["Item A", "Item B"])


@app.get("/items/search", response_model=list[schemas.Item])
def search_items(keyword: str, db: Session = Depends(get_db)):
    return crud.search_items(db, keyword)

@app.get("/users/item-counts", response_model=list[schemas.UserItemCount])
def user_item_counts(db: Session = Depends(get_db)):
    return crud.get_user_item_counts(db)