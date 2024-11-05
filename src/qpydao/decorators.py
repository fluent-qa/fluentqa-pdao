from __future__ import annotations

import typing
from functools import wraps

from pydantic import BaseModel
from sqlmodel import SQLModel

from qpydao import databases
from qpydao import sql_utils


def native_sql(
    sql_statement,
    return_type: SQLModel | BaseModel | typing.Any = None,
    modify=False,
    db=None,
):
    def sql_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if db is None:
                engine = databases.get_db(args[0].db_qualifier)
            else:
                engine = databases.get_db(db)

            if modify:
                sql_result = engine.execute(sql_statement, **kwargs)
            else:
                raw_result = engine.plain_query(sql_statement, **kwargs)
                if return_type is None:
                    new_return_type = args[0].base_type
                else:
                    new_return_type = return_type
                sql_result = sql_utils.SqlResultMapper.sql_result_to_model(
                    raw_result, new_return_type
                )
            return sql_result

        return wrapper

    return sql_decorator
