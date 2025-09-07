from airflow import DAG
# Airflow 3.x
from airflow.providers.standard.operators.python import (
    PythonOperator,
    BranchPythonOperator,
    ShortCircuitOperator,
    PythonVirtualenvOperator,
    ExternalPythonOperator,
)
from datetime import datetime, timedelta
import sys
import os

# Ensure the path to the ETL function is available
sys.path.append(os.path.join(os.path.dirname(__file__), '../football-and-spark/backend/data'))
print(os.getcwd())

# sys.path.append(os.path.join(os.path.dirname(__file__), '../football-and-spark/data'))
from get_all_leagues import get_leagues_etl

default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	'start_date': datetime(2025, 1, 1),
	'retries': 1,
	'retry_delay': timedelta(minutes=5),
}

with DAG(
	'load_leagues_dag',
	default_args=default_args,
	description='ETL DAG to load football leagues data',
	# schedule_interval='@daily',
	catchup=False,
) as dag:
	run_leagues_etl = PythonOperator(
		task_id='run_leagues_etl',
		python_callable=get_leagues_etl,
	)
