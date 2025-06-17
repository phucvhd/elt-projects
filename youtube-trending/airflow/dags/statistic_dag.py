import sys
from datetime import datetime

from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

from airflow import DAG

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

def fail_task():
    sys.exit(1)

dag = DAG(
    'Daily_DBT',
    default_args=default_args,
    description='Daily_DBT',
    start_date=datetime(2025, 6, 12),
    schedule=None,
    catchup=False,
)

t1 = DockerOperator(
    task_id='dbt_trending_streak',
    image='ghcr.io/dbt-labs/dbt-postgres:1.6.0',
    command=[
        "run",
        "--select",
        "trending_streak",
        "--project-dir",
        "/opt/airflow/youtube_trending_dbt",
        "--profiles-dir",
        "/opt/airflow/youtube_trending_dbt/",
        "--full-refresh"
    ],
    mounts=[
        Mount(
            source='/Users/vuhoangdinhphuc/Documents/Data_engineering/elt-projects/youtube-trending/youtube_trending_dbt',
            target='/opt/airflow/youtube_trending_dbt/',
            type='bind'
        )
    ],
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    dag=dag
)

t2 = DockerOperator(
    task_id='dbt_popular_category',
    image='ghcr.io/dbt-labs/dbt-postgres:1.6.0',
    command=[
        "run",
        "--select",
        "popular_category",
        "--project-dir",
        "/opt/airflow/youtube_trending_dbt",
        "--profiles-dir",
        "/opt/airflow/youtube_trending_dbt/",
        "--full-refresh"
    ],
    mounts=[
        Mount(
            source='/Users/vuhoangdinhphuc/Documents/Data_engineering/elt-projects/youtube-trending/youtube_trending_dbt',
            target='/opt/airflow/youtube_trending_dbt/',
            type='bind'
        )
    ],
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    dag=dag
)

t1 >> t2