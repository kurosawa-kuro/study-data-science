from fastapi import APIRouter
from pydantic import BaseModel
import services

# Input schema definitions
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
    # Utilize services.py function for creating a category.
    return services.create_category(data.name)

@router.get("/categories")
async def list_categories():
    # Utilize services.py function for listing categories.
    return services.list_categories()

@router.get("/categories/{category_id}")
async def get_category(category_id: int):
    # Utilize services.py function for retrieving a category.
    return services.get_category(category_id)

# --- Users Endpoints ---
@router.post("/users")
async def create_user(data: UserInput):
    # Utilize services.py function for creating a user.
    return services.create_user(data.name)

@router.get("/users")
async def list_users():
    # Utilize services.py function for listing users.
    return services.list_users()

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    # Utilize services.py function for retrieving a user.
    return services.get_user(user_id)

# --- Microposts Endpoints ---
@router.post("/microposts")
async def create_micropost(data: MicropostInput):
    # Utilize services.py function for creating a micropost.
    return services.create_micropost(data.content, data.user_id)

@router.get("/microposts")
async def list_microposts():
    # Utilize services.py function for listing microposts.
    return services.list_microposts()

@router.get("/microposts/{micropost_id}")
async def get_micropost(micropost_id: int):
    # Utilize services.py function for retrieving a micropost.
    return services.get_micropost(micropost_id)

# --- Micropost-Categories Endpoints ---
@router.post("/micropost-categories")
async def link_micropost_category(data: MicropostCategoryLinkInput):
    # Utilize services.py function for linking a micropost and category.
    return services.link_micropost_category(data.micropost_id, data.category_id)

@router.get("/micropost-categories")
async def list_micropost_category_links():
    # Utilize services.py function for listing all micropost-category links.
    return services.list_micropost_category_links()

@router.get("/micropost-categories/micropost/{micropost_id}")
async def get_categories_for_micropost(micropost_id: int):
    # Utilize services.py function for retrieving categories for a micropost.
    return services.get_categories_for_micropost(micropost_id)

@router.get("/micropost-categories/category/{category_id}")
async def get_microposts_for_category(category_id: int):
    # Utilize services.py function for retrieving microposts for a category.
    return services.get_microposts_for_category(category_id) 