from fastapi import APIRouter, HTTPException
from database import engine
from sqlalchemy import text

router = APIRouter()

@router.post("/")
async def create_user(name: str):
    query = text("INSERT INTO users (name) VALUES (:name) RETURNING *")
    with engine.connect() as conn:
        result = conn.execute(query, {"name": name})
        user = result.fetchone()
        conn.commit()
    return dict(user._mapping)

@router.get("/{user_id}")
async def get_user(user_id: int):
    query = text("SELECT * FROM users WHERE id = :id")
    with engine.connect() as conn:
        result = conn.execute(query, {"id": user_id})
        user = result.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user._mapping)
