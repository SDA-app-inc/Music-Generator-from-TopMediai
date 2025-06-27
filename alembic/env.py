from logging.config import fileConfig
import sys
from os.path import dirname, abspath

from sqlalchemy import engine_from_config, pool, inspect
from alembic import context

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

from app.configs import settings
from app.database import Base
# Импорт моделей (чтобы они попали в metadata)
from app.models.application import Application,ApplicationTemplate  # noqa
from app.models.template import Template  # noqa
from app.models.request_stats import RequestStats  # noqa
from app.models.voice import Voice  #noqa

# Alembic Config
config = context.config
config.set_main_option("sqlalchemy.url", f"{settings.DATABASE_URL_psycopg}")

# Логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata



def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
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
