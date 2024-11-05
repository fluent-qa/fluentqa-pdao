from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from sqlmodel import SQLModel

from qpydao import databases


class RepositoryMeta(type):
    def __new__(
        cls,
        name,
        bases,
        attrs,
        base_type: SQLModel | BaseModel | Any = SQLModel,
        db_qualifier="default",
        **kwargs,
    ):
        x = super().__new__(cls, name, bases, attrs, **kwargs)
        x.base_type = base_type
        x.db_qualifier = db_qualifier
        x.db_client = databases.get_db(x.db_qualifier)
        return x
