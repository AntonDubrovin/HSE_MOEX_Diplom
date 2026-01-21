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
        for inst in instruments:
            data_to_insert_instruments.append(
                (
                    inst.secid,
                    inst.sec_name,
                    inst.sec_type,
                    inst.short_name,
                    inst.isin,
                    inst.lot_size,
                    inst.currency,
                    inst.board,
                    inst.engine,
                    inst.market,
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
