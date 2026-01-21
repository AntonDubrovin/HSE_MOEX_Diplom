from clickhouse_driver import Client


class ClickHouseDAO:
    def __init__(self, settings):
        self.client = Client(
            host=settings.CLICKHOUSE_HOST,
            port=settings.CLICKHOUSE_PORT,
            user=settings.CLICKHOUSE_USER,
            password=settings.CLICKHOUSE_PASSWORD,
            database=settings.CLICKHOUSE_DB,
        )

    def close(self):
        self.client.disconnect()

    def insert_instruments(self, instruments):
        data_to_insert_instruments = []
        for instrument in instruments:
            isin = ""
            if instrument.isin:
                isin = instrument.isin

            data_to_insert_instruments.append(
                {
                    "secid": instrument.secid,
                    "sec_name": instrument.sec_name,
                    "sec_type": instrument.sec_type,
                    "short_name": instrument.short_name,
                    "isin": isin,
                    "lot_size": instrument.lot_size,
                    "currency": instrument.currency,
                    "board": instrument.board,
                    "engine": instrument.engine,
                    "market": instrument.market,
                }
            )

        query_insert_instruments = (
            "INSERT INTO moex_olap.instruments_ref "
            "("
            " secid, "
            " sec_name, "
            " sec_type, "
            " short_name, "
            " isin, "
            " lot_size, "
            " currency, "
            " board, "
            " engine, "
            " market "
            ") "
            "VALUES "
        )

        # TODO try execute
        self.client.execute(query_insert_instruments, data_to_insert_instruments)

        # TODO optimize в else
        query_optimize_instruments_ref = "OPTIMIZE TABLE moex_olap.instruments_ref FINAL"
        self.client.execute(query_optimize_instruments_ref)
