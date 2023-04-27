#!/usr/bin/env python
import pytest

from omymodels import create_models


ddl = """
create table category
(
    name         varchar(64)              default ''::character varying not null,
    description  varchar(512)             default ''::character varying not null,
    status       varchar(64)              default ''::character varying not null,
    creator_id   varchar(64)              default ''::character varying not null,
    created_at   timestamp with time zone default CURRENT_TIMESTAMP     not null,
    updated_at   timestamp with time zone default CURRENT_TIMESTAMP     not null,
    is_valid     boolean                  default true                  not null,
    u_id         varchar(64)              default ''::character varying not null,
    archive_time timestamp with time zone
);
"""


@pytest.mark.skip
def test_create_model():
    result = create_models(ddl, models_type="pydantic")["code"]
    print(result)
