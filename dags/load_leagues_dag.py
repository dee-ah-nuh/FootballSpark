from __future__ import annotations
from pathlib import Path
import sys

DAGS_DIR = Path(__file__).resolve().parent
DATA_DIR = (DAGS_DIR / ".." / "football-and-spark" / "backend" / "data").resolve()
UTILS_DIR = (DAGS_DIR / ".." / "football-and-spark" / "backend" / "database" / "utils").resolve()

for p in (DATA_DIR, UTILS_DIR):
    if not p.exists():
        raise RuntimeError(f"Missing mount: {p}")
    sys.path.insert(0, str(p))

from get_all_leagues import get_leagues_etl 


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

default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	'start_date': datetime(2025, 1, 1),
	'retries': 1,
	'retry_delay': timedelta(minutes=1),
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
