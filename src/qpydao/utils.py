from typing import Any

from select import select

from pydantic import BaseModel
from sqlalchemy.exc import ResourceClosedError
from sqlmodel import SQLModel
from sqlmodel import delete
from sqlmodel import select


def sql_result_to_model(result, model_type: type[BaseModel]) -> list[Any]:
    all_list = []
    try:
        for row in result:
            result_dict = {}
            for key in result.keys():
                result_dict[key] = str(row[key])
            all_list.append(model_type(**result_dict))
    except ResourceClosedError as e:
        print(e)
    return all_list


def sql_result_to_dict(result) -> list[dict]:
    all_list = []
    for row in result:
        result_dict = {}
        for key in result.keys():
            result_dict[key] = str(row[key])
        all_list.append(result_dict)
    return all_list


def build_select_query(entity: SQLModel, **kwargs):
    return select(entity).filter_by(**kwargs)


def build_delete_statement(entity: SQLModel, **kwargs):
    return delete(entity).filter_by(**kwargs)
