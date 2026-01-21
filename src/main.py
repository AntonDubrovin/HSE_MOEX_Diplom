from config.settings import Settings
from src.clients.moex_mapper import MOEXMapper
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.postgres_dao import PostgresDAO
from src.clients.moex_rest_client import MOEXRestClient


def get_instruments(moex_rest_client, postgres_dao, clickhouse_dao):
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


if __name__ == "__main__":
    moex_rest_client = MOEXRestClient()
    moex_mapper = MOEXMapper()
    settings = Settings()
    postgres_dao = PostgresDAO(settings)
    clickhouse_dao = ClickHouseDAO(settings)

    get_instruments(moex_rest_client, postgres_dao, clickhouse_dao)

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
    # current_indices = moex_rest_client.get_current_indices(
    #     params={
    #         "boardid": "SNDX",
    #         "marketdata.columns": "SECID,BOARDID,CURRENTVALUE,LASTCHANGEPRC,OPENVALUE,LASTVALUE,HIGH,LOW,VALTODAY,CAPITALIZATION,UPDATETIME,TRADEDATE",
    #     },
    #     engine="stock",
    #     market="index",
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
