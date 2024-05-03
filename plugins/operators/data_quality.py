from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from helpers.test_data_quality import TestDataQuality


class DataQualityOperator(BaseOperator):
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 test: TestDataQuality = None,
                 *args, **kwargs):
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.test = test

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)

        for table in self.test.tables:
            records = redshift_hook.get_records(f"SELECT COUNT(*) FROM {table}")
            self.test.validate(records, table)
