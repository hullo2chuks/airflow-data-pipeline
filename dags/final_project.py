from datetime import datetime, timedelta
import pendulum
from airflow.models import Variable
from airflow.decorators import dag
from airflow.operators.dummy_operator import DummyOperator

from helpers.test_data_quality import TestDataQuality
from helpers.sql_queries import SqlQueries

from operators.stage_redshift import StageToRedshiftOperator
from operators.load_fact import LoadFactOperator
from operators.load_dimension import LoadDimensionOperator
from operators.data_quality import DataQualityOperator


default_args = {
    'owner': 'Philip',
    'start_date': pendulum.datetime(2018, 11, 1, 0, 0, 0),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_retry': False
}
s3_bucket = Variable.get('s3_bucket')


@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *'
)
def final_project():
    start_operator = DummyOperator(task_id='Begin_execution')
    end_operator = DummyOperator(task_id='End_execution')

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        table="staging_events",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket=s3_bucket,
        s3_key="log-data/{executed_date.year}/{executed_date.month}",
        data_format="JSON 's3://philip-dags/log_json_path.json'"
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        table="staging_songs",
        redshift_conn_id="redshift",
        aws_credentials_id="aws_credentials",
        s3_bucket=s3_bucket,
        s3_key="song-data",
        data_format="JSON 'auto'"
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        table="songplays",
        redshift_conn_id="redshift",
        sql=SqlQueries.songplay_table_insert
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        table="users",
        redshift_conn_id="redshift",
        sql=SqlQueries.user_table_insert
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        table="songs",
        redshift_conn_id="redshift",
        sql=SqlQueries.song_table_insert
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        table="artists",
        redshift_conn_id="redshift",
        sql=SqlQueries.artist_table_insert
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        table="time",
        redshift_conn_id="redshift",
        sql=SqlQueries.time_table_insert
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        redshift_conn_id="redshift",
        test=TestDataQuality(["songplays", "artists", "time", "users", "songs"])
    )

    start_operator >> stage_events_to_redshift
    start_operator >> stage_songs_to_redshift

    stage_events_to_redshift >> load_songplays_table
    stage_songs_to_redshift >> load_songplays_table

    load_songplays_table >> load_user_dimension_table
    load_songplays_table >> load_song_dimension_table
    load_songplays_table >> load_artist_dimension_table
    load_songplays_table >> load_time_dimension_table

    load_user_dimension_table >> run_quality_checks
    load_song_dimension_table >> run_quality_checks
    load_artist_dimension_table >> run_quality_checks
    load_time_dimension_table >> run_quality_checks

    run_quality_checks >> end_operator


final_project_dag = final_project()
