import datetime

from airflow.decorators import dag, task

from config.settings import Settings
from src.clients.moex_api_client import MOEXApiClient
from src.clients.moex_api_mapper import MOEXAPIMapper
from src.db.clickhouse_dao import ClickHouseDAO


@dag(
    start_date=datetime.datetime(2026, 2, 27),
    schedule="@daily",
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
    def get_candles_task(**kwargs):
        settings = Settings()
        clickhouse_dao = ClickHouseDAO(settings)
        moex_rest_client = MOEXApiClient()
        moex_mapper = MOEXAPIMapper()

        params = kwargs["params"]
        engine = params["engine"]
        market = params["market"]
        interval_ = params["interval"]
        secid = params["secid"]
        from_ = params["from"]
        till_ = params["till"]

        candles = moex_rest_client.get_candles_by_security(
            params={"from": from_, "till": till_, "interval": interval_},
            secid=secid,
            engine=engine,
            market=market,
            moex_mapper=moex_mapper,
        )
        # print(candles)
        print(len(candles))

        clickhouse_dao.insert_candles(candles)
        print("Вставлены свечи в clickhouse")

    get_candles_task()


get_candles_dag()
