# fluentqa-pdao

<div align="center">

[![Build status](https://github.com/fluent-qa/fluentqa-pdao/workflows/build/badge.svg?branch=main&event=push)](https://github.com/fluent-qa/fluentqa-pdao/actions/workflows/build.yml/badge.svg)
![Coverage Report](assets/images/coverage.svg)

`qpydao` is a Python package for database operation

</div>

## Features:

1. [X] easy to connect database
2. [X] easy to do sql operations CRUD
3. [X] easy to support different mapper to python class
4. [X] easy to generate sql and create sql version
5. [X] easy to integrate with other libs
6. [X] support async operations
7. [X] support supabase


## 项目中使用:

添加以下依赖到pyproject.toml文件

```shell
qpydao = { git = "https://github.com/fluent-qa/fluentqa-pdao.git", branch = "main" }
```

## 目标

1. 可以使用pydantic model
2. 也可以使用sqlachmey/sqlmodel
3. 能够支持常用的DAO模式:
   - [X] 直接CRUD
   - [X] Repository 模式
   - [X] Model 支持直接操作数据库
   - [X] Async支持+Session封装
   - [X] 支持多数据库
4. event listener on entity change
5. code generation
6. CRUD operation
7. Module Registration and Auto Injection

##  使用用例

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

## More

integrate with dl-sql:
- [dl-sql](https://github.com/adobe/dy-sql.git)
