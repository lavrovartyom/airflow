import logging
from pathlib import Path

from airflow import DAG
from airflow.decorators import task
from airflow.models.xcom import XCom
from airflow.utils.trigger_rule import TriggerRule


def task_success_alert(context):
    ti = context["ti"]
    push_xcom(ti, "email_notification", "success")


def task_failure_alert(context):
    ti = context["ti"]
    push_xcom(ti, "email_notification", "failed")


def push_xcom(ti, key, value):
    ti.xcom_push(key=key, value=value)


with DAG(
    dag_id=Path(__file__).name,
) as dag:

    @task(
        on_failure_callback=task_failure_alert, on_success_callback=task_success_alert
    )
    def task_1() -> None:
        logging.info("Начало работы задачи - 2!")

    @task(
        on_failure_callback=task_failure_alert, on_success_callback=task_success_alert
    )
    def task_2():
        logging.info("Начало работы задачи - 2!")
        a = 5 / 0

    @task(trigger_rule=TriggerRule.ALL_DONE)
    def final_task(ti):
        xcoms = XCom.get_many(run_id=ti.get_dagrun().run_id)
        sorted_xcoms = sorted(xcoms, key=lambda x: x.timestamp)

        logging.info(f"Найдено {xcoms.count()} записей в XCom.")

        for i, task in enumerate(sorted_xcoms, start=1):
            logging.info(
                f"Задача {task.task_id} под номером {i} завершилась со статусом - {task.value}"
            )

    task_1() >> task_2() >> final_task()
