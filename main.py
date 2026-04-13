from fastapi import FastAPI
from pydantic import BaseModel

# Create an instance with metadata
app = FastAPI(
    title="My First API",
    description="A simple API built with FastAPI",
    version="0.1.0",
    docs_url="/documentation",  # Change the docs URL (default: /docs)
    redoc_url="/redoc"          # Alternative docs (default: /redoc)
)

# Define a Pydantic model for request body validation
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

# Define a root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Define a path parameter endpoint with query parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Define a POST endpoint with request body
@app.post("/items")
def create_item(item: Item):
    return item