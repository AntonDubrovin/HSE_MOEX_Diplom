В репозитории представлена разработанная в рамках магистерской ВКР ВШЭ комплескная система для полного цикла работы с биржевыми данными Московской биржи.

Система обеспечивает:
- автоматический сбор данных - как исторических, так и в реальном времени.
- Хранение данных - в оперативном и аналитическом хранилищах.
- Трансформацию данных и построение аналитических витрин.
- И предоставление данных конечному пользователю.
    - Телеграм-бот
    - Дашборды

В качестве источника выбрана Московская биржа. Выбор обоснован тем, что большую часть данных можно получить бесплатно и без брокерского договора, биржа обслуживает более 40 миллионов инвесторов, а по её данным можно получить информацию по индексам, акциям, облигациям, дивидендам и многому другому.

Архитектуру системы можно посмотреть [здесь](docs/ВКР%20схема/MOEX_diplom_schema.drawio.png)

Схему БД PostgreSQL можно посмотреть [здесь](docs/db/OLTP.drawio.png)

Схему БД ClickHouse можно посмотреть [здесь](docs/db/OLAP.drawio.png)

Сравнительную таблицу с аналогами анализа биржевых данных можно посмотреть [здесь](docs/сравнительная таблица.png)


Ниже приведена структура проекта.
- config/settings.py - здесь содержатся настройки для postgres, clickhouse, airflow
- docker:
    - здесь описаны все yml файлы для контейнеров,
    - написан код всех DAG в docker/airflow/dags
    - описаны init.sql файлы postgre и clickhouse для инициализации БД с созданием таблиц
- src - здесь приведен основной код системы:
    - clients - работа с MOEX API:
        - обращение к API по REST, соответствующие мапперы в Pydantic модели
        - обращение к MOEX через WebSocket, соответствующие мапперы в Pydantic модели
    - db - работа с БД:
        - аналитические витрины данных в виде VIEW ClickHouse
        - DAO классы PH и CH
        - Классы для контроля данных
    - models - здесь описаны все сущности MOEX, с которыми ведется работа, в виде Pydantic моделей
    - tg_bot - работа с Телеграм-ботом
    - websocket - работа с WebSocket сервисом
    

```
├── config
│   └── settings.py
├── docker
│   ├── airflow
│   │   ├── config
│   │   ├── dags
│   │   │   ├── candles_dag.py
│   │   │   ├── daily_aggregates_dag.py
│   │   │   ├── dividends_dag.py
│   │   │   ├── index_dag.py
│   │   │   ├── index_history_dag.py
│   │   │   └── instruments_dag.py
│   │   ├── docker-compose.yml
│   │   └── plugins
│   ├── db
│   │   ├── clickhouse
│   │   │   └── init.sql
│   │   ├── docker-compose.yml
│   │   └── postgres
│   │       └── init.sql
│   ├── tg_bot
│   │   └── docker-compose.yml
│   └── websocket
│       └── docker-compose.yml
├── requirements.txt
└── src
    ├── clients
    │   ├── moex_api_client.py
    │   ├── moex_api_mapper.py
    │   ├── moex_urls.py
    │   ├── moex_ws_client.py
    │   └── moex_ws_mapper.py
    ├── db
    │   ├── clickhouse_dao.py
    │   ├── clickhouse_data_checker.py
    │   ├── clickhouse_views
    │   │   ├── v_candles_daily.sql
    │   │   ├── v_candles_monthly_agg.sql
    │   │   ├── v_candles_sma.sql
    │   │   ├── v_candles_volatility.sql
    │   │   ├── v_daily_agg_top_tickers.sql
    │   │   ├── v_dividends_yearly.sql
    │   │   ├── v_index_history_capitalization.sql
    │   │   └── v_index_history_daily.sql
    │   ├── posgtres_data_checker.py
    │   └── postgres_dao.py
    ├── main.py
    ├── models
    │   └── moex_models
    │       ├── candle.py
    │       ├── current_index.py
    │       ├── current_price.py
    │       ├── daily_aggregates.py
    │       ├── dividend.py
    │       ├── index.py
    │       ├── index_history.py
    │       └── instrument.py
    ├── tg_bot
    │   ├── handlers.py
    │   ├── services.py
    │   └── telegram_bot.py
    └── websocket
        └── websocket_main.py
```
