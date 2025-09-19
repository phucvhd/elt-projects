import sys
from datetime import datetime, date

from airflow.providers.standard.operators.python import PythonOperator

from airflow import DAG
from elt.yt_videos import extract_raw_trending_video, extract_video_categories, extract_channel_info, \
    transform_video_stats

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

def fail_task():
    sys.exit(1)

dag = DAG(
    'Daily_ELT',
    default_args=default_args,
    description='An ELT workflow',
    start_date=datetime.today(),
    catchup=False,
    schedule="0 0 * * *"
)

t1 = PythonOperator(
    task_id='extract_video_categories',
    python_callable=extract_video_categories,
    dag=dag,
)

t2 = PythonOperator(
    task_id='extract_raw_trending_video',
    python_callable=extract_raw_trending_video,
    dag=dag,
)

t3 = PythonOperator(
    task_id='extract_channel_info',
    python_callable=extract_channel_info,
    op_kwargs={"query_date": date.today()},
    dag=dag,
)

t4 = PythonOperator(
    task_id='transform_video_stats',
    python_callable=transform_video_stats,
    op_kwargs={"query_date": date.today()},
    dag=dag,
)

t1 >> t2 >> t3 >> t4