import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

import models.db_models
from core.config import settings

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import database settings

# Alembic Config object
config = context.config

# Set up logging
# if config.config_file_name:
fileConfig(config.config_file_name)

# Database connection URL
# DATABASE_URL = f"postgresql://{settings_legacy.POSTGRESQL_USERNAME}:{settings_legacy.POSTGRESQL_PASSWORD}@{settings_legacy.POSTGRESQL_HOST}:5432/{settings_legacy.POSTGRESQL_DATABASE}"
# config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Set target metadata for auto-generating migrations
target_metadata = models.db_models.SQLModel.metadata


def get_url():
    if settings.ENV == 'PROD' and settings.SYSTEM_TYPE == 'AWS_MACHINE':
        return str(settings.SQLALCHEMY_DATABASE_URI)
    elif settings.ENV == 'DEV' and settings.SYSTEM_TYPE == 'MACBOOK':
        return str(settings.LOCAL_SQLALCHEMY_DATABASE_URI)
    else:
        raise Exception(f'Invalid environment configuration. ENV: {settings.ENV}, SYSTEM_TYPE: {settings.SYSTEM_TYPE}. Must be either PROD/AWS_MACHINE or DEV/MACBOOK.')


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
