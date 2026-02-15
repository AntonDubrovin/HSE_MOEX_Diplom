from config.settings import Settings
from src.clients.moex_mapper import MOEXMapper
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.postgres_dao import PostgresDAO
from src.clients.moex_rest_client import MOEXRestClient


def get_instruments(
    moex_rest_client, postgres_dao, clickhouse_dao, moex_mapper, board, engine, market
):
    instruments = moex_rest_client.get_instruments(
        params={
            "securities.columns": "SECID,SECNAME,SHORTNAME,ISIN,SECTYPE,LOTSIZE,CURRENCYID,BOARDID"
        },
        board=board,
        engine=engine,
        market=market,
        moex_mapper=moex_mapper,
    )
    print(instruments)

    postgres_dao.insert_instruments(instruments)
    print("Вставлены инструменты в postgres")

    clickhouse_dao.insert_instruments(instruments)
    print("Вставлены инструменты в clickhouse")


def get_indices(moex_rest_client, postgres_dao, clickhouse_dao, moex_mapper, board, engine, market):
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


def get_current_prices(moex_rest_client, postgres_dao, moex_mapper, board, engine, market):
    current_prices = moex_rest_client.get_current_prices(
        params={"marketdata.columns": "SECID,LAST,VOLTODAY,LASTTOPREVPRICE"},
        board=board,
        engine=engine,
        market=market,
        moex_mapper=moex_mapper,
    )
    print(current_prices)

    postgres_dao.insert_current_prices(current_prices)
    print("Вставлены текущие цены в postgres")


def get_current_indices(moex_rest_client, postgres_dao, moex_mapper, board, engine, market):
    current_indices = moex_rest_client.get_current_indices(
        params={
            "marketdata.columns": "SECID,BOARDID,CURRENTVALUE,OPENVALUE,LASTVALUE,LASTCHANGEPRC,LASTCHANGE,HIGH,LOW,VALTODAY,CAPITALIZATION,UPDATETIME,TRADEDATE",
        },
        board=board,
        engine=engine,
        market=market,
        moex_mapper=moex_mapper,
    )
    print(current_indices)

    postgres_dao.insert_current_indices(current_indices)
    print("Вставлены текущие индексы в postgres")


def get_candles(
    moex_rest_client, clickhouse_dao, moex_mapper, from_, till_, interval_, secid, engine, market
):
    candles = moex_rest_client.get_candles_by_security(
        params={"from": from_, "till": till_, "interval": interval_},
        secid=secid,
        engine=engine,
        market=market,
        moex_mapper=moex_mapper,
    )
    print(candles)

    clickhouse_dao.insert_candles(candles)
    print("Вставлены свечи в clickhouse")


def get_dividends(moex_rest_client, postgres_dao, clickhouse_dao, moex_mapper, secid):
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


if __name__ == "__main__":
    moex_rest_client = MOEXRestClient()
    moex_mapper = MOEXMapper()
    settings = Settings()
    postgres_dao = PostgresDAO(settings)
    clickhouse_dao = ClickHouseDAO(settings)

    get_instruments(
        moex_rest_client=moex_rest_client,
        postgres_dao=postgres_dao,
        clickhouse_dao=clickhouse_dao,
        moex_mapper=moex_mapper,
        board="TQBR",
        engine="stock",
        market="shares",
    )

    get_indices(
        moex_rest_client=moex_rest_client,
        postgres_dao=postgres_dao,
        clickhouse_dao=clickhouse_dao,
        moex_mapper=moex_mapper,
        board="SNDX",
        engine="stock",
        market="index",
    )

    get_current_prices(
        moex_rest_client=moex_rest_client,
        postgres_dao=postgres_dao,
        moex_mapper=moex_mapper,
        engine="stock",
        market="shares",
        board="TQBR",
    )

    get_current_indices(
        moex_rest_client=moex_rest_client,
        postgres_dao=postgres_dao,
        moex_mapper=moex_mapper,
        board="SNDX",
        engine="stock",
        market="index",
    )

    get_candles(
        moex_rest_client=moex_rest_client,
        clickhouse_dao=clickhouse_dao,
        moex_mapper=moex_mapper,
        from_="2026-02-01",
        till_="2026-02-15",
        interval_=24,
        secid="SBER",
        engine="stock",
        market="shares",
    )

    get_dividends(
        moex_rest_client=moex_rest_client,
        postgres_dao=postgres_dao,
        clickhouse_dao=clickhouse_dao,
        moex_mapper=moex_mapper,
        secid="SBER",
    )
