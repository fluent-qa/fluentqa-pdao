from __future__ import annotations

from typing import Any, Optional
from typing import Dict

from pydantic import BaseModel, model_validator
from qpyconf import settings
from sqlmodel import SQLModel, Field

from .exceptions import DatabaseClientConfigError


def _validate_param(name: str, value: str) -> None:
    if not value:
        raise DatabaseClientConfigError(
            f'Database parameter "{name}" is not set or empty and is required'
        )


class DatabaseConfig(BaseModel):
    """
    database client configurations
    """
    db_url: str | None = None
    host: str = None
    user: str = None
    password: str = None
    database: str = None
    port: Optional[int] = 5432
    pool_size: Optional[int] = 10
    pool_recycle: Optional[int] = 3600
    echo_queries: Optional[bool] = True
    charset: Optional[str] = "utf8"
    options: Dict[str, Any] = None

    @model_validator(mode="after")
    def check_db_url(self):
        if self.db_url is None:
            _validate_param("host", self.host)
            _validate_param("user", self.host)
            _validate_param("password", self.host)
            _validate_param("port", self.host)
            _validate_param("database", self.host)


class SqlRequestModel(BaseModel):
    """
    SqlRequestModel: Model for SQLRequest
    """
    config: DatabaseConfig
    sql: str
    parameters: Dict = {}
    db_name: str


class FieldMeta(BaseModel):
    """
    Field Meta: Model for Field
    """
    field_name: str
    field_type: str
    code_type: str = ""
    code_value: str = ""


class TableMeta(BaseModel):
    """
    TableMeta: Model for Table
    """
    table_name: str
    fields: list[FieldMeta]


class BaseEntity(SQLModel):
    """
    BaseEntity: Model for BaseEntity
    """
    pass


class BaseIDModel(BaseEntity):
    id: int | None = Field(default=None, primary_key=True)


def database_config(db_name: str = "default") -> DatabaseConfig:
    return DatabaseConfig(**settings.databases[db_name])
