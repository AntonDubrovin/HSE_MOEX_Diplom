import datetime
import logging

from airflow.decorators import dag, task

from config.settings import Settings
from src.clients.moex_api_client import MOEXApiClient
from src.clients.moex_api_mapper import MOEXAPIMapper
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.clickhouse_data_checker import ClickHouseDataChecker
from src.models.moex_models.daily_aggregates import DailyAggregates


@dag(
    start_date=datetime.datetime(2026, 2, 23),
    schedule="@daily",
    catchup=False,
    params={
        "engine": "stock",
        "market": "shares",
        "board": "TQBR",
        "secid": "SBER",
        "from": "2026-01-01",
        "till": "2026-01-01",
    },
)
def get_daily_aggregates_dag():
    @task()
    def get_daily_aggregates_from_moex(**kwargs):
        moex_rest_client = MOEXApiClient()
        moex_mapper = MOEXAPIMapper()

        params = kwargs["params"]
        engine = params["engine"]
        market = params["market"]
        board = params["board"]
        secid = params["secid"]
        from_ = params["from"]
        till_ = params["till"]

        try:
            daily_aggregates = moex_rest_client.get_daily_aggregates(
                params={"from": from_, "till": till_},
                secid=secid,
                board=board,
                engine=engine,
                market=market,
                moex_mapper=moex_mapper,
            )
            logger.info(daily_aggregates)
            logger.info(len(daily_aggregates))
        except Exception as e:
            logger.error(
                f"Ошибка при загрузке дневных агрегатов по secid={secid} | {e}", exc_info=True
            )
            raise Exception(f"Ошибка при загрузке дневных агрегатов по secid={secid} | {e}")
        else:
            return [
                daily_aggregate.model_dump() for daily_aggregate in daily_aggregates
            ]  # таски в даге не могут передавать pydantic модель между друг другом

    @task()
    def insert_daily_aggregates_clickhouse(daily_aggregates_dump, **kwargs):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)

        params = kwargs["params"]
        secid = params["secid"]

        daily_aggregates = [DailyAggregates(**c) for c in daily_aggregates_dump]

        try:
            clickhouse_dao.insert_daily_aggregates(daily_aggregates)
            logger.info("Вставлены свечи в clickhouse")
        except Exception as e:
            logger.error(
                f"Ошибка при вставке дневных агрегатов в БД ClickHouse по secid={secid} | {e}",
                exc_info=True,
            )
            raise Exception(
                f"Ошибка при вставке дневных агрегатов в БД ClickHouse по secid={secid}  | {e}"
            )
        else:
            return len(daily_aggregates)

    @task()
    def check_data_daily_aggregates_clickhouse(len_daily_aggregates, **kwargs):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)
        clickhouse_data_checker = ClickHouseDataChecker(clickhouse_dao)

        params = kwargs["params"]
        secid = params["secid"]
        from_ = params["from"]
        till_ = params["till"]

        table = "daily_aggregates"
        try:
            clickhouse_data_checker.check_data_exists_by_secid_dates(
                table=table,
                secid=secid,
                from_=from_,
                till_=till_,
                date_column="trade_date",
                data_length=len_daily_aggregates,
            )
        except Exception as e:
            logger.error(e)
            raise Exception(e)
        else:
            logger.info(
                f"Проверка на наличе данных дневных агрегатов в clickhouse по secid={secid} успешно завершена"
            )

        try:
            clickhouse_data_checker.check_data_duplicates(
                table=table, groupby_columns=["secid", "trade_date"]
            )
        except Exception as e:
            logger.error(e)
            raise Exception(e)
        else:
            logger.info(
                f"Проверка на дубли данных дневных агрегатов в clickhouse успешно завершена"
            )

    daily_aggregates = get_daily_aggregates_from_moex()
    len_daily_aggregates = insert_daily_aggregates_clickhouse(daily_aggregates)
    check_data_daily_aggregates_clickhouse(len_daily_aggregates)


logger = logging.getLogger(__name__)
get_daily_aggregates_dag()
