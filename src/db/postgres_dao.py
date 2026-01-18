import psycopg2
from config.settings import settings
from src.models.moex_models.instrument import Instrument


class PostgresDAO:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
        )

    def close(self):
        self.connection.cursor().close()
        self.connection.close()

    def insert_instrument(self, instrument: Instrument):
        query_insert_instrument = """
            INSERT INTO
                instruments
                    (
                        secid,
                        sec_name,
                        short_name,
                        isin,
                        lot_size,
                        currency,
                        board,
                        engine,
                        market
                    )
            VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT
                (secid)
            DO
            UPDATE
            SET
                sec_name = EXCLUDED.sec_name,
                short_name = EXCLUDED.short_name,
                isin = EXCLUDED.isin,
                lot_size = EXCLUDED.lot_size,
                currency = EXCLUDED.currency,
                board = EXCLUDED.board
        """
        self.connection.cursor().execute(
            query_insert_instrument,
            [
                instrument.secid,
                instrument.sec_name,
                instrument.short_name,
                instrument.isin,
                instrument.lot_size,
                instrument.currency,
                instrument.board,
                instrument.engine,
                instrument.market,
            ],
        )
        self.connection.commit()
