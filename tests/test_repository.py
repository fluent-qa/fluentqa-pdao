from qpydao import databases
from qpydao.core.decorators import native_sql
from qpydao.repository import RepositoryMeta

from .fixtures_db import *

init_db_test()


class HeroRepo(metaclass=RepositoryMeta, base_type=Hero):
    @native_sql("select * from hero")
    def find_hero(self):
        pass

    @native_sql("select * from hero where name=:name and age=:age")
    def find_hero_by_name_and_age(self, name, age):
        pass

    @native_sql("select * from hero where name= :name")
    def find_hero_by_name(self, name): ...

    @native_sql("update hero set name= :new_name where name= :name", modify=True)
    def update_name(self, name, new_name):
        pass


def test_default_db():
    db = databases.get_db("default")
    print(db)


def test_repo():
    repo = HeroRepo()
    print(repo)
    result = repo.find_hero()
    print(result)
    repo.find_hero_by_name(name="new_test")
    repo.update_name(name="test", new_name="new_test")
