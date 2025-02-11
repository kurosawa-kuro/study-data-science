from fastapi import FastAPI
from routers import users, microposts, categories, micropost_categories

app = FastAPI()

# ルーター登録
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(microposts.router, prefix="/microposts", tags=["Microposts"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(micropost_categories.router, prefix="/micropost-categories", tags=["Micropost-Categories"])
