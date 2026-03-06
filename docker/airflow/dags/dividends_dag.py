import datetime
import logging

from airflow.decorators import dag, task

from config.settings import Settings
from src.clients.moex_api_client import MOEXApiClient
from src.clients.moex_api_mapper import MOEXAPIMapper
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.clickhouse_data_checker import ClickHouseDataChecker
from src.db.postgres_dao import PostgresDAO
from src.models.moex_models.dividend import Dividend


@dag(
    start_date=datetime.datetime(2026, 2, 27),
    catchup=False,
    schedule="@daily",
    params={"secid": "SBER"},
)
def get_dividends_dag():
    @task()
    def get_dividends_by_security_from_moex(**kwargs):
        moex_rest_client = MOEXApiClient()
        moex_mapper = MOEXAPIMapper()

        params = kwargs["params"]
        secid = params["secid"]

        try:
            dividends = moex_rest_client.get_dividends_by_security(
                params={},
                secid=secid,
                moex_mapper=moex_mapper,
            )
            logger.info(dividends)
            logger.info(len(dividends))
        except Exception as e:
            logger.error(f"Ошибка при загрузке дивидендов по secid={secid} | {e}", exc_info=True)
            raise Exception(f"Ошибка при загрузке дивидендов по secid={secid} | {e}")
        else:
            return [
                dividend.model_dump() for dividend in dividends
            ]  # таски в даге не могут передавать pydantic модель между друг другом

    @task()
    def insert_dividends_clickhouse(dividends_dump, **kwargs):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)

        params = kwargs["params"]
        secid = params["secid"]

        dividends = [Dividend(**c) for c in dividends_dump]

        try:
            clickhouse_dao.insert_corporate_actions(dividends)
            logger.info("Вставлены дивиденды в clickhouse")
        except Exception as e:
            logger.error(
                f"Ошибка при вставке дивидендов в БД ClickHouse по secid={secid} | {e}",
                exc_info=True,
            )
            raise Exception(
                f"Ошибка при вставке дивидендов в БД ClickHouse по secid={secid}  | {e}"
            )
        else:
            return len(dividends)

    @task()
    def insert_dividends_postgres(dividends_dump, **kwargs):
        settings = Settings()
        postgres_dao = PostgresDAO(settings)

        params = kwargs["params"]
        secid = params["secid"]

        dividends = [Dividend(**c) for c in dividends_dump]

        try:
            postgres_dao.insert_corporate_actions(dividends)
            logger.info("Вставлены дивиденды в postgres")
        except Exception as e:
            logger.error(
                f"Ошибка при вставке дивидендов в БД PostgreSQL по secid={secid} | {e}",
                exc_info=True,
            )
            raise Exception(
                f"Ошибка при вставке дивидендов в БД PostgreSQL по secid={secid}  | {e}"
            )
        else:
            return len(dividends)

    @task()
    def check_data_dividends_clickhouse(len_dividends, **kwargs):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)
        clickhouse_data_checker = ClickHouseDataChecker(clickhouse_dao)

        params = kwargs["params"]
        secid = params["secid"]

        try:
            clickhouse_data_checker.check_data_exists_by_secid(
                table="corporate_actions", secid=secid, data_length=len_dividends
            )
        except Exception as e:
            logger.error(e)
            raise Exception(e)
        else:
            logger.info(f"Проверка на наличе данных дивидендов по secid={secid} успешно завершена")

    dividends = get_dividends_by_security_from_moex()
    len_dividends_clickhouse = insert_dividends_clickhouse(dividends)
    len_dividends_postgres = insert_dividends_postgres(dividends)
    check_data_dividends_clickhouse(len_dividends_clickhouse)


logger = logging.getLogger(__name__)
get_dividends_dag()
