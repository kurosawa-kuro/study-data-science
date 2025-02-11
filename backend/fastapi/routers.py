from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from database import engine
from pydantic import BaseModel

# 入力スキーマの定義
class CategoryInput(BaseModel):
    name: str

class UserInput(BaseModel):
    name: str

class MicropostInput(BaseModel):
    content: str
    user_id: int

class MicropostCategoryLinkInput(BaseModel):
    micropost_id: int
    category_id: int

router = APIRouter()

# --- Categories Endpoints ---
@router.post("/categories")
async def create_category(data: CategoryInput):
    # Create: Insert a new category and return the created record.
    query = text("INSERT INTO categories (name) VALUES (:name) RETURNING *")
    with engine.connect() as conn:
        result = conn.execute(query, {"name": data.name})
        category = result.fetchone()
        conn.commit()
    return dict(category._mapping)

@router.get("/categories")
async def list_categories():
    # Read All: Retrieve all categories.
    query = text("SELECT * FROM categories")
    with engine.connect() as conn:
        result = conn.execute(query)
        categories = result.fetchall()
    return [dict(category._mapping) for category in categories]

@router.get("/categories/{category_id}")
async def get_category(category_id: int):
    # Read One: Retrieve a category by its id.
    query = text("SELECT * FROM categories WHERE id = :id")
    with engine.connect() as conn:
        result = conn.execute(query, {"id": category_id})
        category = result.fetchone()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return dict(category._mapping)

# --- Users Endpoints ---
@router.post("/users")
async def create_user(data: UserInput):
    # Create: Insert a new user and return the created record.
    query = text("INSERT INTO users (name) VALUES (:name) RETURNING *")
    with engine.connect() as conn:
        result = conn.execute(query, {"name": data.name})
        user = result.fetchone()
        conn.commit()
    return dict(user._mapping)

@router.get("/users")
async def list_users():
    # Read All: Retrieve all users.
    query = text("SELECT * FROM users")
    with engine.connect() as conn:
        result = conn.execute(query)
        users = result.fetchall()
    return [dict(user._mapping) for user in users]

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    # Read One: Retrieve a user by its id.
    query = text("SELECT * FROM users WHERE id = :id")
    with engine.connect() as conn:
        result = conn.execute(query, {"id": user_id})
        user = result.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user._mapping)

# --- Microposts Endpoints ---
@router.post("/microposts")
async def create_micropost(data: MicropostInput):
    # Create: Insert a new micropost and associate it with a user.
    query = text("INSERT INTO microposts (content, user_id) VALUES (:content, :user_id) RETURNING *")
    with engine.connect() as conn:
        result = conn.execute(query, {"content": data.content, "user_id": data.user_id})
        micropost = result.fetchone()
        conn.commit()
    return dict(micropost._mapping)

@router.get("/microposts")
async def list_microposts():
    # Read All: Retrieve all microposts.
    query = text("SELECT * FROM microposts")
    with engine.connect() as conn:
        result = conn.execute(query)
        microposts = result.fetchall()
    return [dict(micropost._mapping) for micropost in microposts]

@router.get("/microposts/{micropost_id}")
async def get_micropost(micropost_id: int):
    # Read One: Retrieve a micropost by its id.
    query = text("SELECT * FROM microposts WHERE id = :id")
    with engine.connect() as conn:
        result = conn.execute(query, {"id": micropost_id})
        micropost = result.fetchone()
    if not micropost:
        raise HTTPException(status_code=404, detail="Micropost not found")
    return dict(micropost._mapping)

# --- Micropost-Categories Endpoints ---
@router.post("/micropost-categories")
async def link_micropost_category(data: MicropostCategoryLinkInput):
    # 事前に対象のmicropostとcategoryが存在するかチェックする
    with engine.connect() as conn:
        # Check if the specified category exists
        category_query = text("SELECT * FROM categories WHERE id = :id")
        category_result = conn.execute(category_query, {"id": data.category_id})
        category = category_result.fetchone()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        # Check if the specified micropost exists
        micropost_query = text("SELECT * FROM microposts WHERE id = :id")
        micropost_result = conn.execute(micropost_query, {"id": data.micropost_id})
        micropost = micropost_result.fetchone()
        if not micropost:
            raise HTTPException(status_code=404, detail="Micropost not found")
        # Link creation
        query = text("INSERT INTO micropost_categories (micropost_id, category_id) VALUES (:micropost_id, :category_id) RETURNING *")
        result = conn.execute(query, {"micropost_id": data.micropost_id, "category_id": data.category_id})
        link = result.fetchone()
        conn.commit()
    return dict(link._mapping)

@router.get("/micropost-categories")
async def list_micropost_category_links():
    # Read All: Retrieve all micropost-category links.
    query = text("SELECT * FROM micropost_categories")
    with engine.connect() as conn:
        result = conn.execute(query)
        links = result.fetchall()
    return [dict(link._mapping) for link in links]

@router.get("/micropost-categories/micropost/{micropost_id}")
async def get_categories_for_micropost(micropost_id: int):
    # Read: Retrieve all categories associated with a specified micropost.
    query = text("""
        SELECT c.* FROM categories c 
        JOIN micropost_categories mc ON c.id = mc.category_id 
        WHERE mc.micropost_id = :micropost_id
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"micropost_id": micropost_id})
        categories = result.fetchall()
    return [dict(category._mapping) for category in categories]

@router.get("/micropost-categories/category/{category_id}")
async def get_microposts_for_category(category_id: int):
    # Read: Retrieve all microposts associated with a specified category.
    query = text("""
        SELECT m.* FROM microposts m 
        JOIN micropost_categories mc ON m.id = mc.micropost_id 
        WHERE mc.category_id = :category_id
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"category_id": category_id})
        microposts = result.fetchall()
    return [dict(micropost._mapping) for micropost in microposts] 