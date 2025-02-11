from fastapi import APIRouter, HTTPException
from database import engine
from sqlalchemy import text

router = APIRouter()

@router.post("/")
async def create_category(name: str):
    query = text("INSERT INTO categories (name) VALUES (:name) RETURNING *")
    with engine.connect() as conn:
        result = conn.execute(query, {"name": name})
        category = result.fetchone()
        conn.commit()
    return dict(category._mapping)

@router.get("/{category_id}")
async def get_category(category_id: int):
    query = text("SELECT * FROM categories WHERE id = :id")
    with engine.connect() as conn:
        result = conn.execute(query, {"id": category_id})
        category = result.fetchone()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return dict(category._mapping)
