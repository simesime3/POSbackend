from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base
import os

# データベース接続URLを読み込む
config = context.config
url = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:@localhost/pos_app")

# メタデータを取り込む
target_metadata = Base.metadata

def run_migrations_offline():
    # オフラインマイグレーションを実行
    context.configure(url=url, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    # オンラインマイグレーションを実行
    connectable = engine_from_config(config.get_section(config.config_ini_section), poolclass=pool.NullPool)
    context.configure(connection=connectable, target_metadata=target_metadata)
    with connectable.connect() as connection:
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
