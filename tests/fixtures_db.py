from __future__ import annotations

from datetime import datetime

from sqlmodel import Field
from sqlmodel import SQLModel

from qpydao import DatabaseClient, DatabaseConfig, BaseIDModel, databases
from qpydao import Databases
from qpydao.bootstrap import init_database

# db_config = DatabaseConfig(db_url="sqlite:///test.db")
dao = databases.get_db("default")

# default_client = databases.register_db("default", db_config)


class Hero(BaseIDModel, table=True, extend_existing=True):
    # id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None
    created_date: datetime = datetime.now()


def init_db_test():
    try:
        init_database(dao)

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
    except Exception as e:
        print(e)
