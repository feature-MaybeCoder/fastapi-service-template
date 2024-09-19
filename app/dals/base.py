import logging
from typing import Generator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)
import sqlalchemy as sa
from app.db import sessions_maker


class BaseDal:
    """
    A base class for data access layer
    """

    def __init__(self):
        self._sessions_maker = sessions_maker

    async def _get_db(self) -> AsyncSession:
        """
        Get DB session instance.
        """
        try:
            async with self._sessions_maker() as db:
                return db
        except Exception as e:
            logger.exception("Session rollback because of exception: %s.", e)
            await db.rollback()
        finally:
            await db.close()
