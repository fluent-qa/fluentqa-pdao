#!/usr/bin/env python
import pytest
from qpybase.builtins import rendertools

from qpydao import *

seq = """
activity_answer_id_seq
calculation_file_id_seq
calculation_id_seq
calculation_item_id_seq
emission_item_id_seq
model_id_seq
parameter_id_seq
phase_id_seq
phase_snapshot_id_seq
product_id_seq
question_id_seq
question_option_id_seq
question_result_id_seq
question_rule_id_seq
r_calculation_parameter_id_seq
report_data_quality_and_sensitivity_id_seq
report_id_seq
report_phase_statement_id_seq
report_significant_issue_id_seq
report_uncertainty_statement_id_seq
result_id_seq
task_id_seq
unit_process_id_seq
unit_process_snapshot_id_seq
"""


def generate_postgre_seqs(schema_name: str, seqs: str):
    all_seq = seqs.split("\n")
    result = []
    for item in all_seq:
        if len(item) > 1:
            result.append(generate_postgres_seq(schema_name, item))
    return result


def generate_postgres_seq(
    schema_name: str, seq_name: str, table_name: str = None
) -> str:
    temp = "select setval('{}.{}'::regclass,max(id)) from {};"
    if table_name is None:
        table_name = seq_name.replace("_id_seq", "")
    return temp.format(schema_name, seq_name, table_name)


def test_seq():
    print(seq)
    result = generate_postgre_seqs("calculator", seq)
    for item in result:
        print(item)


query_field = """
SELECT a.attnum, a.attname AS field_name, t.typname AS field_type, a.attlen AS length, a.atttypmod AS lengthvar
    , a.attnotnull AS notnull, b.description AS comment
FROM pg_class c, pg_attribute a
    LEFT JOIN pg_description b
    ON a.attrelid = b.objoid
        AND a.attnum = b.objsubid, pg_type t
WHERE c.relname = '{}'
    AND a.attnum > 0
    AND a.attrelid = c.oid
    AND a.atttypid = t.oid
ORDER BY a.attnum;
"""

python_type_mapping = {"int": "int", "varchar": "str", "timestamp": "DateTime"}


def get_field_type(field_type: str):
    for k, v in python_type_mapping.items():
        if field_type.startswith(k):
            return v
    return "str"


TABLE_CLASS = """
class {{table_name}}(SQLModel, table=True):
    {% for field in fields -%}
      {{field.field_name}}: Optional[{{field.code_type}}] = {{field.code_value}}
    {% endfor %}
"""


@pytest.mark.skip
def test_db_model():
    db_config = DatabaseConfig(url="postgresql://postgres:changeit@localhost:7432/test_hub")
    pg = DatabaseClient(config=db_config)
    result = pg.query(query_field.format("api_monitor_record"))
    model_result = sql_result_to_model(result, models.FieldMeta)
    print(model_result)
    for model in model_result:
        if model.field_name == "id":
            model.code_type = get_field_type(model.field_type)
            model.code_value = " Field(default=None, primary_key=True)"
        else:
            model.code_type = get_field_type(model.field_type)
            model.code_value = "None"
    table_meta = models.TableMeta(table_name="ApiMonitorRecord", fields=model_result)
    class_txt = rendertools.render_template(TABLE_CLASS, table_meta.dict())
    print(class_txt)
