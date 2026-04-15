from config.settings import Settings
from src.db.clickhouse_dao import ClickHouseDAO
from src.db.postgres_dao import PostgresDAO


class Services:
    def __init__(self):
        self.settings = Settings()
        self.postgres_dao = PostgresDAO(self.settings)
        self.clickhouse_dao = ClickHouseDAO(self.settings)

    def get_instrument_secid_by_name(self, name):
        query_select_instrument_secid_by_name = f"""
            SELECT
                secid, sec_name, short_name
            FROM
                instruments
            WHERE
                sec_name ilike '%{name}%' OR
                short_name ilike '%{name}%'
            LIMIT 10
        """
        res = self.postgres_dao.execute(query_select_instrument_secid_by_name)
        return res

    def get_index_secid_by_name(self, name):
        query_select_index_secid_by_name = f"""
            SELECT
                secid, index_name
            FROM
                indices
            WHERE
                index_name ilike '%{name}%'
            LIMIT 10
        """
        res = self.postgres_dao.execute(query_select_index_secid_by_name)
        return res

    def get_instrument_current_price(self, secid):
        query_instrument_current_price = f"""
            SELECT
                secid, price, volume, change, trading_status
            FROM
                current_prices
            WHERE
                secid = '{secid.upper()}'
        """
        res = self.postgres_dao.execute(query_instrument_current_price)
        return res

    def get_index_current_price(self, secid):
        query_index_current_price = f"""
            SELECT
                secid, board, current_value, open_value, last_value, change_percent, change_points, high, low, volume, capitalization
            FROM
                current_indices
            WHERE
                secid = '{secid.upper()}'
        """
        res = self.postgres_dao.execute(query_index_current_price)
        return res
