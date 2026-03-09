class ClickHouseDataChecker:
    def __init__(self, clickhouse_dao):
        self.clickhouse_dao = clickhouse_dao

    def check_data_exists_by_secid_dates(
        self, table, secid, from_, till_, date_column, data_length
    ):
        query_check_data_exists_by_secid_dates = f"""
            SELECT
                COUNT(*)
            FROM
                moex_olap.{table} FINAL
            WHERE
                secid = '{secid}' AND
                {date_column} BETWEEN '{from_}' AND '{till_}';
        """
        db_length = self.clickhouse_dao.client.execute(query_check_data_exists_by_secid_dates)[0][0]

        if db_length != data_length:
            raise Exception(
                f"Несовпадение количества данных. "
                f"Из API получено {data_length} записей, в БД {db_length} записей"
            )

    def check_data_exists_by_secid(self, table, secid, data_length):
        query_check_data_exists_by_secid = f"""
            SELECT
                COUNT(*)
            FROM
                moex_olap.{table} FINAL
            WHERE
                secid = '{secid}'
        """
        db_length = self.clickhouse_dao.client.execute(query_check_data_exists_by_secid)[0][0]

        if db_length != data_length:
            raise Exception(
                f"Несовпадение количества данных. "
                f"Из API получено {data_length} записей, в БД {db_length} записей"
            )

    def check_data_exists(self, table, data_length):
        query_check_data_exists = f"""
            SELECT
                COUNT(*)
            FROM
                moex_olap.{table} FINAL
            WHERE
                updated_at > now() - INTERVAL 1 DAY
        """
        db_length = self.clickhouse_dao.client.execute(query_check_data_exists)[0][0]

        if db_length != data_length:
            raise Exception(
                f"Несовпадение количества данных. "
                f"Из API получено {data_length} записей, в БД {db_length} записей"
            )

    def check_data_duplicates(self, table, groupby_columns):
        query_check_data_duplicates = f"""
            SELECT
                {", ".join(groupby_columns)}, COUNT(*)
            FROM
                moex_olap.{table} FINAL
            GROUP BY
                {", ".join(groupby_columns)}
            HAVING
                COUNT(*) > 1
        """
        res = self.clickhouse_dao.client.execute(query_check_data_duplicates)

        if res:
            raise Exception(f"Найдены дубли в таблице {table} | {res}")

    def check_data_not_empty(self, table, needed_columns):
        not_empty_data_condition = " OR ".join([f"{needed_column} IS NULL" for needed_column in needed_columns])
        query_check_data_not_empty = f"""
            SELECT
                COUNT(*)
            FROM
                moex_olap.{table} FINAL
            WHERE 
                {not_empty_data_condition}
        """
        db_empty_count = self.clickhouse_dao.client.execute(query_check_data_not_empty)[0][0]

        if db_empty_count > 0:
            raise Exception(f"Найдено {db_empty_count} записей с пустыми обязательными полями в таблице {table}")

