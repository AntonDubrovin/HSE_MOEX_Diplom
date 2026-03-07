class PostgresDataChecker:
    def __init__(self, postgres_dao):
        self.postgres_dao = postgres_dao

    def check_data_exists_by_secid(self, table, secid, data_length):
        query_check_data_exists_by_secid = f"""
            SELECT
                COUNT(*)
            FROM
                {table}
            WHERE
                secid = '{secid}'
        """
        db_length = self.postgres_dao.execute(query_check_data_exists_by_secid)[0][0]

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
                {table}
        """
        db_length = self.postgres_dao.execute(query_check_data_exists)[0][0]

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
                {table}
            GROUP BY
                {", ".join(groupby_columns)}
            HAVING
                COUNT(*) > 1
        """
        res = self.postgres_dao.execute(query_check_data_duplicates)

        if res:
            raise Exception(f"Найдены дубли в таблице {table} | {res}")
