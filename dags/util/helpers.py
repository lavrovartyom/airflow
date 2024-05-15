import typing as t
from functools import wraps

from airflow.exceptions import AirflowFailException
from airflow.operators.python import get_current_context
from airflow.utils.db import provide_session


def track_status_task(func: t.Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        context = get_current_context()
        ti = context["ti"]
        try:
            result = func(*args, **kwargs)
            push_xcom(ti, "email_notification", "success")
            return result
        except Exception as e:
            push_xcom(ti, "email_notification", "failed")
            raise AirflowFailException(
                f"Задача в функции: {func.__name__}, завершилась c ошибкой: {e} "
            ) from e

    return wrapper


@provide_session
def push_xcom(ti, key, value, session=None):
    ti.xcom_push(key=key, value=value)
