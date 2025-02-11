from fastapi import APIRouter, HTTPException
from database import engine
from sqlalchemy import text

router = APIRouter()

@router.post("/")
async def link_micropost_category(micropost_id: int, category_id: int):
    query = text("INSERT INTO micropost_categories (micropost_id, category_id) VALUES (:micropost_id, :category_id) RETURNING *")
    with engine.connect() as conn:
        result = conn.execute(query, {"micropost_id": micropost_id, "category_id": category_id})
        link = result.fetchone()
        conn.commit()
    return dict(link._mapping)

@router.get("/micropost/{micropost_id}")
async def get_categories_for_micropost(micropost_id: int):
    query = text("""
        SELECT c.* FROM categories c 
        JOIN micropost_categories mc ON c.id = mc.category_id 
        WHERE mc.micropost_id = :micropost_id
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"micropost_id": micropost_id})
        categories = result.fetchall()
    return [dict(category._mapping) for category in categories]

@router.get("/category/{category_id}")
async def get_microposts_for_category(category_id: int):
    query = text("""
        SELECT m.* FROM microposts m 
        JOIN micropost_categories mc ON m.id = mc.micropost_id 
        WHERE mc.category_id = :category_id
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"category_id": category_id})
        microposts = result.fetchall()
    return [dict(micropost._mapping) for micropost in microposts]
