import datetime
import logging

from airflow.decorators import dag, task

from config.settings import Settings
from src.clients.moex_api_client import MOEXApiClient
from src.clients.moex_api_mapper import MOEXAPIMapper
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.clickhouse_data_checker import ClickHouseDataChecker
from src.models.moex_models.index_history import IndexHistory


@dag(
    start_date=datetime.datetime(2026, 2, 23),
    schedule="@daily",
    catchup=False,
    params={
        "engine": "stock",
        "market": "index",
        "board": "SNDX",
        "secid": "IMOEX",
        "from": "2026-01-01",
        "till": "2026-01-01",
    },
)
def get_index_history_dag():
    @task()
    def get_index_history_by_security_from_moex(**kwargs):
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
            index_histories = moex_rest_client.get_index_history(
                params={"from": from_, "till": till_},
                secid=secid,
                board=board,
                engine=engine,
                market=market,
                moex_mapper=moex_mapper,
            )
            # print(index_history)
            logger.info(len(index_histories))
        except Exception as e:
            logger.error(f"Ошибка при загрузке index_history по secid={secid} | {e}", exc_info=True)
            raise Exception(f"Ошибка при загрузке index_history по secid={secid} | {e}")
        else:
            return [
                index_history.model_dump() for index_history in index_histories
            ]  # таски в даге не могут передавать pydantic модель между друг другом

    @task()
    def insert_index_history_clickhouse(index_history_dump, **kwargs):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)

        params = kwargs["params"]
        secid = params["secid"]

        index_history = [IndexHistory(**c) for c in index_history_dump]

        try:
            clickhouse_dao.insert_index_history(index_history)
            logger.info("Вставлена история индексов в clickhouse")
        except Exception as e:
            logger.error(
                f"Ошибка при вставке истории индексов в БД ClickHouse по secid={secid} | {e}",
                exc_info=True,
            )
            raise Exception(
                f"Ошибка при вставке истории индексов в БД ClickHouse по secid={secid}  | {e}"
            )
        else:
            return len(index_history)

    @task()
    def check_data_index_history_clickhouse(len_index_history, **kwargs):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)
        clickhouse_data_checker = ClickHouseDataChecker(clickhouse_dao)

        params = kwargs["params"]
        secid = params["secid"]
        from_ = params["from"]
        till_ = params["till"]

        table = "index_history"
        try:
            clickhouse_data_checker.check_data_exists_by_secid_dates(
                table=table,
                secid=secid,
                from_=from_,
                till_=till_,
                date_column="trade_date",
                data_length=len_index_history,
            )
        except Exception as e:
            logger.error(e)
            raise Exception(e)
        else:
            logger.info(
                f"Проверка на наличе данных истории индексов по secid={secid} успешно завершена"
            )

        try:
            clickhouse_data_checker.check_data_duplicates(
                table=table, groupby_columns=["secid", "trade_date"]
            )
        except Exception as e:
            logger.error(e)
            raise Exception(e)
        else:
            logger.info(f"Проверка на дубли данных истории индексов в clickhouse успешно завершена")

        try:
            clickhouse_data_checker.check_data_not_empty(
                table=table,
                needed_columns=["open", "close", "value"]
            )
        except Exception as e:
            logger.error(e)
            raise Exception(e)
        else:
            logger.info(f"Проверка на пустые данные истории индексов в clickhouse успешно завершена")

    index_history = get_index_history_by_security_from_moex()
    len_index_history = insert_index_history_clickhouse(index_history)
    check_data_index_history_clickhouse(len_index_history)


logger = logging.getLogger(__name__)
get_index_history_dag()
