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
├── scripts
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
