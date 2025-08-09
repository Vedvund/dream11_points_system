from sqlmodel import create_engine

from core.config import settings

if settings.ENV == 'PROD':
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
else:
    engine = create_engine(str(settings.LOCAL_SQLALCHEMY_DATABASE_URI))
