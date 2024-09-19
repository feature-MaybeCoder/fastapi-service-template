"""
Module with the DB session configuration.
"""

import sqlalchemy as sa
import sqlalchemy.orm
from app.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine(
    settings.DB_URI,
    future=True,
    echo=False,
    pool_size=20,
    isolation_level="READ COMMITTED",
)

sessions_maker = sa.orm.sessionmaker(
    autocommit=False,
    expire_on_commit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)
