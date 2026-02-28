from datetime import datetime
from pathlib import Path
import pandas as pd

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator


# -----------------------------
# DAG Definition
# -----------------------------
with DAG(
    dag_id="pre_incremental_data_processing",
    start_date=datetime(2026, 2, 24),
    schedule="@daily",
    catchup=False,
    tags=["incremental", "etl"],
) as dag:

    # -----------------------------
    # Task 1: Fetch Incremental Data
    # -----------------------------
    fetch_events = BashOperator(
        task_id="fetch_events",
        bash_command="""
        mkdir -p /tmp/data &&
        echo "START={{ data_interval_start }} END={{ data_interval_end }}" &&
        curl -o /tmp/data/events_{{ ds }}.json \
        "http://events_api:5000/events?start_date={{ ds }}&end_date={{ next_ds }}"
        """
    )

    # -----------------------------
    # Task 2: Process Data
    # -----------------------------
    def _calculate_stats(input_path, output_path):
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        events = pd.read_json(input_path)

        stats = (
            events.groupby(["date", "user"])
            .size()
            .reset_index(name="count")
        )

        stats.to_csv(output_path, index=False)
        print(f"Saved output to {output_path}")

    calculate_stats = PythonOperator(
        task_id="calculate_stats",
        python_callable=_calculate_stats,
        op_kwargs={
            "input_path": "/tmp/data/events_{{ ds }}.json",
            "output_path": "/tmp/data/output_{{ ds }}.csv",
        },
    )

    # -----------------------------
    # Dependency
    # -----------------------------
    fetch_events >> calculate_stats