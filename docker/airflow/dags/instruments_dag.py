import datetime
import logging

from airflow.decorators import dag, task

from config.settings import Settings
from src.clients.moex_api_client import MOEXApiClient
from src.clients.moex_api_mapper import MOEXAPIMapper
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.clickhouse_data_checker import ClickHouseDataChecker
from src.db.postgres_dao import PostgresDAO
from src.models.moex_models.instrument import Instrument


@dag(
    start_date=datetime.datetime(2026, 2, 23),
    schedule="@daily",
    catchup=False,
    params={
        "engine": "stock",
        "market": "shares",
        "board": "TQBR",
    },
)
def get_instruments_dag():
    @task()
    def get_instruments_by_security_from_moex(**kwargs):
        moex_rest_client = MOEXApiClient()
        moex_mapper = MOEXAPIMapper()

        params = kwargs["params"]
        engine = params["engine"]
        market = params["market"]
        board = params["board"]

        try:
            instruments = moex_rest_client.get_instruments(
                params={
                    "securities.columns": "SECID,SECNAME,SHORTNAME,ISIN,SECTYPE,LOTSIZE,CURRENCYID,BOARDID"
                },
                engine=engine,
                market=market,
                board=board,
                moex_mapper=moex_mapper,
            )
            logger.info(len(instruments))
            logger.info(instruments)
        except Exception as e:
            logger.error(f"Ошибка при загрузке инструментов | {e}", exc_info=True)
            raise Exception(f"Ошибка при загрузке инструментов | {e}")
        else:
            return [
                instrument.model_dump() for instrument in instruments
            ]  # таски в даге не могут передавать pydantic модель между друг другом

    @task()
    def insert_instruments_clickhouse(instruments_dump):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)

        instruments = [Instrument(**c) for c in instruments_dump]

        try:
            clickhouse_dao.insert_instruments(instruments)
            logger.info("Вставлены инструменты в clickhouse")
        except Exception as e:
            logger.error(f"Ошибка при вставке инструментов в БД ClickHouse | {e}", exc_info=True)
            raise Exception(f"Ошибка при вставке инструментов в БД ClickHouse | {e}")
        else:
            return len(instruments)

    @task()
    def insert_instruments_postgres(instruments_dump):
        settings = Settings()
        postgres_dao = PostgresDAO(settings)

        instruments = [Instrument(**c) for c in instruments_dump]

        try:
            postgres_dao.insert_instruments(instruments)
            logger.info("Вставлены инструменты в postgres")

        except Exception as e:
            logger.error(f"Ошибка при вставке инструментов в БД PostgreSQL | {e}", exc_info=True)
            raise Exception(f"Ошибка при вставке инструментов в БД PostgreSQL  | {e}")
        else:
            return len(instruments)

    @task()
    def check_data_instruments_clickhouse(len_instruments):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)
        clickhouse_data_checker = ClickHouseDataChecker(clickhouse_dao)

        try:
            clickhouse_data_checker.check_data_exists(
                table="instruments_ref", data_length=len_instruments
            )
        except Exception as e:
            logger.error(e)
            raise Exception(e)
        else:
            logger.info(f"Проверка на наличе данных инструментов в ClickHouse успешно завершена")

    instruments = get_instruments_by_security_from_moex()
    len_instruments_clickhouse = insert_instruments_clickhouse(instruments)
    len_instruments_postgres = insert_instruments_postgres(instruments)
    check_data_instruments_clickhouse(len_instruments_clickhouse)


logger = logging.getLogger(__name__)
get_instruments_dag()
