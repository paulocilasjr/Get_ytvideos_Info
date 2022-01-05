from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator

from __main__ import main

default_args = {
'owner'                 : 'airflow',
'description'           : 'Crawler using Scrapy Python',
'depend_on_past'        : False,
'start_date'            : datetime(2022, 1, 4),
'email_on_failure'      : False,
'email_on_retry'        : False,
'retries'               : 1,
'retry_delay'           : timedelta(minutes=5)
}

getvideo_scraper = '/opt/airflow/dags/tasks'

with DAG('go_spider_operator_dag', default_args=default_args, schedule_interval='*/5 * * * *', catchup=False) as dag:
    start_dag = DummyOperator(
        task_id='start_dag'
        )

    end_dag = DummyOperator(
        task_id='end_dag'
        )        

    t1 = BashOperator(
    task_id='scrape_yt_videos',
    bash_command='cd {} && scrapy crawl getvideos-spider'.format(getvideo_scraper),
    )
        
    start_dag >> t1 

    t1 >> end_dag