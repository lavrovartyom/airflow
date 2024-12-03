from airflow.models.baseoperator import BaseOperator


class XMLParser(BaseOperator):
    template_fields = ('metadata',)

    def __init__(
            self,
            xsl_file: str,
            source_folder: str,
            metadata: dict[str, str],
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.xsl_file = xsl_file
        self.source_folder = source_folder
        self.metadata = metadata

    # def _load_metadata(self, metadata: list[dict]) -> list[dict]:
    #     self.log.info("вызвался метод лоад")
    #     return self.my_metadata

    def execute(self, context):
        """
        Логика выполнения задачи.
        """
        self.log.info(f"Обрабатываю данные: {self.metadata}")
        self.log.info(f"Source folder: {self.source_folder}")
        self.log.info(f"XSLT файл: {self.xsl_file}")
