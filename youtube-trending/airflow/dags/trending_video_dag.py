import sys
from datetime import datetime, date

from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from docker.types import Mount

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
    start_date=datetime(2025, 4, 29),
    catchup=False,
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

t5 = BashOperator(
    task_id='dbt_trending_streak',
    bash_command="""
    docker run --rm \
    -v /Users/vuhoangdinhphuc/Documents/Data_engineering/elt-projects/youtube-trending/youtube_trending_dbt:/opt/airflow/youtube_trending_dbt \
    --network bridge \
    ghcr.io/dbt-labs/dbt-postgres:1.6.0 \
    run --select trending_streak \
    --project-dir /opt/airflow/youtube_trending_dbt \
    --profiles-dir /opt/airflow/youtube_trending_dbt \
    --full-refresh
    """,
    dag=dag
)

t6 = BashOperator(
    task_id='dbt_popular_category',
    bash_command="""
    docker run --rm \
    -v /Users/vuhoangdinhphuc/Documents/Data_engineering/elt-projects/youtube-trending/youtube_trending_dbt:/opt/airflow/youtube_trending_dbt \
    --network bridge \
    ghcr.io/dbt-labs/dbt-postgres:1.6.0 \
    run --select popular_category \
    --project-dir /opt/airflow/youtube_trending_dbt \
    --profiles-dir /opt/airflow/youtube_trending_dbt \
    --full-refresh
    """,
    dag=dag
)

t7 = BashOperator(
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

t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7