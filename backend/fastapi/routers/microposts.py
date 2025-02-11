from fastapi import APIRouter, HTTPException
from database import engine
from sqlalchemy import text

router = APIRouter()

@router.post("/")
async def create_micropost(content: str, user_id: int):
    query = text("INSERT INTO microposts (content, user_id) VALUES (:content, :user_id) RETURNING *")
    with engine.connect() as conn:
        result = conn.execute(query, {"content": content, "user_id": user_id})
        micropost = result.fetchone()
        conn.commit()
    return dict(micropost._mapping)

@router.get("/{micropost_id}")
async def get_micropost(micropost_id: int):
    query = text("SELECT * FROM microposts WHERE id = :id")
    with engine.connect() as conn:
        result = conn.execute(query, {"id": micropost_id})
        micropost = result.fetchone()
    if not micropost:
        raise HTTPException(status_code=404, detail="Micropost not found")
    return dict(micropost._mapping)
