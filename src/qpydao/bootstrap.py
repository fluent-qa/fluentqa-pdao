from sqlalchemy import MetaData
from sqlmodel import SQLModel

from qpydao import DatabaseClient


def init_pg_database(database: DatabaseClient, schema_name: str):
    SQLModel.metadata.create_all(database.engine)
    metadata = MetaData(schema=schema_name)
    metadata.create_all(database.engine)
