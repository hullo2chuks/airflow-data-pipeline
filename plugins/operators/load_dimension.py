from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class LoadDimensionOperator(BaseOperator):
    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 table="",
                 sql="",
                 append_only=False,
                 *args, **kwargs):
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql = sql
        self.append_only = append_only

    def execute(self, context):
        redshift_hook = PostgresHook(self.redshift_conn_id)
        self.log.info("Clearing data from destination Redshift table")
        if not self.append_only:
            redshift_hook.run("TRUNCATE {}".format(self.table))
            self.log.info(f"Clearing data from destination {self.table} table")

        self.log.info(f"Insert into the {self.table} table")
        redshift_hook.run(f"INSERT INTO {self.table} {self.sql}")
