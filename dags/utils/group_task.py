from airflow.decorators import task_group, task
import logging
import random
from utils.parser import XMLParser
from airflow.models.xcom_arg import XComArg


@task
def create_random_dicts() -> list:
    """
    Создает список словарей с рандомными данными.
    """
    return [
        {"id": i, "name": f"RandomName_{i}", "value": random.uniform(0, 100)}
        for i in range(3)
    ]


@task_group
def process_data():
    """
    Группа задач с использованием mapped tasks.
    """
    # Получаем список словарей
    random_dicts = create_random_dicts()

    # Динамическое маппирование задачи XMLParser
    XMLParser.partial(task_id="test_xml_parser_task").expand(
        my_metadata=random_dicts  # Маппим каждый словарь
    )