import logging
from pathlib import Path

from airflow import DAG
from airflow.decorators import task
from airflow.models.xcom import XCom
from airflow.utils.dates import days_ago
from airflow.utils.trigger_rule import TriggerRule
from util.helpers import track_status_task


def on_failure_callback(context):
    ti = context["ti"]
    push_xcom(ti, "email_notification", "failed")
    # Дополнительно можно добавить отправку уведомления здесь


def on_success_callback(context):
    ti = context["ti"]
    push_xcom(ti, "email_notification", "success")
    # Дополнительно можно добавить отправку уведомления здесь


def push_xcom(ti, key, value):
    ti.xcom_push(key=key, value=value)


with DAG(dag_id=Path(__file__).name, tags=["ДАГ рассылки уведомлений"]) as dag:

    @task(
        on_failure_callback=on_failure_callback, on_success_callback=on_success_callback
    )
    def producer_task() -> None:
        logging.info("Начало работы задачи!")
        # a = 5 / 0

    @task(
        on_failure_callback=on_failure_callback, on_success_callback=on_success_callback
    )
    def test_fail_task():
        logging.info("Начало работы задачи!")
        # a = 5 / 0

    @task(trigger_rule=TriggerRule.ALL_DONE)
    def final_task(ti):
        xcoms = XCom.get_many(run_id=ti.get_dagrun().run_id)
        sorted_xcoms = sorted(xcoms, key=lambda x: x.timestamp)

        logging.info(f"Найдено {xcoms.count()} записей в XCom.")

        for i, task in enumerate(sorted_xcoms, start=1):
            logging.info(
                f"Задача {task.task_id} под номером {i} завершилась со статусом - {task.value}"
            )

    producer_task() >> test_fail_task() >> final_task()

    # @task
    # @track_status_task
    # def producer_task() -> None:
    #     logging.info("Начало работы задачи!")
    #     # a = 5 / 0
    #
    # @task
    # @track_status_task
    # def test_fail_task():
    #     logging.info("Начало работы задачи!")
    #
    #     a = 5 / 0
    #
    # @task(trigger_rule=TriggerRule.ALL_DONE)
    # def final_task(ti):
    #     xcoms = XCom.get_many(run_id=ti.get_dagrun().run_id)
    #     sorted_xcoms = sorted(xcoms, key=lambda x: x.timestamp)
    #
    #     logging.info(f"Найдено {xcoms.count()} записей в XCom.")
    #
    #     for i, task in enumerate(sorted_xcoms, start=1):
    #         logging.info(
    #             f"Задача {task.task_id} под номером {i} завершилась со статусом - {task.value}"
    #         )

    #
    # producer_task() >> test_fail_task() >> final_task()
