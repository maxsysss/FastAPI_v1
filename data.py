from models import Book
from uuid import uuid4

fake_db = {};

#Add one book to start
book_id = uuid4()
fake_db[book_id] = Book(
    id=book_id,
    title="1984",
    author="Geroge Orwell",
    year=1949,
    description="Dystopian novel"
)