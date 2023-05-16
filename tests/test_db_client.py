#!/usr/bin/env python
# postgresql: postgresql: // scott: tiger @ localhost:5432 / mydatabase
# jdbc:postgresql://localhost:5432/mydatabase?currentSchema=myschema
# pip install psycopg2-binary
import datetime

import pytest

from sqlmodel import Field, select
from sqlmodel import SQLModel

from qpydao import SqlResultMapper
from qpydao.bootstrap import init_pg_database
from qpydao.client import DatabaseClient
from qpydao.models import DatabaseConfig

db_config = DatabaseConfig(url="sqlite:///test.db")
dao = DatabaseClient(config=db_config)


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None
    created_date: datetime.datetime = datetime.datetime.now()


def test_init_database():
    init_pg_database(dao)


def test_create_engine():
    h1 = Hero(name="test3", secret_name="scret_name", age=10)
    h2 = Hero(name="test4", secret_name="scret_name", age=10)
    h3 = Hero(name="test6", secret_name="scret_name", age=10)
    print(h3.dict())
    dao.save(h1)
    dao.save(h2)
    dao.save(h3)
    r1 = dao.one_or_none(Hero, name=h1.name, age=h1.age)
    if r1 is not None:
        print(h1.age)
        print(h1.age)
    # pg.update_by(Hero, r1)
    r2 = dao.find_by(Hero, name="test3")
    print(r2)


def test_batch_save():
    h1 = Hero(name="test3", secret_name="scret_name", age=10)
    h2 = Hero(name="test4", secret_name="scret_name", age=11)
    h3 = Hero(name="test6", secret_name="scret_name", age=12)
    instances = [h1, h2, h3]
    dao.batch_save(instances)
    for instance in instances:
        print(instance.json())


def test_query_all():
    sql = """
    select * from hero
    """
    raw_result = dao.query(sql)
    result = SqlResultMapper.sql_result_to_model(raw_result, Hero)
    print(result)

    objects = dao.query_for_objects(sql, Hero)
    print(objects)


def test_query_bind_params():
    sql = """
    select * from hero where name=:name
    """
    raw_result = dao.query(sql, **{"name": "test6"})
    result = SqlResultMapper.sql_result_to_model(raw_result, Hero)
    print(result)
    objects = dao.query_for_objects(sql, Hero, **{"name": "test6"})
    print(objects)


def test_use_sqlmodel_statement():
    s = select(Hero).where(Hero.name == "test6")
    result = dao.query_by_statement(s)
    print(result)


def test_find_by():
    result = dao.find_by(Hero, **{"name": "4321"})
    print(result)


def test_delete_by():
    r2 = dao.find_by(Hero, name="test3")
    dao.delete_by(Hero, **r2[0].dict())
    r3 = dao.find_by(Hero, name="test3")
    print(r3)


def test_one_or_none():
    result = dao.one_or_none(Hero, **{"name": "test6"})
    print(result)


def test_update_by():
    r2 = dao.find_one(Hero, name="test6")
    r2.age = 190
    print(r2.__class__)
    dao.update_by_id(r2)
    print(dao.find_by(Hero, id=r2.id)[0])
