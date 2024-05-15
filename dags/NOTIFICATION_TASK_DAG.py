from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import logging


@dag(schedule_interval="@daily", start_date=days_ago(1), catchup=False, dag_id="NOTIFICATION_TASK_DAG")
def example_dag():
    @task
    def producer_task() -> str:
        # Производство данных
        return "Передача тестового сообщения!"

    @task
    def consumer_task(data: str) -> None:
        # Потребление данных
        logging.info(data)

    # Правильное использование зависимостей и передачи данных
    data = producer_task()
    consumer_task(data)


dag_instance = example_dag()
