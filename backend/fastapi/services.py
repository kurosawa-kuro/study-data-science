from fastapi import HTTPException
from sqlalchemy import text
from database import engine

# --- Category Functions ---
def create_category(name: str):
    # Insert a new category and return the created record.
    query = text("INSERT INTO categories (name) VALUES (:name) RETURNING *")
    with engine.connect() as conn:
        result = conn.execute(query, {"name": name})
        category = result.fetchone()
        conn.commit()
    if category is None:
        raise HTTPException(status_code=500, detail="Category creation failed")
    return dict(category._mapping)

def list_categories():
    # Retrieve all categories.
    query = text("SELECT * FROM categories")
    with engine.connect() as conn:
        result = conn.execute(query)
        categories = result.fetchall()
    return [dict(category._mapping) for category in categories]

def get_category(category_id: int):
    # Retrieve a category by its id.
    query = text("SELECT * FROM categories WHERE id = :id")
    with engine.connect() as conn:
        result = conn.execute(query, {"id": category_id})
        category = result.fetchone()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return dict(category._mapping)

# --- User Functions ---
def create_user(name: str):
    # Insert a new user and return the created record.
    query = text("INSERT INTO users (name) VALUES (:name) RETURNING *")
    with engine.connect() as conn:
        result = conn.execute(query, {"name": name})
        user = result.fetchone()
        conn.commit()
    if user is None:
        raise HTTPException(status_code=500, detail="User creation failed")
    return dict(user._mapping)

def list_users():
    # Retrieve all users.
    query = text("SELECT * FROM users")
    with engine.connect() as conn:
        result = conn.execute(query)
        users = result.fetchall()
    return [dict(user._mapping) for user in users]

def get_user(user_id: int):
    # Retrieve a user by its id.
    query = text("SELECT * FROM users WHERE id = :id")
    with engine.connect() as conn:
        result = conn.execute(query, {"id": user_id})
        user = result.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user._mapping)

# --- Micropost Functions ---
def create_micropost(content: str, user_id: int):
    # Insert a new micropost and associate it with a user.
    query = text("INSERT INTO microposts (content, user_id) VALUES (:content, :user_id) RETURNING *")
    with engine.connect() as conn:
        result = conn.execute(query, {"content": content, "user_id": user_id})
        micropost = result.fetchone()
        conn.commit()
    if micropost is None:
        raise HTTPException(status_code=500, detail="Micropost creation failed")
    return dict(micropost._mapping)

def list_microposts():
    # Retrieve all microposts.
    query = text("SELECT * FROM microposts")
    with engine.connect() as conn:
        result = conn.execute(query)
        microposts = result.fetchall()
    return [dict(micropost._mapping) for micropost in microposts]

def get_micropost(micropost_id: int):
    # Retrieve a micropost by its id.
    query = text("SELECT * FROM microposts WHERE id = :id")
    with engine.connect() as conn:
        result = conn.execute(query, {"id": micropost_id})
        micropost = result.fetchone()
    if not micropost:
        raise HTTPException(status_code=404, detail="Micropost not found")
    return dict(micropost._mapping)

# --- Micropost-Category Link Functions ---
def link_micropost_category(micropost_id: int, category_id: int):
    """
    Verify the existence of both micropost and category, then create a link record.
    """
    # Verify if the specified category exists.
    query_category = text("SELECT * FROM categories WHERE id = :id")
    with engine.connect() as conn:
        result_category = conn.execute(query_category, {"id": category_id})
        category = result_category.fetchone()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Verify if the specified micropost exists.
    query_micropost = text("SELECT * FROM microposts WHERE id = :id")
    with engine.connect() as conn:
        result_micropost = conn.execute(query_micropost, {"id": micropost_id})
        micropost = result_micropost.fetchone()
    if not micropost:
        raise HTTPException(status_code=404, detail="Micropost not found")

    # Create link between micropost and category.
    query_link = text("INSERT INTO micropost_categories (micropost_id, category_id) VALUES (:micropost_id, :category_id) RETURNING *")
    with engine.connect() as conn:
        result_link = conn.execute(query_link, {"micropost_id": micropost_id, "category_id": category_id})
        link = result_link.fetchone()
        conn.commit()
    if link is None:
        raise HTTPException(status_code=500, detail="Link creation failed")
    return dict(link._mapping)

def list_micropost_category_links():
    # Retrieve all micropost-category links.
    query = text("SELECT * FROM micropost_categories")
    with engine.connect() as conn:
        result = conn.execute(query)
        links = result.fetchall()
    return [dict(link._mapping) for link in links]

def get_categories_for_micropost(micropost_id: int):
    # Retrieve all categories associated with a specified micropost.
    query = text("""
        SELECT c.* FROM categories c 
        JOIN micropost_categories mc ON c.id = mc.category_id 
        WHERE mc.micropost_id = :micropost_id
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"micropost_id": micropost_id})
        categories = result.fetchall()
    return [dict(category._mapping) for category in categories]

def get_microposts_for_category(category_id: int):
    # Retrieve all microposts associated with a specified category.
    query = text("""
        SELECT m.* FROM microposts m 
        JOIN micropost_categories mc ON m.id = mc.micropost_id 
        WHERE mc.category_id = :category_id
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"category_id": category_id})
        microposts = result.fetchall()
    return [dict(micropost._mapping) for micropost in microposts]
