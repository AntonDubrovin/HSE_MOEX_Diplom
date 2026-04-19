import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

    CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST")
    CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT"))
    CLICKHOUSE_DB = os.getenv("CLICKHOUSE_DB")
    CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER")
    CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")

    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    AIRFLOW_BASE_URL = os.getenv("AIRFLOW_BASE_URL")
    AIRFLOW_USERNAME = os.getenv("AIRFLOW_USERNAME")
    AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD")
