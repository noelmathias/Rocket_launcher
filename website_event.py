from datetime import datetime,timedelta
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

dag= DAG(
    dag_id="01_unsheduled",
    start_date=datetime(2026,1,1),
    schedule=None,
)

fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command="curl -o /opt/airflow/dags/output/events.csv -L 'https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv'",
)

def _calculate_stats(input_path, output_path):
    Path(output_path).parent.mkdir(exist_ok=True)

    events = pd.read_csv(input_path)

    print(events.head())  # helpful debug

    result = events.describe()  # simple stats

    result.to_csv(output_path)

calculate_stats = PythonOperator(
    task_id="calculate_stats",
    python_callable=_calculate_stats,
    op_kwargs={
        "input_path": "/tmp/events.csv",
        "output_path": "/opt/airflow/dags/output/event_stats.csv",
    },
    dag=dag,
)

fetch_events >> calculate_stats