from qpydao import DatabaseClient, DatabaseConfig, database_config, db

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
