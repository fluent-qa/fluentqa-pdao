from __future__ import annotations

import typing
from collections.abc import Coroutine, Sequence
from typing import Any

import sqlalchemy
from qpyconf import settings
from sqlalchemy import Row, RowMapping, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import Session, SQLModel, select

from qpydao.core.models import (
    DatabaseConfig,
    SingletonMeta,
    SqlRequestModel,
    database_config,
)
from qpydao.core.sql_utils import SqlBuilder

from .exceptions import DAOException

"""
1. database client to do simple database operations
2. Overall Operations
    1. Execute SQL
    2. Pagination
    3. Get Records - Pydantic/SQLModel
    4. Save or Update
    5. Delete/Soft-Delete
    6. Like Query or With Some Dynamic Filter
"""


class DatabaseClient:
    """Database client, both synchronous and asynchronous."""

    def __init__(self, config: DatabaseConfig = None):
        self.config = config
        self._engine = None
        self._async_engine = None

    @property
    def engine(self):
        if self._engine is None:
            self._engine = sqlalchemy.create_engine(
                url=self.config.db_url,
                pool_pre_ping=True,
                pool_recycle=self.config.pool_recycle,
                echo=self.config.echo_queries,
            )
        return self._engine

    @property
    def async_engine(self):
        if self._async_engine is None:
            self._async_engine = create_async_engine(
                url=self.config.db_url,
                pool_pre_ping=True,
                pool_recycle=self.config.pool_recycle,
                echo=self.config.echo_queries,
            )
        return self._async_engine

    @staticmethod
    def create(db_name: str) -> DatabaseClient:
        return DatabaseClient(database_config(db_name))

    def save(self, instance: SQLModel | typing.Any):
        """Save a sql model instance
        :param instance:
        :return:
        """
        with Session(self.engine) as s:
            s.add(instance)
            s.commit()
            s.refresh(instance)
        return instance

    def async_save(self, instance: SQLModel | typing.Any):
        """Save a sql model instance
        :param instance:
        :return:
        """
        with AsyncSession(self.async_engine) as s:
            s.add(instance)
            s.commit()
            s.refresh(instance)
        return instance

    def batch_save(self, instances: list[SQLModel | typing.Any]):
        with Session(self.engine) as s:
            s.bulk_save_objects(instances, return_defaults=True)
            s.commit()
        return instances

    def plain_query(self, plain_sql: str, **kwargs) -> Sequence[RowMapping]:
        """Execute sql with binding parameters
        :param plain_sql:
        :param kwargs:
        :return:
        """
        s = text(plain_sql)
        with self.engine.connect() as conn:
            result = conn.execute(s, kwargs).mappings().all()
        return result

    async def async_plain_query(self, plain_sql: str, **kwargs) -> Sequence[RowMapping]:
        """Execute sql with binding parameters
        :param plain_sql:
        :param kwargs:
        :return:
        """
        s = text(plain_sql)
        async with AsyncSession(self.async_engine) as conn:
            result = await conn.execute(s, kwargs)
        return result.mappings().all()

    def query_for_model(
        self, statement: select
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        with Session(self.engine) as session:
            result = session.exec(statement).fetchall()
        return result

    def async_query_for_model(
        self, statement: select
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        with AsyncSession(self.engine) as session:
            result = session.exec(statement).fetchall()
        return result

    def execute(self, plain_sql: str, **kwargs):
        """Execute sql
        :param plain_sql:
        :param kwargs:
        :return:
        """
        s = SqlBuilder.from_plain_sql(plain_sql)
        with self.engine.connect() as conn:
            return conn.execute(s, kwargs)

    async def async_execute(self, plain_sql: str, **kwargs):
        """Execute sql
        :param plain_sql:
        :param kwargs:
        :return:
        """
        s = SqlBuilder.from_plain_sql(plain_sql)
        with self.async_engine.connect() as conn:
            return conn.execute(s, kwargs)

    def find_by(
        self, entity: [SQLModel], **kwargs
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        query = SqlBuilder.build_select_query(entity, **kwargs)
        return self.query_for_model(statement=query)

    async def async_find_by(
        self, entity: [SQLModel], **kwargs
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        query = SqlBuilder.build_select_query(entity, **kwargs)
        return self.async_query_for_model(statement=query)

    def find_one(self, entity: [SQLModel], **kwargs) -> SQLModel | None:
        return self.one_or_none(entity, **kwargs)

    async def async_find_one(
        self, entity: [SQLModel], **kwargs
    ) -> Coroutine[Any, Any, Any]:
        return self.async_one_or_none(entity, **kwargs)

    def one_or_none(self, entity: type[SQLModel], **kwargs) -> typing.Any:
        query = SqlBuilder.build_select_query(entity, **kwargs)
        result = self.query_for_model(statement=query)
        if len(result) < 1:
            # raise RecordNotFoundException("Record Not Found", kwargs)
            return None
        else:
            return result[0]

    async def async_one_or_none(self, entity: type[SQLModel], **kwargs) -> typing.Any:
        """TODO: Check Out Work or Not."""
        query = SqlBuilder.build_select_query(entity, **kwargs)
        result = self.async_query_for_model(statement=query)
        if len(result) < 1:
            # raise RecordNotFoundException("Record Not Found", kwargs)
            return None
        else:
            return result[0]

    def delete_by(self, entity: type[SQLModel], **kwargs) -> typing.NoReturn:
        if len(kwargs.values()) == 0:
            raise DAOException("can't execute delete without any filter")
        with Session(self.engine) as session:
            statement = SqlBuilder.build_delete_statement(entity, **kwargs)
            session.exec(statement)
            session.commit()

    def update_by_id(self, instance: SQLModel | typing.Any):
        with Session(self.engine) as session:
            statement = SqlBuilder.build_update_statement(instance)
            session.exec(statement)
            session.commit()


class Databases(metaclass=SingletonMeta):
    def __init__(self, conf=settings.DATABASES):
        self._databases = {}
        self._settings = conf
        self.__db_setup__()

    def __db_setup__(self):
        for item in self._settings:
            self._databases[item] = DatabaseClient(database_config(item))

    def __getitem__(self, name):
        try:
            return self._databases[name]
        except KeyError:
            raise KeyError(f"Database {name} does not exist")

    def __getattr__(self, name):
        try:
            return self._databases[name]
        except KeyError:
            raise KeyError(f"Database {name} does not exist")

    def default_client(self):
        return self._databases["default"]

    def register_db(self, db_name: str, config: DatabaseConfig):
        self._databases[db_name] = DatabaseClient(config)
        return self._databases[db_name]

    def invoke(self, request: SqlRequestModel):
        """TODO: SQL Injection Protection
        :param request:
        :return:
        """
        client = self.register_db(request.db_name, request.config)
        return client.execute(request.sql, **request.parameters)

    def get_db(self, db_name: str = None) -> DatabaseClient:
        if db_name is None:
            return self._databases["default"]
        else:
            return self._databases[db_name]


all_dbs = Databases()
default_dao = all_dbs.get_db("default")
default_db_conf = database_config(db_name="default")
