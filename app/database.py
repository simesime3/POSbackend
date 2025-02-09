import os
import tempfile
import atexit
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import logging
import base64
from urllib.parse import quote_plus
from sqlalchemy import text
import ssl


# ロガーを設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# .env ファイルをロード
load_dotenv()

# 環境変数からデータベースの接続情報を取得
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", 3306)

# 環境変数から Base64 化された証明書を取得
pem_b64 = os.getenv("DB_SSL_CA")

if pem_b64:
    # Base64 をデコードして PEM に戻す
    pem_content = base64.b64decode(pem_b64).decode("utf-8")
    # PEM 証明書を一時ファイルに書き込む
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".pem") as temp_pem:
        temp_pem.write(pem_content.replace("\\n", "\n"))  # 改行コードの変換
        temp_pem_path = temp_pem.name

    logger.info(f"証明書ファイルのパス: {temp_pem_path}")

    # SSLコンテキストを作成（非同期用）
    ssl_context = ssl.create_default_context(cafile=temp_pem_path)


    # 同期用SQLAlchemy接続URL（aiomysqlは非同期用なのでこちらは使わない）
    DATABASE_URL = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@"
        f"{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl_ca={temp_pem_path}"
    )
    # 非同期用SQLAlchemy接続URL（sslは connect_args に渡すので URL に含めない）
    DATABASE_URL_async = (
        f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

else:
    logger.error("SSL証明書の環境変数 DB_SSL_CA が設定されていません。")
    raise ValueError("SSL証明書の環境変数 DB_SSL_CA が設定されていません。")

# --- SQLAlchemy エンジンの作成（同期）---
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- 非同期SQLAlchemy エンジンの作成 ---
engine_async = create_async_engine(
    DATABASE_URL_async, 
    echo=True,
    connect_args={"ssl": ssl_context}  # ここで SSL を適用
)

AsyncSessionLocal = sessionmaker(bind=engine_async, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# --- ロガーの設定 ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# --- DB接続を管理する関数（同期）---
def get_db():
    db = SessionLocal()
    logger.info(f"✅ DB 接続確立（同期）: {type(db)}")
    try:
        yield db
    finally:
        db.close()
        logger.info("✅ DB 接続を閉じました（同期）")

# --- 非同期DB接続を管理する関数 ---
async def get_db_async():
    async with AsyncSessionLocal() as db:
        logger.info(f"✅ DB 接続確立（非同期）: {type(db)}")

        try:
            # 簡単なクエリを実行して DB 接続を確認
            result = await db.execute(text("SELECT 1;"))
            logger.info(f"🎯 DB接続テスト成功: {result.scalar()}")
        except Exception as e:
            logger.error(f"❌ DB接続テスト失敗: {e}")

        yield db

# --- 非同期DB接続を管理する関数（非同期）---
# 非同期用のコードは無効にしましたが、必要に応じて非同期処理も記述可能です。
# もし非同期処理を有効にする場合は、`aiomysql`を使う設定を有効化してください。

