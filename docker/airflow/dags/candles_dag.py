import datetime
import logging

from airflow.decorators import dag, task

from config.settings import Settings
from src.clients.moex_api_client import MOEXApiClient
from src.clients.moex_api_mapper import MOEXAPIMapper
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.clickhouse_data_checker import ClickHouseDataChecker
from src.models.moex_models.candle import Candle


@dag(
    start_date=datetime.datetime(2026, 2, 27),
    schedule="@daily",
    catchup=False,
    params={
        "engine": "stock",
        "market": "shares",
        "interval": 24,
        "secid": "SBER",
        "from": "2026-01-01",
        "till": "2026-01-01",
    },
)
def get_candles_dag():
    @task()
    def get_candles_by_security_from_moex(**kwargs):
        moex_rest_client = MOEXApiClient()
        moex_mapper = MOEXAPIMapper()

        params = kwargs["params"]
        engine = params["engine"]
        market = params["market"]
        interval_ = params["interval"]
        secid = params["secid"]
        from_ = params["from"]
        till_ = params["till"]

        try:
            candles = moex_rest_client.get_candles_by_security(
                params={"from": from_, "till": till_, "interval": interval_},
                secid=secid,
                engine=engine,
                market=market,
                moex_mapper=moex_mapper,
            )
            # print(candles)
            logger.info(len(candles))
        except Exception as e:
            logger.error(f"Ошибка при загрузке свечей по secid={secid} | {e}", exc_info=True)
            raise Exception(f"Ошибка при загрузке свечей по secid={secid} | {e}")
        else:
            return [
                candle.model_dump() for candle in candles
            ]  # таски в даге не могут передавать pydantic модель между друг другом

    @task()
    def insert_candles_clickhouse(candles_dump, **kwargs):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)

        params = kwargs["params"]
        secid = params["secid"]

        candles = [Candle(**c) for c in candles_dump]

        try:
            clickhouse_dao.insert_candles(candles)
            logger.info("Вставлены свечи в clickhouse")
        except Exception as e:
            logger.error(
                f"Ошибка при вставке свечей в БД ClickHouse по secid={secid} | {e}", exc_info=True
            )
            raise Exception(f"Ошибка при вставке свечей в БД ClickHouse по secid={secid}  | {e}")
        else:
            return len(candles)

    @task()
    def check_data_candles_clickhouse(len_candles, **kwargs):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)
        clickhouse_data_checker = ClickHouseDataChecker(clickhouse_dao)

        params = kwargs["params"]
        secid = params["secid"]
        from_ = params["from"]
        till_ = params["till"]

        try:
            clickhouse_data_checker.check_data_exists_by_secid_dates(
                table="candles",
                secid=secid,
                from_=from_,
                till_=till_,
                date_column="begin",
                data_length=len_candles,
            )
        except Exception as e:
            logger.error(e)
            raise Exception(e)
        else:
            logger.info(f"Проверка на наличе данных свечей по secid={secid} успешно завершена")

    candles = get_candles_by_security_from_moex()
    len_candles = insert_candles_clickhouse(candles)
    check_data_candles_clickhouse(len_candles)


logger = logging.getLogger(__name__)
get_candles_dag()
