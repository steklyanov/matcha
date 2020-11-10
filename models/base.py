from asyncpg import Connection
from sqlalchemy import Column, DateTime, MetaData, select, text
from sqlalchemy.ext.declarative import as_declarative, declared_attr

convention = {
    "all_column_names": lambda constraint, table: "_".join([column.name for column in constraint.columns.values()]),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


@as_declarative(metadata=metadata)
class Base:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=text("clock_timestamp()"), nullable=False)


class CreateByNameMixin:
    @classmethod
    async def get_or_create(cls, conn: Connection, name: str) -> int:
        # Check if object already exists
        query = select([cls.__table__.c.id]).where(cls.name == name)
        object_id = await conn.fetchval(query)
        if object_id is not None:
            return object_id
        # Create new object
        query = cls.__table__.insert().values(name=name).returning(cls.__table__.c.id)
        return await conn.fetchval(query)
