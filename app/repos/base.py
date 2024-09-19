"""
Module which contains base repositories.
"""

from typing import Any, Generic, List, Optional, Type, TypeVar

import sqlalchemy as sa
from app.models import base as base_model
from sqlalchemy import ScalarResult, select, text
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=base_model.Base)


class DbRepo(Generic[ModelType]):
    """
    Base DB repository.
    Warning!: To use base db repo id field of your model must be "id", redefine methods for your model otherwise
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, db: AsyncSession, **create_kwargs) -> ModelType:
        """
        Create object.

        Args:
            db (AsyncSession): A DB instance.
            **create_kwargs: A kwargs to create object.

        Returns:
            ModelType: New object.
        """
        new_obj = self.model()
        for key in create_kwargs.keys():
            setattr(new_obj, key, create_kwargs[key])

        db.add(new_obj)

        return new_obj

    async def get(
        self, db: AsyncSession, *, obj_id: int
    ) -> Optional[ModelType]:
        """
        Get a single object by ID.

        Args:
            db (AsyncSession): A DB instance.
            obj_id (int): An object's ID.

        Returns:
            Optional[ModelType]: The found object or None.
        """
        result = await db.execute(
            select(self.model).where(text(f"id = {obj_id}"))
        )

        return result.scalar()

    async def get_all(self, db: AsyncSession) -> ScalarResult[Any]:
        """
        Get all objects.

        Args:
            db (sa.orm.Session): A DB instance.

        Returns:
            Optional[ModelType]: The found object or None.
        """
        result = await db.execute(select(self.model))
        result = result.scalars()
        return result

    async def update(
        self, db: AsyncSession, obj_id: int, **update_kwargs
    ) -> None:
        """
        Update object.

        Args:
            db (AsyncSession): A DB instance.
            obj_id (int): An id of object to update.
            update_kwargs: A kwargs to update object.

        Returns:
            None.
        """
        obj = await self.get(db, obj_id=obj_id)
        for key in update_kwargs.keys():
            setattr(obj, key, update_kwargs[key])

        db.add(obj)

        return obj

    async def delete(self, db: AsyncSession, obj_id: int) -> None:
        """
        Delete object.

        Args:
            db (AsyncSession): A DB instance.
            obj_id (int): An id of object to delete.

        Returns:
            None.
        """
        obj = await self.get(db, obj_id=obj_id)
        await db.delete(obj)
