from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="FastAPI Example")


class ItemIn(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class Item(ItemIn):
    id: int


items: Dict[int, Item] = {}
next_id = 1


@app.get("/")
def root():
    return {"message": "Hello, FastAPI"}


@app.get("/items", response_model=List[Item])
def list_items():
    return list(items.values())


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemIn):
    global next_id
    new_item = Item(id=next_id, **item.model_dump())
    items[next_id] = new_item
    next_id += 1
    return new_item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemIn):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = Item(id=item_id, **item.model_dump())
    return items[item_id]


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]


# Run with: uvicorn app:app --reload
