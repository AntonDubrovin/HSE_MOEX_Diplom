import asyncio

from config.settings import Settings
from src.clients.moex_ws_client import get_securities, moex_websocket
from src.clients.moex_ws_mapper import MOEXWebSocketMapper
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.postgres_dao import PostgresDAO

if __name__ == "__main__":
    settings = Settings()
    postgres_dao = PostgresDAO(settings)
    clickhouse_dao = ClickHouseDAO(settings)

    moex_ws_mapper = MOEXWebSocketMapper()

    WS_URL = "ws://iss.moex.com/infocx/v3/websocket"
    WS_CREDENTIALS = {
        "domain": "DEMO",
        "login": "guest",
        "passcode": "guest",
    }
    destination = "MXSE.securities"
    selector = 'TICKER="MXSE.TQBR.SBER"'

    asyncio.run(
        moex_websocket(
            url=WS_URL,
            credentials=WS_CREDENTIALS,
            destination=destination,
            selector=selector,
            handler=get_securities,
            moex_ws_mapper=moex_ws_mapper,
            postgres_dao=postgres_dao,
        )
    )
