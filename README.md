# fluentqa-pdao

<div align="center">

[![Build status](https://github.com/fluent-qa/fluentqa-pdao/workflows/build/badge.svg?branch=main&event=push)](https://github.com/fluent-qa/fluentqa-pdao/actions/workflows/build.yml/badge.svg)
![Coverage Report](assets/images/coverage.svg)

`fluentqa_pdao` is a Python package for database operation

</div>

## Features:

1. [] easy to connect database 
2. [] easy to do sql operations CRUD
3. [] easy to support different mapper to python class
4. [] easy to generate sql and create sql version
5. [] easy to integrate with other libs
6. [] support async operations
7. [] support supabase

## Very first steps

### Initialize your code

1. Initialize `git` inside your repo:

```bash
cd fluentqa-pdao && git init
```

2. If you don't have `Poetry` installed run:

```bash
make poetry-download
```

3. Initialize poetry and install `pre-commit` hooks:

```bash
make install
make pre-commit-install
```

4. Run the codestyle:

```bash
make codestyle
```

5. Upload initial code to GitHub:

```bash
git add .
git commit -m ":tada: Initial commit"
git branch -M main
git remote add origin https://github.com/fluent-qa/fluentqa-pdao.git
git push -u origin main
```

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

### 1.1 创建数据库访问Client

创建数据库访问客户端:

```python
db_config = DatabaseConfig(url="sqlite:///test.db")
dao = DatabaseClient(config=db_config)
```

### 1.2 表结构定义

```python
class Hero(SQLModel, table=True, extend_existing=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None
    created_date: datetime = datetime.now()
```
创建表:

```shell
  SQLModel.metadata.create_all(database.engine)
    metadata = MetaData(schema=schema_name,)
    metadata.create_all(database.engine)

```

## 1.2 使用查询

1. 直接使用SQL

```python
def test_query_all():
    sql = """
    select * from hero
    """
    raw_result = dao.query(sql)
    result = SqlResultMapper.sql_result_to_model(raw_result, Hero)
    print(result)

    objects = dao.query_for_objects(sql, Hero)
    print(objects)
```

## Repository

使用native_sql装饰器：

```python
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

    @native_sql("update hero set name= :new_name where name= :name",modify=True)
    def update_name(self, name, new_name):
        ...
```

调用:

```python
repo = HeroRepo()


def test_query_by_decor():
    result = repo.find_hero()
    print(result)
    result = repo.find_hero_by_name(name="test3", age=10)
    print(result)
    repo.update_name(name="test4",new_name="test_name_4")
    print(repo.find_hero_by_name(name="test_name_4"))

```

## More

integrate with dl-sql:
- [dl-sql](https://github.com/adobe/dy-sql.git)

