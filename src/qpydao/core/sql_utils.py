from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel
from sqlalchemy.exc import ResourceClosedError
from sqlmodel import SQLModel
from sqlmodel import delete
from sqlmodel import select
from sqlmodel import text
from sqlmodel import update


class SqlBuilder:
    @staticmethod
    def from_plain_sql(plain_sql, **kwargs):
        s = text(plain_sql, **kwargs)
        return s

    @staticmethod
    def build_select_query(entity: type[SQLModel], **kwargs):
        return select(entity).filter_by(**kwargs)

    @staticmethod
    def build_delete_statement(entity: type[SQLModel], **kwargs):
        return delete(entity).filter_by(**kwargs)

    @staticmethod
    def build_filter_query(entity: type[SQLModel], instance: SQLModel, *args):
        filters = {}
        ## TODO: if time, solve it, 或者Between 这种
        for item in args:
            filters[item] = getattr(instance, item)
        return select(entity).filter_by(**filters)

    @staticmethod
    def build_update_statement(instance: type[SQLModel], **kwargs):
        return (
            update(type(instance))
            .filter_by(id=getattr(instance, "id"))
            .filter_by(**kwargs)
            .values(**instance.model_dump())
        )


class SqlResultMapper:
    @staticmethod
    def sql_result_to_model(
        result: List[Dict], model_type: type[SQLModel,BaseModel]
    ) -> list[Any]:
        all_list = []
        try:
            for row in result:
                all_list.append(model_type(**row))
        except ResourceClosedError as e:
            print(e)
        return all_list

    @staticmethod
    def sqlmodel_query_result_to_model(result) -> list[Any]:
        return [item[0] for item in result]
