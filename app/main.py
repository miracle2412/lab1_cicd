from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Items REST API",
    description="REST API for CI/CD Laboratory Work №1",
    version="1.0.0"
)


class Item(BaseModel):
    name: str
    price: float


items = {
    1: {"name": "Laptop", "price": 1200.0},
    2: {"name": "Mouse", "price": 25.0}
}


@app.get("/")
def root():
    return {"message": "REST API is working"}


@app.get("/api/items")
def get_items():
    return items


@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    return items[item_id]


@app.post("/api/items", status_code=201)
def create_item(item: Item):
    new_id = max(items.keys(), default=0) + 1

    items[new_id] = {
        "name": item.name,
        "price": item.price
    }

    return {
        "id": new_id,
        **items[new_id]
    }


@app.put("/api/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    items[item_id] = {
        "name": item.name,
        "price": item.price
    }

    return {
        "id": item_id,
        **items[item_id]
    }


@app.delete("/api/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    deleted_item = items.pop(item_id)

    return {
        "message": "Item deleted",
        "item": deleted_item
    }