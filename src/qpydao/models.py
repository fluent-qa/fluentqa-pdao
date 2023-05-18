from typing import Any
from typing import Dict

from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    url: str | None = None
    pool_size: int | None = None
    additional: Dict[str, Any] = None


class SqlRequestModel(BaseModel):
    config: DatabaseConfig
    sql: str
    parameters: Dict = {}


class FieldMeta(BaseModel):
    field_name: str
    field_type: str
    code_type: str = ""
    code_value: str = ""


class TableMeta(BaseModel):
    table_name: str
    fields: list[FieldMeta]
