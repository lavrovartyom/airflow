from airflow.models.baseoperator import BaseOperator


class XMLParser(BaseOperator):
    def __init__(self, my_metadata: list[dict], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.my_metadata = my_metadata

    def execute(self, context):
        """
        Логика выполнения задачи.
        """
        self.log.info(f"Обрабатываю данные: {self.my_metadata}")

