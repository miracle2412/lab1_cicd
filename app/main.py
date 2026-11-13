from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Item as ItemModel


app = FastAPI(
    title="Items REST API",
    description="REST API for CI/CD Laboratory Work №4",
    version="2.0.0"
)


class Item(BaseModel):
    name: str
    price: float


@app.get("/")
def root():
    return {"message": "REST API is working"}


@app.get("/api/items")
def get_items(db: Session = Depends(get_db)):
    items = db.query(ItemModel).order_by(ItemModel.id).all()

    # Сохраняем старый формат ответа для React:
    # {"1": {"name": "...", "price": ...}, ...}
    return {
        item.id: {
            "name": item.name,
            "price": item.price
        }
        for item in items
    }


@app.get("/api/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(ItemModel, item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "name": item.name,
        "price": item.price
    }


@app.post("/api/items", status_code=201)
def create_item(item: Item, db: Session = Depends(get_db)):
    db_item = ItemModel(
        name=item.name,
        price=item.price
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return {
        "id": db_item.id,
        "name": db_item.name,
        "price": db_item.price
    }


@app.put("/api/items/{item_id}")
def update_item(
    item_id: int,
    item: Item,
    db: Session = Depends(get_db)
):
    db_item = db.get(ItemModel, item_id)

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.name = item.name
    db_item.price = item.price

    db.commit()
    db.refresh(db_item)

    return {
        "id": db_item.id,
        "name": db_item.name,
        "price": db_item.price
    }


@app.delete("/api/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.get(ItemModel, item_id)

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    deleted_item = {
        "name": db_item.name,
        "price": db_item.price
    }

    db.delete(db_item)
    db.commit()

    return {
        "message": "Item deleted",
        "item": deleted_item
    }