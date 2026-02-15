from config.settings import Settings
from src.clients.moex_mapper import MOEXMapper
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.postgres_dao import PostgresDAO
from src.clients.moex_rest_client import MOEXRestClient


def get_instruments(
    moex_rest_client, postgres_dao, clickhouse_dao, engine, market, board, moex_mapper
):
    instruments = moex_rest_client.get_instruments(
        params={
            "securities.columns": "SECID,SECNAME,SHORTNAME,ISIN,SECTYPE,LOTSIZE,CURRENCYID,BOARDID"
        },
        engine=engine,
        market=market,
        board=board,
        moex_mapper=moex_mapper,
    )
    print(instruments)

    postgres_dao.insert_instruments(instruments)
    print("Вставлены инструменты в postgres")

    clickhouse_dao.insert_instruments(instruments)
    print("Вставлены инструменты в clickhouse")


def get_indices(moex_rest_client, postgres_dao, clickhouse_dao, engine, market, board, moex_mapper):
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


def get_current_prices(moex_rest_client, postgres_dao, engine, market, board, moex_mapper):
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


def get_current_indices(moex_rest_client, postgres_dao, engine, market, board, moex_mapper):
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
    moex_rest_client, clickhouse_dao, from_, till_, interval_, secid, engine, market, moex_mapper
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


def get_dividends(moex_rest_client, postgres_dao, clickhouse_dao, secid, moex_mapper):
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


def get_daily_aggregates(
    moex_rest_client, clickhouse_dao, from_, till_, secid, engine, market, board, moex_mapper
):
    daily_aggregates = moex_rest_client.get_daily_aggregates(
        params={"from": from_, "till": till_},
        secid=secid,
        board=board,
        engine=engine,
        market=market,
        moex_mapper=moex_mapper,
    )
    print(daily_aggregates)

    clickhouse_dao.insert_daily_aggregates(daily_aggregates)
    print("Вставлены дневные агрегаты в clickhouse")


def get_index_history(
    moex_rest_client, clickhouse_dao, from_, till_, secid, engine, market, board, moex_mapper
):
    index_history = moex_rest_client.get_index_history(
        params={"from": from_, "till": till_},
        secid=secid,
        board=board,
        engine=engine,
        market=market,
        moex_mapper=moex_mapper,
    )
    print(index_history)

    clickhouse_dao.insert_index_history(index_history)
    print("Вставлена история индексов в clickhouse")


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
        engine="stock",
        market="shares",
        board="TQBR",
        moex_mapper=moex_mapper,
    )

    get_indices(
        moex_rest_client=moex_rest_client,
        postgres_dao=postgres_dao,
        clickhouse_dao=clickhouse_dao,
        engine="stock",
        market="index",
        board="SNDX",
        moex_mapper=moex_mapper,
    )

    get_current_prices(
        moex_rest_client=moex_rest_client,
        postgres_dao=postgres_dao,
        engine="stock",
        market="shares",
        board="TQBR",
        moex_mapper=moex_mapper,
    )

    get_current_indices(
        moex_rest_client=moex_rest_client,
        postgres_dao=postgres_dao,
        engine="stock",
        market="index",
        board="SNDX",
        moex_mapper=moex_mapper,
    )

    get_candles(
        moex_rest_client=moex_rest_client,
        clickhouse_dao=clickhouse_dao,
        from_="2026-02-01",
        till_="2026-02-15",
        interval_=24,
        secid="SBER",
        engine="stock",
        market="shares",
        moex_mapper=moex_mapper,
    )

    get_dividends(
        moex_rest_client=moex_rest_client,
        postgres_dao=postgres_dao,
        clickhouse_dao=clickhouse_dao,
        secid="SBER",
        moex_mapper=moex_mapper,
    )

    get_daily_aggregates(
        moex_rest_client=moex_rest_client,
        clickhouse_dao=clickhouse_dao,
        from_="2026-02-01",
        till_="2026-02-15",
        secid="SBER",
        engine="stock",
        market="shares",
        board="TQBR",
        moex_mapper=moex_mapper,
    )

    get_index_history(
        moex_rest_client=moex_rest_client,
        clickhouse_dao=clickhouse_dao,
        from_="2026-02-01",
        till_="2026-02-15",
        secid="IMOEX",
        engine="stock",
        market="index",
        board="SNDX",
        moex_mapper=moex_mapper,
    )
