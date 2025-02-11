from fastapi import FastAPI
from routers import router

app = FastAPI()

# 統合したルーターを登録
app.include_router(router)
