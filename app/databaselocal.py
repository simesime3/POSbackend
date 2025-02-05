from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from .config import DATABASE_URL, DATABASE_URL_async  # DB接続情報
import os
from dotenv import load_dotenv

# .env ファイルをロード
load_dotenv()

# 環境変数からデータベースのURLを取得
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL_async = os.getenv("DATABASE_URL_async")

# 非同期エンジンの作成
engine_asyc = create_async_engine(DATABASE_URL_async, echo=True)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 非同期セッションローカルを作成
AsyncSessionLocal = sessionmaker(
    bind=engine_asyc,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

import logging

# ロガーを設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# DB接続を管理するためのget_db関数（同期セッション）
def get_db():
    db = SessionLocal()  # 新しい同期DBセッションを作成
    logger.info(f"dbのタイプ: {type(db)}")
    try:
        yield db  # dbセッションをyieldして依存性注入
    finally:
        db.close()  # セッションを閉じる

# 非同期DB接続を管理するためのget_db_async関数（非同期セッション）
async def get_db_async():
    async with AsyncSessionLocal() as db:
        logger.info(f"非同期DB接続が確立されました: {type(db)}")
        return db
