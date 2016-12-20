# -*- coding: UTF-8 -*-

from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 1, 1),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'schedule_interval': timedelta(1),
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('machine_latest_info',
    schedule_interval='0 0 6/1 * *',
    default_args=default_args)

machine_latest_info = BashOperator(
    task_id='machine_latest_info',
    bash_command='echo "machine_latest_info..."',
    dag=dag)
