import sys
from datetime import datetime

from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import Param
from airflow.sdk.definitions.param import ParamsDict

from airflow import DAG
from elt.yt_videos import extract_channel_statistics, extract_channel_info_from_ids

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False
}

def fail_task():
    sys.exit(1)

def extract_top_channel_statistics_task():
    extract_channel_statistics(channel_ids)

dag = DAG(
    'Channel_Metrics',
    default_args=default_args,
    description='Channel metrics',
    start_date=datetime.today(),
    schedule=None,
    catchup=False
)

t1 = BashOperator(
    task_id='dbt_top_channels',
    bash_command="""
    docker run --rm \
    -v /Users/vuhoangdinhphuc/Documents/Data_engineering/elt-projects/youtube-trending/youtube_trending_dbt:/opt/airflow/youtube_trending_dbt \
    --network bridge \
    ghcr.io/dbt-labs/dbt-postgres:1.6.0 \
    run --select top_channels \
    --project-dir /opt/airflow/youtube_trending_dbt \
    --profiles-dir /opt/airflow/youtube_trending_dbt \
    --full-refresh
    """,
    dag=dag
)

t2 = PythonOperator(
    task_id='extract_channel_statistics',
    python_callable=extract_channel_statistics_task,
    dag=dag,
)

t1 >> t2
