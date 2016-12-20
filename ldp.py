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

dag = DAG('ldp',
    schedule_interval='0 10 * * *',
    default_args=default_args)

# -------------- gpsNo, deviceNo 对照 begin --------------
gps_contrast = BashOperator(
    task_id='gpsnoContrastJob',
    bash_command='echo "nvr gpsNo deviceNo contrast..." | sleep 5',
    dag=dag)

gps_contrast_kmx = BashOperator(
    task_id='gpsContrastJob',
    bash_command='echo "nvr gpsNo template by kmx..." | sleep 5',
    dag=dag)

gps_contrast_kmx.set_upstream(gps_contrast)
# -------------- gpsNo, deviceNo 对照 end --------------

# -------------- ldp 数据 begin --------------
chan_net_list = BashOperator(
    task_id='lgChannetListJob',
    bash_command='echo "ldp chan_net_list..." | sleep 5',
    dag=dag)

chan_net_list.set_upstream(gps_contrast_kmx)

city_list = BashOperator(
    task_id='lgCityListJob',
    bash_command='echo "ldp city_list..." | sleep 5',
    dag=dag)

city_list.set_upstream(gps_contrast_kmx)

customer_list = BashOperator(
    task_id='lgCustomerListJob',
    bash_command='echo "ldp customer_list..." | sleep 5',
    dag=dag)

customer_list.set_upstream(gps_contrast_kmx)

# -------------------------------------------------------------
dealer_in_chan_net_list = BashOperator(
    task_id='lgDealerInChannetJob',
    bash_command='echo "ldp dealer_in_chan_net_list..." | sleep 5',
    dag=dag)

dealer_in_chan_net_list.set_upstream(gps_contrast_kmx)

dealer_province = BashOperator(
    task_id='dealerProvinceJob',
    bash_command='echo "ldp dealer_province..." | sleep 5',
    dag=dag)

dealer_province.set_upstream(dealer_in_chan_net_list)
# -------------------------------------------------------------

machine_trans_his = BashOperator(
    task_id='lgMachineTransHisJob',
    bash_command='echo "ldp machine_trans_his..." | sleep 5',
    dag=dag)

machine_trans_his.set_upstream(dealer_in_chan_net_list)

fault_class = BashOperator(
    task_id='lgFaultClassJob',
    bash_command='echo "ldp fault_class..." | sleep 5',
    dag=dag)

fault_class.set_upstream(gps_contrast_kmx)

inspection_history = BashOperator(
    task_id='lgInspectionHistoryJob',
    bash_command='echo "ldp inspection_history..." | sleep 5',
    dag=dag)

inspection_history.set_upstream(gps_contrast_kmx)

machine_profile = BashOperator(
    task_id='lgMachineProfileJob',
    bash_command='echo "ldp machine_profile..." | sleep 5',
    dag=dag)

machine_profile.set_upstream(gps_contrast_kmx)

machine_type = BashOperator(
    task_id='lgMachineTypeJob',
    bash_command='echo "ldp machine_type..." | sleep 5',
    dag=dag)

machine_type.set_upstream(gps_contrast_kmx)

overdue_machine = BashOperator(
    task_id='lgOverdueMachineJob',
    bash_command='echo "ldp overdue_machine..." | sleep 5',
    dag=dag)

overdue_machine.set_upstream(gps_contrast_kmx)

product_type = BashOperator(
    task_id='lgProductTypeJob',
    bash_command='echo "ldp product_type..." | sleep 5',
    dag=dag)

product_type.set_upstream(gps_contrast_kmx)

repair_history = BashOperator(
    task_id='lgRepairHistoryJob',
    bash_command='echo "ldp repair_history..." | sleep 5',
    dag=dag)

repair_history.set_upstream(gps_contrast_kmx)

replace_history = BashOperator(
    task_id='lgReplaceHistoryJob',
    bash_command='echo "ldp replace_history..." | sleep 5',
    dag=dag)

replace_history.set_upstream(gps_contrast_kmx)

service_history = BashOperator(
    task_id='lgServiceHistoryJob',
    bash_command='echo "ldp service_history..." | sleep 5',
    dag=dag)

service_history.set_upstream(gps_contrast_kmx)

# -------------------------------------------------------------
supply_in_chan_net = BashOperator(
    task_id='lgSupplyInChannetJob',
    bash_command='echo "ldp supply_in_chan_net..." | sleep 5',
    dag=dag)

supply_in_chan_net.set_upstream(gps_contrast_kmx)

supply_province = BashOperator(
    task_id='supplyProvinceJob',
    bash_command='echo "ldp supply_province..." | sleep 5',
    dag=dag)

supply_province.set_upstream(supply_in_chan_net)
# -------------------------------------------------------------

upkeep_history = BashOperator(
    task_id='lgUpkeepHistoryJob',
    bash_command='echo "ldp upkeep_history..." | sleep 5',
    dag=dag)

upkeep_history.set_upstream(gps_contrast_kmx)

machine_work_status = BashOperator(
    task_id='MachineWorkStatusJob',
    bash_command='echo "ldp machine_work_status..." | sleep 5',
    dag=dag)

machine_work_status.set_upstream(upkeep_history)
machine_work_status.set_upstream(service_history)
machine_work_status.set_upstream(machine_profile)

machine_dimension = BashOperator(
    task_id='lgMachineDimensionJob',
    bash_command='echo "ldp machine_dimension..." | sleep 5',
    dag=dag)

machine_dimension.set_upstream(machine_work_status)
machine_dimension.set_upstream(fault_class)
machine_dimension.set_upstream(product_type)
machine_dimension.set_upstream(repair_history)
machine_dimension.set_upstream(machine_trans_his)
machine_dimension.set_upstream(machine_type)
machine_dimension.set_upstream(inspection_history)
machine_dimension.set_upstream(chan_net_list)
machine_dimension.set_upstream(city_list)
machine_dimension.set_upstream(replace_history)
machine_dimension.set_upstream(customer_list)
machine_dimension.set_upstream(supply_in_chan_net)
machine_dimension.set_upstream(overdue_machine)
# -------------- ldp 数据 end --------------
