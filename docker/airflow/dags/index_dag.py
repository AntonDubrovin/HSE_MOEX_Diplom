import datetime

from airflow.decorators import dag, task

from config.settings import Settings
from src.clients.moex_api_client import MOEXApiClient
from src.clients.moex_api_mapper import MOEXAPIMapper
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.postgres_dao import PostgresDAO


@dag(
    start_date=datetime.datetime(2026, 2, 23),
    schedule="@daily",
    params={
        "engine": "stock",
        "market": "index",
        "board": "SNDX",
    },
)
def get_index_dag():
    @task()
    def get_index_task(**kwargs):
        settings = Settings()
        postgres_dao = PostgresDAO(settings)
        clickhouse_dao = ClickHouseDAO(settings)
        moex_rest_client = MOEXApiClient()
        moex_mapper = MOEXAPIMapper()

        params = kwargs["params"]
        engine = params["engine"]
        market = params["market"]
        board = params["board"]

        indices = moex_rest_client.get_indices(
            params={"securities.columns": "SECID,SHORTNAME"},
            board=board,
            engine=engine,
            market=market,
            moex_mapper=moex_mapper,
        )
        print(indices)

        postgres_dao.insert_indices(indices)
        print("Вставлены индексы в postgres")

        clickhouse_dao.insert_indices(indices)
        print("Вставлены индексы в clickhouse")

    get_index_task()


get_index_dag()
