"""
Module with the Base model.
"""

import sqlalchemy as sa
from app import utils
from sqlalchemy.ext.declarative import as_declarative, declared_attr

# Custom MetaData object is required here since we should manually provide it
# with naming convention, otherwise migrations, generated by alembic, will have
# constraints with names set to None, which is a bad practice. Moreover, the
# downgrade actions will fail due to unspecified constraint name.
#
# Find more details here (see section "the-importance-of-naming-constraints"):
# https://alembic.sqlalchemy.org/en/latest/naming.html

metadata = sa.MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    },
)


@as_declarative(metadata=metadata)
class Base:
    """
    Base model.
    """

    @declared_attr
    def __tablename__(cls) -> str:
        table_name = f"{utils.underscore_from_camelcase(cls.__name__)}s"
        if table_name.endswith("ys"):
            table_name = f"{table_name[:-2]}ies"
        return table_name

    def __str__(self) -> str:
        pks = [key.name for key in sa.inspect(self.__class__).primary_key]
        return f"<{self.type}-{getattr(self, pks[0], None)}>"

    @property
    def type(self) -> str:
        """
        Get object type as string.
        """
        return self.__class__.__name__
