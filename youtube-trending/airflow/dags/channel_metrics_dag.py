import sys
from datetime import datetime, timedelta

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import Param
from airflow.sdk.definitions.param import ParamsDict

from airflow import DAG
from elt.yt_videos import extract_channel_statistics, extract_channel_info_from_ids

def fail_task():
    sys.exit(1)

def extract_channel_info_task(**context):
    channel_ids = context["params"]["channel_ids"]
    extract_channel_info_from_ids(channel_ids)

def extract_channel_statistics_task(**context):
    channel_ids = context["params"]["channel_ids"]
    extract_channel_statistics(channel_ids)

with DAG(
    "Channel_Metrics",
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
    },
    description="Channel metrics",
    schedule=timedelta(days=1),
    start_date=datetime.today(),
    catchup=False,
    params=ParamsDict({
        "channel_ids": Param(type="array", items={"type": "string"})
    })
) as dag:
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
