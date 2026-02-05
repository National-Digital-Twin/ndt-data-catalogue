# SPDX-License-Identifier: Apache-2.0
#
# This file is unmodified from its original version developed by Acryl Data, Inc.,
# and is now included as part of a repository maintained by the National Digital Twin Programme.
# All support, maintenance and further development of this code is now the responsibility
# of the National Digital Twin Programme.

from datetime import datetime

from airflow import DAG
from airflow.providers.teradata.operators.teradata import TeradataOperator

TERADATA_COST_TABLE = "costs"
TERADATA_PROCESSED_TABLE = "processed_costs"


def _fake_teradata_execute(*args, **kwargs):
    pass


with DAG(
    "teradata_operator",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    TeradataOperator.execute = _fake_teradata_execute

    transform_cost_table = TeradataOperator(
        teradata_conn_id="my_teradata",
        task_id="transform_cost_table",
        sql="""
        CREATE OR REPLACE TABLE {{ params.out_table_name }} AS
        SELECT
            id,
            month,
            total_cost,
            area,
            total_cost / area as cost_per_area
        FROM {{ params.in_table_name }}
        """,
        params={
            "in_table_name": TERADATA_COST_TABLE,
            "out_table_name": TERADATA_PROCESSED_TABLE,
        },
    )
