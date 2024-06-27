## How TO

## How to Use database

- setting files:

```sh
[default]
key = "value"
databases = { default = { db_url = "postgresql+psycopg://postgres:changeit@127.0.0.1:5432/workspace" } }
pg_url = "postgresql+psycopg://postgres:changeit@127.0.0.1:5432/workspace"
pg_a_url = "postgresql+psycopg_async://postgres:changeit@127.0.0.1:5432/workspace"

```

```python
db = databases.get_db("default")
```

## How to Use query directly

```python
def test_query_bind_params():
  sql = f'select * from hero where name=:name'
  raw_result = dao.plain_query(sql, name="test6")
  result = SqlResultMapper.sql_result_to_model(raw_result, Hero)
  print(result)
  objects = dao.find_by(Hero, **{"name": "test6"})
  print(objects)
```

```python
def test_use_sqlmodel_statement():
  s = select(Hero).where(Hero.name == "test6")
  result = dao.query_for_model(s)
  print(result)


def test_find_by():
  result = dao.find_by(Hero, **{"name": "4321"})
  print(result)
```

## How to Use Repository Model

```python

class HeroRepo(metaclass=RepositoryMeta, base_type=Hero):

    @native_sql("select * from hero")
    def find_hero(self):
        pass

    @native_sql("select * from hero where name=:name and age=:age")
    def find_hero_by_name_and_age(self, name, age):
        pass

    @native_sql("select * from hero where name= :name")
    def find_hero_by_name(self, name):
        ...

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

```
