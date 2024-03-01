# type: ignore[attr-defined]
"""Awesome `fluentqa_pdao` is a Python cli/package """

from .bootstrap import *
from .client import *
from .models import *


## TODO Add more imports

# Public imports
from .mapper.base import (
    BaseMapper,
    DbMapResult,
    RecordCombiningMapper,
    SingleRowMapper,
    SingleColumnMapper,
    SingleRowAndColumnMapper,
    CountMapper,
    KeyValueMapper,
)
from .sql_utils import QueryData, QueryDataError, TemplateGenerators
from .connections import (
    sqlexists,
    sqlquery,
    sqlupdate,
)
from .db import (
    is_set_current_database_supported,
    reset_current_database,
    set_current_database,
    set_database_init_hook,
    set_default_connection_parameters,
)
from .exceptions import DBNotPreparedError


__all__ = [
    "BaseMapper",
    "DbMapResult",
    "RecordCombiningMapper",
    "SingleRowMapper",
    "SingleColumnMapper",
    "SingleRowAndColumnMapper",
    "CountMapper",
    "KeyValueMapper",
    "QueryData",
    "QueryDataError",
    "TemplateGenerators",
    "sqlexists",
    "sqlquery",
    "sqlupdate",
    "is_set_current_database_supported",
    "reset_current_database",
    "set_current_database",
    "set_database_init_hook",
    "set_default_connection_parameters",
    "DBNotPreparedError",
]
