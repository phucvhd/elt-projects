import sys
from datetime import datetime

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

def extract_channel_info_task(**context):
    channel_ids = context["params"]["channel_ids"]
    extract_channel_info_from_ids(channel_ids)

def extract_channel_statistics_task(**context):
    channel_ids = context["params"]["channel_ids"]
    extract_channel_statistics(channel_ids)

dag = DAG(
    'Channel_Metrics',
    default_args=default_args,
    description='Channel metrics',
    start_date=datetime.today(),
    schedule=None,
    catchup=False,
    params=ParamsDict({
        "channel_ids": Param(type="array", items={"type": "string"})
    })
)

t1 = PythonOperator(
    task_id='extract_channel_info',
    python_callable=extract_channel_info_task,
    dag=dag,
)

t2 = PythonOperator(
    task_id='extract_channel_statistics',
    python_callable=extract_channel_statistics_task,
    dag=dag,
)

t1 >> t2
