from fastapi import FastAPI;
from pydantic import BaseModel

# Create an instance of the FastAPI class
app = FastAPI();

#Define a Pydantic model for request body validation
class Item(BaseModel):
    name: str;
    price: float;
    is_offer: bool = None;

# Define a root endpoint
@app.get("/")
def read_root():
    return {"Message": "Hello World"};

# Define a path parameter endpoint
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
