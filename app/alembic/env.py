from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Импортируем Base из твоего приложения
from core.database import Base
from core.config import settings

# Этот объект Alembic использует для конфигурации
config = context.config

# Подключение URL из твоих настроек
config.set_main_option('sqlalchemy.url', settings.db.url)

# Логирование Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Модель metadata
target_metadata = Base.metadata


def run_migrations_offline():
    """Режим оффлайн — просто генерит SQL."""
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_types=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Режим онлайн — применяет миграции к БД (async)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection: Connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_types=True,  # отслеживать изменения типов колонок
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
