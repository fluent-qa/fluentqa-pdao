from qpydao import (
    DatabaseClient,
    Databases,
    database_config,
    databases,
    db,
    init_database
)
from qpydao.database_client import init_database

config = database_config()
client = DatabaseClient(config=config)


def test_init_database_client():
    print(config)
    print(client)
    assert isinstance(client, DatabaseClient)


def test_engines():
    print(client.engine)
    print(client.async_engine)


def test_default_client():
    print(db.engine)
    print(db.async_engine)


def test_database_singleton():
    db = Databases()
    assert databases == db

def test_init_database():
    init_database(client)
