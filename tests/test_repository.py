from qpydao import native_sql
from qpydao.repository import BaseRepository

from .fixtures_db import *


init_db_test()


class HeroRepo(BaseRepository):
    @native_sql("select * from hero")
    def find_hero(self):
        ...

    @native_sql("select * from hero where name=:name and age=:age")
    def find_hero_by_name(self, name, age):
        ...

    @native_sql("select * from hero where name= :name")
    def find_hero_by_name(self, name):
        ...

    @native_sql("update hero set name= :new_name where name= :name", modify=True)
    def update_name(self, name, new_name):
        ...


repo = HeroRepo()


def test_query_by_decor():
    result = repo.find_hero()
    print(result)
    result = repo.find_hero_by_name(name="test3", age=10)
    print(result)
    repo.update_name(name="test4", new_name="test_name_4")
    print(repo.find_hero_by_name(name="test_name_4"))
