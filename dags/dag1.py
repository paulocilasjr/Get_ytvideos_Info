from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator

from tasks.go_spider import main

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

with DAG('go_spider_operator_dag', default_args=default_args, schedule_interval='*/5 * * * *', catchup=False) as dag:
    start_dag = DummyOperator(
        task_id='start_dag'
        )

    end_dag = DummyOperator(
        task_id='end_dag'
        )        

    t1 = BashOperator(
        task_id='move_to_directory',
        bash_command='cd /opt/airflow/dags/tasks',
    )
    
    t2 = BashOperator(
        task_id='go_spider_command',
        bash_command='python go_spider.py',
    )
    
    #t2 = PythonOperator(
    #    task_id='spider-go',
    #    python_callable=main
    #    )
    
    #t1 = DockerOperator(
    #    task_id='docker_command_go_spider',
    #    image='go_spider_image',
    #    container_name='go_spider_image',
    #    api_version='auto',
    #    auto_remove=True,
    #    command="echo done",
    #    docker_url="unix://var/run/docker.sock",
    #    network_mode="bridge"
    #    )
        
    start_dag >> t1 

    t1 >> end_dag