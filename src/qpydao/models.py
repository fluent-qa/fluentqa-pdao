from typing import Dict, Any
from qpybase import BaseDataModel


class DatabaseConfig(BaseDataModel):
    url: str | None = None
    pool_size: int | None = None
    additional: Dict[str, Any] = None


class FieldMeta(BaseDataModel):
    field_name: str
    field_type: str
    code_type: str = ""
    code_value: str = ""


class TableMeta(BaseDataModel):
    table_name: str
    fields: list[FieldMeta]
