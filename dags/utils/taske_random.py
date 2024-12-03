from airflow.decorators import task
import random


@task
def create_random_dicts() -> dict[str, str | int]:
    """
    Создает список словарей с рандомными данными.
    """
    return {"id": 1, "name": f"RandomName_2", "value": "bla"}