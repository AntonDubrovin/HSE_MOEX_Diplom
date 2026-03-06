import datetime
import logging

from airflow.decorators import dag, task

from config.settings import Settings
from src.clients.moex_api_client import MOEXApiClient
from src.clients.moex_api_mapper import MOEXAPIMapper
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.clickhouse_data_checker import ClickHouseDataChecker
from src.db.postgres_dao import PostgresDAO
from src.models.moex_models.index import Index


@dag(
    start_date=datetime.datetime(2026, 2, 23),
    schedule="@daily",
    catchup=False,
    params={
        "engine": "stock",
        "market": "index",
        "board": "SNDX",
    },
)
def get_index_dag():
    @task()
    def get_index_by_security_from_moex(**kwargs):
        moex_rest_client = MOEXApiClient()
        moex_mapper = MOEXAPIMapper()

        params = kwargs["params"]
        engine = params["engine"]
        market = params["market"]
        board = params["board"]

        try:
            indices = moex_rest_client.get_indices(
                params={"securities.columns": "SECID,SHORTNAME"},
                board=board,
                engine=engine,
                market=market,
                moex_mapper=moex_mapper,
            )
            logger.info(indices)
            logger.info(len(indices))
        except Exception as e:
            logger.error(f"Ошибка при загрузке индексов | {e}", exc_info=True)
            raise Exception(f"Ошибка при загрузке индексов | {e}")
        else:
            return [
                index.model_dump() for index in indices
            ]  # таски в даге не могут передавать pydantic модель между друг другом

    @task()
    def insert_index_clickhouse(indices_dump):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)

        indices = [Index(**c) for c in indices_dump]

        try:
            clickhouse_dao.insert_indices(indices)
            logger.info("Вставлены индексы в clickhouse")
        except Exception as e:
            logger.error(f"Ошибка при вставке индексов в БД ClickHouse | {e}", exc_info=True)
            raise Exception(f"Ошибка при вставке индексов в БД ClickHouse | {e}")
        else:
            return len(indices)

    @task()
    def insert_index_postgres(indices_dump):
        settings = Settings()
        postgres_dao = PostgresDAO(settings)

        indices = [Index(**c) for c in indices_dump]

        try:
            postgres_dao.insert_indices(indices)
            logger.info("Вставлены индексы в postgres")
        except Exception as e:
            logger.error(f"Ошибка при вставке индексов в БД PostgreSQL | {e}", exc_info=True)
            raise Exception(f"Ошибка при вставке индексов в БД PostgreSQL  | {e}")
        else:
            return len(indices)

    @task()
    def check_data_index_clickhouse(len_indices):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)
        clickhouse_data_checker = ClickHouseDataChecker(clickhouse_dao)

        try:
            clickhouse_data_checker.check_data_exists(table="indices_ref", data_length=len_indices)
        except Exception as e:
            logger.error(e)
            raise Exception(e)
        else:
            logger.info(f"Проверка на наличе данных индексов в ClickHouse успешно завершена")

    indicies = get_index_by_security_from_moex()
    len_indicies_clickhouse = insert_index_clickhouse(indicies)
    len_indicies_postgres = insert_index_postgres(indicies)
    check_data_index_clickhouse(len_indicies_clickhouse)


logger = logging.getLogger(__name__)
get_index_dag()
