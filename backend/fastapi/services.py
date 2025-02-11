from fastapi import HTTPException
from sqlalchemy import text
from database import engine

# --- 共通のヘルパー関数 ---
def execute_db_query(query: text, params: dict = None, commit: bool = False, fetch: str = "none"):
    """
    Execute a SQL query, optionally commit, and fetch results.
    
    :param query: SQL query string.
    :param params: Dictionary of parameters for the query.
    :param commit: Whether to commit the transaction.
    :param fetch: 'one' for single record, 'all' for all records, 'none' for no fetch.
    :return: Fetched result(s) if applicable.
    """
    with engine.connect() as conn:
        result = conn.execute(query, params or {})
        data = None
        if fetch == "one":
            data = result.fetchone()
        elif fetch == "all":
            data = result.fetchall()
        if commit:
            conn.commit()
    return data

# --- Category Functions ---
def create_category(name: str):
    # Insert a new category and return the created record.
    query = text("INSERT INTO categories (name) VALUES (:name) RETURNING *")
    category = execute_db_query(query, {"name": name}, commit=True, fetch="one")
    if category is None:
        raise HTTPException(status_code=500, detail="Category creation failed")
    return dict(category._mapping)

def list_categories():
    # Retrieve all categories.
    query = text("SELECT * FROM categories")
    categories = execute_db_query(query, fetch="all")
    return [dict(category._mapping) for category in categories]

def get_category(category_id: int):
    # Retrieve a category by its id.
    query = text("SELECT * FROM categories WHERE id = :id")
    category = execute_db_query(query, {"id": category_id}, fetch="one")
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return dict(category._mapping)

# --- User Functions ---
def create_user(name: str):
    # Insert a new user and return the created record.
    query = text("INSERT INTO users (name) VALUES (:name) RETURNING *")
    user = execute_db_query(query, {"name": name}, commit=True, fetch="one")
    if user is None:
        raise HTTPException(status_code=500, detail="User creation failed")
    return dict(user._mapping)

def list_users():
    # Retrieve all users.
    query = text("SELECT * FROM users")
    users = execute_db_query(query, fetch="all")
    return [dict(user._mapping) for user in users]

def get_user(user_id: int):
    # Retrieve a user by its id.
    query = text("SELECT * FROM users WHERE id = :id")
    user = execute_db_query(query, {"id": user_id}, fetch="one")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user._mapping)

# --- Micropost Functions ---
def create_micropost(content: str, user_id: int):
    # Insert a new micropost and associate it with a user.
    query = text("INSERT INTO microposts (content, user_id) VALUES (:content, :user_id) RETURNING *")
    micropost = execute_db_query(query, {"content": content, "user_id": user_id}, commit=True, fetch="one")
    if micropost is None:
        raise HTTPException(status_code=500, detail="Micropost creation failed")
    return dict(micropost._mapping)

def list_microposts():
    # Retrieve all microposts.
    query = text("SELECT * FROM microposts")
    microposts = execute_db_query(query, fetch="all")
    return [dict(micropost._mapping) for micropost in microposts]

def get_micropost(micropost_id: int):
    # Retrieve a micropost by its id.
    query = text("SELECT * FROM microposts WHERE id = :id")
    micropost = execute_db_query(query, {"id": micropost_id}, fetch="one")
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
    category = execute_db_query(query_category, {"id": category_id}, fetch="one")
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Verify if the specified micropost exists.
    query_micropost = text("SELECT * FROM microposts WHERE id = :id")
    micropost = execute_db_query(query_micropost, {"id": micropost_id}, fetch="one")
    if not micropost:
        raise HTTPException(status_code=404, detail="Micropost not found")

    # Create link between micropost and category.
    query_link = text("INSERT INTO micropost_categories (micropost_id, category_id) VALUES (:micropost_id, :category_id) RETURNING *")
    link = execute_db_query(query_link, {"micropost_id": micropost_id, "category_id": category_id}, commit=True, fetch="one")
    if link is None:
        raise HTTPException(status_code=500, detail="Link creation failed")
    return dict(link._mapping)

def list_micropost_category_links():
    # Retrieve all micropost-category links.
    query = text("SELECT * FROM micropost_categories")
    links = execute_db_query(query, fetch="all")
    return [dict(link._mapping) for link in links]

def get_categories_for_micropost(micropost_id: int):
    # Retrieve all categories associated with a specified micropost.
    query = text("""
        SELECT c.* FROM categories c 
        JOIN micropost_categories mc ON c.id = mc.category_id 
        WHERE mc.micropost_id = :micropost_id
    """)
    categories = execute_db_query(query, {"micropost_id": micropost_id}, fetch="all")
    return [dict(category._mapping) for category in categories]

def get_microposts_for_category(category_id: int):
    # Retrieve all microposts associated with a specified category.
    query = text("""
        SELECT m.* FROM microposts m 
        JOIN micropost_categories mc ON m.id = mc.micropost_id 
        WHERE mc.category_id = :category_id
    """)
    microposts = execute_db_query(query, {"category_id": category_id}, fetch="all")
    return [dict(micropost._mapping) for micropost in microposts]
