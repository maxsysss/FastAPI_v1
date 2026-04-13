# main.py — FastAPI Core Logic

from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4
from typing import List
from models import Book, BookCreate
from data import fake_db

app = FastAPI()

@app.get("/books", response_model=List[Book])
def get_books():
    return list(fake_db.values())

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: UUID):
    book = fake_db.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=Book, status_code=201)
def create_book(book: BookCreate):
    book_id = uuid4()
    new_book = Book(id=book_id, **book.model_dump())
    fake_db[book_id] = new_book
    return new_book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: UUID, book_data: BookCreate):
    if book_id not in fake_db:
        raise HTTPException(status_code=404, detail="Book not found")
    updated_book = Book(id=book_id, **book_data.model_dump())
    fake_db[book_id] = updated_book
    return updated_book

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: UUID):
    if book_id not in fake_db:
        raise HTTPException(status_code=404, detail="Book not found")
    del fake_db[book_id]