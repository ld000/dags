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

dag = DAG('slice',
    schedule_interval='0 30 * * *',
    default_args=default_args)

level1_base_data = BashOperator(
    task_id='level1_base_data',
    bash_command='echo "level1_base_data..." | sleep 10',
    dag=dag)

level1_date = BashOperator(
    task_id='level1_date',
    bash_command='echo "level1_date..." | sleep 10',
    dag=dag)

level1_date_issue_device_no = BashOperator(
    task_id='level1_date_issue_device_no',
    bash_command='echo "level1_date_issue_device_no..." | sleep 10',
    dag=dag)

level1_date_issue_device_no.set_upstream(level1_date)

miss_n_false = BashOperator(
    task_id='miss_n_false',
    bash_command='echo "miss_n_false..." | sleep 10',
    dag=dag)

miss_n_false.set_upstream(level1_date)

level1_sensor = BashOperator(
    task_id='level1_sensor',
    bash_command='echo "level1_sensor..." | sleep 10',
    dag=dag)

level2 = BashOperator(
    task_id='level2',
    bash_command='echo "level2..." | sleep 10',
    dag=dag)

level2.set_upstream(level1_sensor)

level3 = BashOperator(
    task_id='level3',
    bash_command='echo "level3..." | sleep 10',
    dag=dag)

level3.set_upstream(level2)

# week
# month -> machineDistributionJob, machineDistributionBarJob
# season
# year

# machine event
