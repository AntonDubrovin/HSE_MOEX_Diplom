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
        data_insert_instruments = []
        for instrument in instruments:
            data_insert_instruments.append(
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

        query_insert_instruments = (
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
        self.connection.cursor().executemany(query_insert_instruments, data_insert_instruments)
        # todo else commit
        self.connection.commit()

    def insert_indices(self, indices):
        data_insert_indices = []
        for index in indices:
            data_insert_indices.append(
                (
                    index.index_code,
                    index.index_name,
                    index.engine,
                    index.market,
                )
            )

        query_insert_indices = (
            "INSERT INTO indices "
            "( "
            " index_code, "
            " index_name, "
            " engine, "
            " market "
            ") "
            "VALUES (%s, %s, %s, %s) "
            "ON CONFLICT (index_code) DO "
            "UPDATE SET "
            " index_name = EXCLUDED.index_name, "
            " engine = EXCLUDED.engine, "
            " market = EXCLUDED.market, "
            " updated_at = NOW()"
        )

        # TODO try execute
        self.connection.cursor().executemany(query_insert_indices, data_insert_indices)
        # todo else commit
        self.connection.commit()

    def insert_current_prices(self, current_prices):
        data_insert_current_prices = []
        for price in current_prices:
            data_insert_current_prices.append(
                (
                    price.secid,
                    price.price,
                    price.volume,
                    price.change,
                    price.trading_status,
                )
            )

        query_insert_insert_current_prices = (
            "INSERT INTO current_prices "
            "( "
            " secid, "
            " price, "
            " volume, "
            " change, "
            " trading_status "
            ") "
            "VALUES (%s, %s, %s, %s, %s) "
            "ON CONFLICT (secid) DO "
            "UPDATE SET "
            " price = EXCLUDED.price, "
            " volume = EXCLUDED.volume, "
            " change = EXCLUDED.change, "
            " trading_status = COALESCE(EXCLUDED.trading_status, current_prices.trading_status), "
            " updated_at = NOW()"
        )

        # TODO try execute
        self.connection.cursor().executemany(query_insert_insert_current_prices, data_insert_current_prices)
        # todo else commit
        self.connection.commit()

    def insert_current_indices(self, current_indices):
        data_insert_current_indices = []
        for index in current_indices:
            data_insert_current_indices.append(
                (
                    index.index_code,
                    index.board,
                    index.current_value,
                    index.open_value,
                    index.last_value,
                    index.change_percent,
                    index.change_points,
                    index.high,
                    index.low,
                    index.volume,
                    index.capitalization,
                    index.update_time,
                    index.trade_date,
                )
            )

        query_insert_current_indices = (
            "INSERT INTO current_indices "
            "( "
            " index_code, "
            " board, "
            " current_value, "
            " open_value, "
            " last_value, "
            " change_percent, "
            " change_points, "
            " high, "
            " low, "
            " volume, "
            " capitalization, "
            " update_time, "
            " trade_date "
            ") "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
            "ON CONFLICT (index_code) DO "
            "UPDATE SET "
            " board = EXCLUDED.board, "
            " current_value = EXCLUDED.current_value, "
            " open_value = EXCLUDED.open_value, "
            " last_value = EXCLUDED.last_value, "
            " change_percent = EXCLUDED.change_percent, "
            " change_points = EXCLUDED.change_points, "
            " high = EXCLUDED.high, "
            " low = EXCLUDED.low, "
            " volume = EXCLUDED.volume, "
            " capitalization = EXCLUDED.capitalization, "
            " update_time = EXCLUDED.update_time, "
            " trade_date = EXCLUDED.trade_date, "
            " updated_at = NOW()"
        )

        # TODO try execute
        self.connection.cursor().executemany(query_insert_current_indices, data_insert_current_indices)
        # todo else commit
        self.connection.commit()

    def insert_corporate_actions(self, dividends):
        data_insert_corporate_actions = []
        for d in dividends:
            data_insert_corporate_actions.append(
                (
                    d.secid,
                    d.isin,
                    d.record_date,
                    d.value,
                    d.currency,
                    d.action_type,
                    d.status,
                    d.source_url,
                )
            )

        query_insert_corporate_actions = (
            "INSERT INTO corporate_actions "
            "("
            " secid, "
            " isin, "
            " record_date, "
            " value, "
            " currency, "
            " action_type, "
            " status, "
            " source_url "
            ") "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
            "ON CONFLICT (secid, record_date) DO "
            "UPDATE SET "
            " isin = EXCLUDED.isin, "
            " value = EXCLUDED.value, "
            " currency = EXCLUDED.currency, "
            " action_type = EXCLUDED.action_type, "
            " status = EXCLUDED.status, "
            " source_url = EXCLUDED.source_url, "
            " updated_at = NOW()"
        )

        # TODO try execute
        self.connection.cursor().executemany(query_insert_corporate_actions, data_insert_corporate_actions)
        # todo else commit
        self.connection.commit()
