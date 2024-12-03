from airflow.decorators import task_group, task
from utils.parser import XMLParser
from airflow.models.xcom_arg import XComArg
from utils.taske_random import create_random_dicts


XSLT_FILES = ["contract_44fz.xsl", "contract_procedure.xsl", "contract_finansess.xsl", "contract_suplier.xsl"]


@task_group
def process_data(source_folder: str):
    """
    Группа задач с использованием mapped tasks.
    """
    metadata = create_random_dicts()

    XMLParser.partial(
        task_id="xml_parse",
        source_folder=source_folder,
        metadata=metadata
    ).expand(
        xsl_file=XSLT_FILES
    )
