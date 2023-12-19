#!/usr/bin/env python
import typing

from functools import wraps

from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import psycopg2
from sqlmodel import Session
from sqlmodel import SQLModel

from .exceptions import DAOException
from .models import DatabaseConfig
from .models import SqlRequestModel
from .sql_utils import SqlBuilder
from .sql_utils import SqlResultMapper


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
    def __init__(self, config: DatabaseConfig):
        """
        DataConfiguration Could be injected
        """
        self.config = config
        self.engine = create_engine(url=config.url, echo=True)

    @staticmethod
    def db_client(url: str):
        return DatabaseClient(DatabaseConfig(url=url))

    @staticmethod
    def create_engine(connection_url, **kwargs):
        """
        postgresql: postgresql://scott:tiger@localhost:5432/mydatabase
        """

        return create_engine(connection_url)

    def save(self, instance: SQLModel | typing.Any, **kwargs):
        """
        save a sql model instance
        :param instance:
        :return:
        """
        with Session(self.engine) as s:
            s.add(instance)
            s.commit()
            s.refresh(instance)
        return instance

    def batch_save(self, instances: typing.List[SQLModel | typing.Any], **kwargs):
        with Session(self.engine) as s:
            s.bulk_save_objects(instances, return_defaults=True)
            s.commit()
        return instances

    def query(self, plain_sql: str, **kwargs) -> list[typing.Mapping[typing.Any, typing.Any]]:
        """
        execute sql with binding parameters
        :param plain_sql:
        :param kwargs:
        :return:
        """
        s = text(plain_sql)
        with self.engine.connect() as conn:
            result = conn.execute(s, kwargs).mappings().all()
        return result

    def execute(self, plain_sql: str, **kwargs):
        """
        execute sql
        :param plain_sql:
        :param kwargs:
        :return:
        """
        s = SqlBuilder.from_plain_sql(plain_sql)
        with self.engine.connect() as conn:
            return conn.execute(s, kwargs)

    def query_for_objects(self, plain_sql, result_type: type[BaseModel], **kwargs):
        """
        sql for object result
        :param plain_sql:
        :param result_type:
        :param kwargs:
        :return:
        """
        result = self.query(plain_sql, **kwargs)
        return SqlResultMapper.sql_result_to_model(result, result_type)

    def query_by_statement(self, statement) -> typing.List[SQLModel]:
        with Session(self.engine) as session:
            result = session.exec(statement).all()
        return result

    def find_by(self, entity: [SQLModel], **kwargs) -> typing.List[SQLModel]:
        query = SqlBuilder.build_select_query(entity, **kwargs)
        return self.query_by_statement(statement=query)

    def find_one(self, entity: [SQLModel], **kwargs) -> SQLModel | None:
        return self.one_or_none(entity, **kwargs)

    def one_or_none(self, entity: type[SQLModel], **kwargs) -> typing.Any:
        query = SqlBuilder.build_select_query(entity, **kwargs)
        result = self.query_by_statement(statement=query)
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

    def update_by_id(self, instance: typing.Union[SQLModel | typing.Any]):
        with Session(self.engine) as session:
            statement = SqlBuilder.build_update_statement(instance)
            session.exec(statement)
            session.commit()

    def invoke(self, request: SqlRequestModel):
        """
        TODO: SQL Injection Protection
        :param request:
        :return:
        """
        client = Databases.register_db(request.config, request.config.url)
        return client.execute(request.sql, **request.parameters)


class Databases:
    _instances = {}

    @staticmethod
    def default_client(config: DatabaseConfig = None):
        if Databases._instances.get("DEFAULT") is None:
            if config is None:
                raise DAOException("No Database Default Config Found")
            else:
                Databases._instances["DEFAULT"] = DatabaseClient(config)

        return Databases._instances["DEFAULT"]

    @staticmethod
    def get_db_client(name: str = None):
        return Databases._instances[name] if name else Databases._instances["DEFAULT"]

    @staticmethod
    def register_db(config: DatabaseConfig, qualifier: str):
        Databases._instances[qualifier] = DatabaseClient(config)
        return Databases._instances[qualifier]


def native_sql(sql_statement, modify=False, db=None):
    def sql_decorator(func):
        engine = Databases.get_db_client(db)

        @wraps(func)
        def wrapper(*args, **kwargs):
            if modify:
                sql_result = engine.execute(sql_statement, **kwargs)
            else:
                sql_result = engine.query(sql_statement, **kwargs)
            return sql_result

        return wrapper

    return sql_decorator


class GenericDao:
    def __init__(self, host, port, username, password, database, auto_commit=True):
        try:
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=username,
                password=password,
            )
            self.auto_commit = auto_commit
        except Exception as e:
            print("Error while connecting to PostgreSQL", e)
            self.__close_connection()

    def select(self, sql):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print("Error while access MySQL", e)
            self.__close_connection()
        finally:
            cursor.close()

    def insert(self, sql, values):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, values)
            if self.auto_commit:
                self.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error while access MySQL", e)
            self.__close_connection()
        finally:
            cursor.close()

    def execute_sql(self, sql):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql)
            if self.auto_commit:
                self.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error while access MySQL", e)
            self.__close_connection()
        finally:
            cursor.close()

    def __close_connection(self):
        if self.connection is None:
            return
        if self.connection.is_connected():
            self.connection.close()
            print("PgSql connection is closed")

    def commit(self):
        self.connection.commit()

    @staticmethod
    def get_dao(host, port, username, password, database, auto_commit=True):
        return GenericDao(
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
            auto_commit=auto_commit,
        )
