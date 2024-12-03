from airflow import DAG
from utils.group_task import process_data


with DAG(dag_id="DAG_MAPPED") as dag:

    process_data()
