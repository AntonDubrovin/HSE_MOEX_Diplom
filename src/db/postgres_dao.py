import psycopg2


class PostgresDAO:
    def __init__(self, settings):
        self.connection = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
        )

    def close(self):
        self.connection.close()

    def insert_instruments(self, instruments):
        data_to_insert_instruments = []
        for instrument in instruments:
            data_to_insert_instruments.append(
                (
                    instrument.secid,
                    instrument.sec_name,
                    instrument.sec_type,
                    instrument.short_name,
                    instrument.isin,
                    instrument.lot_size,
                    instrument.currency,
                    instrument.board,
                    instrument.engine,
                    instrument.market,
                )
            )

        query_insert_instrument_ref = (
            "INSERT INTO instruments "
            "( "
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
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
            "ON CONFLICT (secid) DO "
            "UPDATE SET "
            " sec_name = EXCLUDED.sec_name, "
            " sec_type = EXCLUDED.sec_type, "
            " short_name = EXCLUDED.short_name, "
            " isin = EXCLUDED.isin, "
            " lot_size = EXCLUDED.lot_size, "
            " currency = EXCLUDED.currency, "
            " board = EXCLUDED.board, "
            " updated_at = NOW()"
        )

        # TODO try execute
        self.connection.cursor().executemany(
            query_insert_instrument_ref, data_to_insert_instruments
        )
        # todo else commit
        self.connection.commit()
