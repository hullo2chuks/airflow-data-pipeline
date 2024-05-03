import logging


class TestDataQuality():
    TABLES = ["songplays", "artists", "time", "users", "songs"]

    def __init__(self, tables=None):
        self.tables = tables or self.TABLES

    @staticmethod
    def validate(records, table):
        if len(records) < 1 or len(records[0]) < 1:
            raise ValueError(f"Data quality check failed. {table} returned no results")
        num_records = records[0][0]
        if num_records < 1:
            raise ValueError(f"Data quality check failed. {table} contained 0 rows")
        logging.info(f"Data quality on table {table} check passed with {records[0][0]} records")
