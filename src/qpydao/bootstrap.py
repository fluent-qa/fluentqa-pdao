from sqlalchemy import MetaData
from sqlmodel import SQLModel

from qpydao import DatabaseClient, db


def init_database(database: DatabaseClient = db, schema_name: str = None):
    """
    init postgresql database
    :param database:
    :param schema_name:
    :return:
    """
    SQLModel.metadata.create_all(database.engine)
    metadata = MetaData(
        schema=schema_name,
    )
    metadata.create_all(database.engine)
