#!/usr/bin/env python
import typing

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import update
from sqlmodel import Session

from qpydao.exceptions import RecordNotFoundException
from qpydao.models import DatabaseConfig
from qpydao.utils import *


class DatabaseClient:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = create_engine(url=config.url, echo=True)

    @staticmethod
    def db_client(url: str):
        return DatabaseClient(DatabaseConfig(url=url))

    @classmethod
    def create_engine(cls, connection_url):
        """
        postgresql: postgresql://scott:tiger@localhost:5432/mydatabase
        """

        return create_engine(connection_url)

    ## todo: page request
    def save(self, instance: SQLModel):
        with Session(self.engine) as s:
            s.add(instance)
            s.commit()
            s.refresh(instance)

    def query(self, plain_sql: str, **kwargs):
        s = text(plain_sql)
        with self.engine.connect() as conn:
            result = conn.execute(s, **kwargs).fetchall()
        return result

    def execute(self, plain_sql: str, **kwargs) -> typing.NoReturn:
        s = text(plain_sql, **kwargs)
        with self.engine.connect() as conn:
            conn.execute(s, **kwargs)

    def query_for_objects(self, plain_sql, result_type: type[BaseModel], **kwargs):
        result = self.query(plain_sql, **kwargs)
        return sql_result_to_model(result, result_type)

    def __query_by_statement(self, statement):
        with Session(self.engine) as session:
            return session.exec(statement).all()

    def find_by(self, entity: [SQLModel], **kwargs) -> Any:
        query = build_select_query(entity, **kwargs)
        return self.__query_by_statement(statement=query)

    def one_or_none(self, entity: [SQLModel], **kwargs):
        query = build_select_query(entity, **kwargs)
        result = self.__query_by_statement(statement=query)
        if len(result) < 1:
            raise RecordNotFoundException("Record Not Found", kwargs)
        else:
            return result[0]

    def delete_by(self, entity: type[SQLModel], **kwargs):
        with Session(self.engine) as session:
            statement = build_delete_statement(entity, **kwargs)
            session.exec(statement)
            session.commit()

    def update_by(self, entity: type[SQLModel], instance: SQLModel):
        with Session(self.engine) as session:
            statement = (
                update(entity).filter_by(id=instance.id).values(**instance.dict())
            )
            session.exec(statement)
            session.commit()
