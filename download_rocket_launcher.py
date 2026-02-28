import json
import pathlib
import requests
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

OUTPUT_DIR = "/opt/airflow/dags/output/rocket_output"

def download_launches():
    url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?limit=10&format=json"
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    with open(f"{OUTPUT_DIR}/launches.json", "w") as f:
        json.dump(response.json(), f)

def get_pictures():
    pathlib.Path(f"{OUTPUT_DIR}/images").mkdir(parents=True, exist_ok=True)

    with open(f"{OUTPUT_DIR}/launches.json") as f:
        launches = json.load(f)

    for i, launch in enumerate(launches.get("results", [])):
        image_url = launch.get("image")
        if image_url:
            response = requests.get(image_url, timeout=15)
            response.raise_for_status()

            with open(f"{OUTPUT_DIR}/images/image_{i}.jpg", "wb") as img:
                img.write(response.content)

with DAG(
    dag_id="download_rocket_launches",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id="download_launches",
        python_callable=download_launches
    )

    t2 = PythonOperator(
        task_id="get_pictures",
        python_callable=get_pictures
    )

    t1 >> t2