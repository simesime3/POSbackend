from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import product, transaction, transaction_detail
from app.database import engine, Base, engine_async

# データベースの初期化
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORSの設定を追加
origins = [
    "https://tech0-gen8-step4-pos-app-97.azurewebsites.net",  # 実際のフロントエンドドメイン
    "https://tech0-gen8-step4-pos-app-98.azurewebsites.net",
    "http://localhost:3000",  # ローカル開発用
    # 必要に応じて他のドメインを追加
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 許可するドメインを指定
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

# ルーターを登録
app.include_router(product.router, prefix="/api", tags=["products"])
app.include_router(transaction.router, prefix="/api", tags=["transactions"])
app.include_router(transaction_detail.router, prefix="/api", tags=["transaction_details"])  