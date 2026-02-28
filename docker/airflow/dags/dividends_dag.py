import datetime

from airflow.decorators import dag, task

from config.settings import Settings
from src.clients.moex_api_client import MOEXApiClient
from src.clients.moex_api_mapper import MOEXAPIMapper
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.postgres_dao import PostgresDAO


@dag(
    start_date=datetime.datetime(2026, 2, 27),
    schedule="@daily",
    params={"secid": "SBER"},
)
def get_dividends_dag():
    @task()
    def get_dividends_task(**kwargs):
        settings = Settings()
        postgres_dao = PostgresDAO(settings)
        clickhouse_dao = ClickHouseDAO(settings)
        moex_rest_client = MOEXApiClient()
        moex_mapper = MOEXAPIMapper()

        params = kwargs["params"]
        secid = params["secid"]

        dividends = moex_rest_client.get_dividends_by_security(
            params={},
            secid=secid,
            moex_mapper=moex_mapper,
        )
        print(dividends)

        postgres_dao.insert_corporate_actions(dividends)
        print("Вставлены дивиденды в postgres")

        clickhouse_dao.insert_corporate_actions(dividends)
        print("Вставлены дивиденды в clickhouse")

    get_dividends_task()


get_dividends_dag()
