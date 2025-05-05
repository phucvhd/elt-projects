from datetime import datetime

from airflow.providers.standard.operators.python import PythonOperator

from airflow import DAG
from elt.yt_videos import elt_trending_video, elt_video_categories

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'elt_and_dbt',
    default_args=default_args,
    description='An ELT workflow with dbt',
    start_date=datetime(2025, 4, 29),
    catchup=False,
)

t1 = PythonOperator(
    task_id='elt_trending_video',
    python_callable=elt_trending_video,
    dag=dag,
)

t2 = PythonOperator(
    task_id='elt_video_categories',
    python_callable=elt_video_categories,
    dag=dag,
)

t1 >> t2