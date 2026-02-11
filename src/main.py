from config.settings import Settings
from src.clients.moex_mapper import MOEXMapper
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.postgres_dao import PostgresDAO
from src.clients.moex_rest_client import MOEXRestClient


def get_instruments(moex_rest_client, postgres_dao, clickhouse_dao, moex_mapper):
    instruments = moex_rest_client.get_tqbr_securities(
        params={
            "securities.columns": "SECID,SECNAME,SHORTNAME,ISIN,SECTYPE,LOTSIZE,CURRENCYID,BOARDID"
        },
        engine="stock",
        market="shares",
        moex_mapper=moex_mapper,
    )
    print(instruments)

    postgres_dao.insert_instruments(instruments)
    print("Вставлены инструменты в postgres")

    clickhouse_dao.insert_instruments(instruments)
    print("Вставлены инструменты в clickhouse")


def get_indices(moex_rest_client, postgres_dao, clickhouse_dao, moex_mapper):
    indices = moex_rest_client.get_indices(
        params={"indices.colums": "indexid,shortname"},
        engine="stock",
        market="index",
        moex_mapper=moex_mapper,
    )
    print(indices)

    postgres_dao.insert_indices(indices)
    print("Вставлены индексы в postgres")

    clickhouse_dao.insert_indices(indices)
    print("Вставлены индексы в clickhouse")


def get_current_prices(moex_rest_client, postgres_dao, moex_mapper):
    current_prices = moex_rest_client.get_current_prices(
        params={"marketdata.columns": "SECID,LAST,VOLTODAY,LASTTOPREVPRICE"},
        engine="stock",
        market="shares",
        moex_mapper=moex_mapper,
    )
    print(current_prices)

    postgres_dao.insert_current_prices(current_prices)
    print("Вставлены текущие цены в postgres")


def get_current_indices(moex_rest_client, postgres_dao, moex_mapper):
    current_indices = moex_rest_client.get_current_indices(
        params={
            "boardid": "SNDX",
            "marketdata.columns": "SECID,BOARDID,CURRENTVALUE,OPENVALUE,LASTVALUE,LASTCHANGEPRC,LASTCHANGE,HIGH,LOW,VALTODAY,CAPITALIZATION,UPDATETIME,TRADEDATE",
        },
        engine="stock",
        market="index",
        moex_mapper=moex_mapper,
    )
    print(current_indices)

    postgres_dao.insert_current_indices(current_indices)
    print("Вставлены текущие индексы в postgres")


if __name__ == "__main__":
    moex_rest_client = MOEXRestClient()
    moex_mapper = MOEXMapper()
    settings = Settings()
    postgres_dao = PostgresDAO(settings)
    clickhouse_dao = ClickHouseDAO(settings)

    get_instruments(moex_rest_client, postgres_dao, clickhouse_dao, moex_mapper)
    get_indices(moex_rest_client, postgres_dao, clickhouse_dao, moex_mapper)
    get_current_prices(moex_rest_client, postgres_dao, moex_mapper)
    get_current_indices(moex_rest_client, postgres_dao, moex_mapper)

    # candles_by_security = moex_rest_client.get_candles_by_security(
    #     secid="SBER",
    #     params={"from": "2026-01-01", "till": "2026-01-31", "interval": 1},
    #     engine="stock",
    #     market="shares",
    # )
    # indices_metadata = moex_rest_client.get_indices_metadata(
    #     params={"boardid": "SNDX"},
    #     engine="stock",
    #     market="index",
    # )
    # corporate_actions_by_security = moex_rest_client.get_dividends_by_security(secid="SBER", params={})
    # daily_aggregates_by_security = moex_rest_client.get_info_by_security(
    #     secid="SBER",
    #     params={"date": "2026-01-14"},
    #     engine="stock",
    #     market="shares",
    # )
    # index_history = moex_rest_client.get_index_history(
    #     params={
    #         "boardid": "SNDX",
    #         "secid": "IMOEX",
    #         "from": "2026-01-01",
    #         "till": "2026-01-31",
    #         "history.columns": "TRADEDATE,SECID,BOARDID,OPEN,HIGH,LOW,CLOSE,VALUE,CAPITALIZATION,CURRENCYID,TRADINGSESSION,RECALC_DATE",
    #     },
    #     engine="stock",
    #     market="index",
    # )
