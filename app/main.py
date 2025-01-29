from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import product, transaction
from app.database import engine, Base

# データベースの初期化
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORSの設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # * はすべてのドメインを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

# ルーターを登録
app.include_router(product.router, prefix="/api", tags=["products"])
app.include_router(transaction.router, prefix="/api", tags=["transactions"])

