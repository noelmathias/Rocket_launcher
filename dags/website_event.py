from datetime import datetime,timedelta
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from scipy import stats

dag= DAG(
    dag_id="01_unsheduled",
    start_date=datetime(2026,1,1),
    schedule=None,
)

fetch_events=BashOperator(
    task_id="fetch_events",
    bash_command="curl -o /tmp/events.csv -L 'https://people.sc.fsu.edu/~jburkardt/data/csv/airtravel.csv'",
    dag=dag,
)

def _calculate_stats(input_path,output_path):
    Path(output_path).parent.mkdir(exist_ok=True)

    events =pd.read_json(input_path)
    stats = events.groupby(["date","user"]).size().reset_index()

    stats.to_csv(output_path,index=False)

calculate_stats=PythonOperator(
    task_id="calculate_stats",
    python_callable=_calculate_stats,
    op_kwargs={
        "input_path": "/tmp/events.json",
        "output_path": "/tmp/event_stats.csv",
    },
)

fetch_events >> calculate_stats