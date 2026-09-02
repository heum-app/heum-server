from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 1. 추가 import
import os
from dotenv import load_dotenv
from app.core.config import SQLALCHEMY_DATABASE_URI  # DB 연결 경로
from app.db.base import Base  # Base.metadata 로드 (모델 등록용)

# 2. Alembic 기본 설정
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. 환경 변수 로드
load_dotenv()

# 4. Alembic의 DB URL 설정을 환경값으로 대체
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URI)

# 5. metadata 등록 (모든 모델 감지)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
