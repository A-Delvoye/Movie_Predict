from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

BASE_PATH = "/opt/airflow/Movie_Predict/moviescraper/moviescraper/spiders"

default_args = {
    "owner": "gauthier",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

def run_project(path, script_name):
    print('###################################')
    print(BASE_PATH)
    if path not in sys.path:
        sys.path.append(path)

    script_path = os.path.join(path, f"{script_name}.py")
    print('-'*50)
    print(script_path)
    if not os.path.isfile(script_path):
        print('~'*50)
        print(f">>> Looking for script at: {script_path}")
        raise FileNotFoundError(f"Script {script_path} not found")
    print('='*50)
    print(f"Running script: {script_path}")
    with open(script_path) as f:
        code = compile(f.read(), script_path, 'exec')
        exec(code, {"__name__": "__main__"})

with DAG(
    dag_id="multi_scrapy_dag",
    default_args=default_args,
    start_date=datetime(2024, 4, 15),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="scrape_movies",
        python_callable=run_project,
        op_args=[BASE_PATH, "runner"],  # runner = runner.py
    )