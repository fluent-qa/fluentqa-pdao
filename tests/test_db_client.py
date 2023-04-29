#!/usr/bin/env python
# postgresql: postgresql: // scott: tiger @ localhost:5432 / mydatabase
# jdbc:postgresql://localhost:5432/mydatabase?currentSchema=myschema
# pip install psycopg2-binary
import pytest

from sqlmodel import Field
from sqlmodel import SQLModel

from qpydao import sql_result_to_model
from qpydao.bootstrap import init_pg_database
from qpydao.client import DatabaseClient
from qpydao.models import DatabaseConfig


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None


db_config = DatabaseConfig(url="sqlite:///test.db")
pg = DatabaseClient(config=db_config)


def test_init_database():
    init_pg_database(pg)


def test_create_engine():
    h1 = Hero(name="test3", secret_name="scret_name", age=10)
    pg.save(h1)
    r1 = pg.one_or_none(Hero, name=h1.name, age=h1.age)
    if r1 is not None:
        r1.age = h1.age
    pg.update_by(Hero, r1)
    r2 = pg.find_by(Hero, name="test3")
    pg.delete_by(Hero, name="test3")


## TODO: Fix the query
def test_execute_sql():
    sql = """
    delete from hero
    """
    raw_result = pg.execute(sql)
    sql_1 = """
    update hero set name = 'test'
    """
    pg.execute(sql_1)


def test_query_bind_params():
    sql = """
    select * from hero where name=:name
    """
    raw_result = pg.query(sql, **{"name": "t2"})
    result = sql_result_to_model(raw_result, Hero)
    print(result)
