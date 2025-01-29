from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from .config import DATABASE_URL  # DB接続情報

# データベース接続の設定
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DB接続を管理するためのget_db関数
@contextmanager
def get_db():
    db = SessionLocal()  # 新しいDBセッションを作成
    try:
        yield db  # dbセッションをyieldして依存性注入
    finally:
        db.close()  # セッションを閉じる
