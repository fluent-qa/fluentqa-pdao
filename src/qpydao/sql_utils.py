from typing import Any

from pydantic import BaseModel
from sqlmodel import text, delete, select, update, SQLModel
from sqlalchemy.exc import ResourceClosedError


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
        return update(type(instance)) \
            .filter_by(id=getattr(instance, "id")) \
            .filter_by(**kwargs).values(**instance.dict())


class SqlResultMapper:
    @staticmethod
    def sql_result_to_model(result, model_type: type[BaseModel]) -> list[Any]:
        all_list = []
        try:
            for row in result:
                result_dict = {}
                for key in row.keys():
                    result_dict[key] = str(row[key])
                all_list.append(model_type(**result_dict))
        except ResourceClosedError as e:
            print(e)
        return all_list

    @staticmethod
    def sql_result_to_dict(result) -> list[dict]:
        all_list = []
        for row in result:
            result_dict = {}
            for key in result.keys():
                result_dict[key] = str(row[key])
            all_list.append(result_dict)
        return all_list

    @staticmethod
    def sqlmodel_query_result_to_model(result) -> list[Any]:
        return [item[0] for item in result]
