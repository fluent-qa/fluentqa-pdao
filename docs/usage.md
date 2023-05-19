# 使用用例

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

