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
        "market": "shares",
        "board": "TQBR",
    },
)
def get_instruments_dag():
    @task()
    def get_instruments_task(**kwargs):
        settings = Settings()
        postgres_dao = PostgresDAO(settings)
        clickhouse_dao = ClickHouseDAO(settings)
        moex_rest_client = MOEXApiClient()
        moex_mapper = MOEXAPIMapper()

        params = kwargs["params"]
        engine = params["engine"]
        market = params["market"]
        board = params["board"]

        instruments = moex_rest_client.get_instruments(
            params={
                "securities.columns": "SECID,SECNAME,SHORTNAME,ISIN,SECTYPE,LOTSIZE,CURRENCYID,BOARDID"
            },
            engine=engine,
            market=market,
            board=board,
            moex_mapper=moex_mapper,
        )
        print(len(instruments))
        print(instruments)

        postgres_dao.insert_instruments(instruments)
        print("Вставлены инструменты в postgres")

        clickhouse_dao.insert_instruments(instruments)
        print("Вставлены инструменты в clickhouse")

    get_instruments_task()


get_instruments_dag()
