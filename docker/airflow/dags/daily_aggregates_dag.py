import datetime

from airflow.decorators import dag, task

from config.settings import Settings
from src.clients.moex_api_client import MOEXApiClient
from src.clients.moex_api_mapper import MOEXAPIMapper
from src.db.clickhouse_dao import ClickHouseDAO


@dag(
    start_date=datetime.datetime(2026, 2, 23),
    schedule="@daily",
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
    def get_daily_aggregates_task(**kwargs):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)
        moex_rest_client = MOEXApiClient()
        moex_mapper = MOEXAPIMapper()

        params = kwargs["params"]
        engine = params["engine"]
        market = params["market"]
        board = params["board"]
        secid = params["secid"]
        from_ = params["from"]
        till_ = params["till"]

        daily_aggregates = moex_rest_client.get_daily_aggregates(
            params={"from": from_, "till": till_},
            secid=secid,
            board=board,
            engine=engine,
            market=market,
            moex_mapper=moex_mapper,
        )
        print(len(daily_aggregates))
        print(daily_aggregates)

        clickhouse_dao.insert_daily_aggregates(daily_aggregates)
        print("Вставлены дневные агрегаты в clickhouse")

    get_daily_aggregates_task()


get_daily_aggregates_dag()
