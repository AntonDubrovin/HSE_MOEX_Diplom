CREATE TABLE moex_olap.instruments_ref ( -- справочник инструментов
    secid       String,                 -- secid из tqbr/securities
    short_name  String,                 -- shortname из tqbr/securities
    isin        String,                 -- isin из из tqbr/securities
    lot_size    UInt32,                 -- lotsize из tqbr/securities
    currency    String,                 -- currencyid из tqbr/securities
    board       String,                 -- boardid из tqbr/securities
    engine      String,                 -- engine из url
    market      String,                 -- market из url
    updated_at  DateTime DEFAULT now()  -- now
) ENGINE = ReplacingMergeTree(updated_at)
ORDER BY secid;

CREATE TABLE moex_olap.candles ( -- исторические свечи
    secid       String,                                     -- secid из url
    open        Float64,                                    -- open из candles
    close       Float64,                                    -- close из candles
    high        Float64,                                    -- high из candles
    low         Float64,                                    -- low из candles
    value       Float64,                                    -- value из candles
    volume      UInt64,                                     -- volume из candles
    begin       DateTime('Europe/Moscow'),                  -- begin из candles
    end         DateTime('Europe/Moscow'),                  -- end из candles
    interval    UInt16,                                     -- interval из параметра
    source      String                      DEFAULT 'MOEX'  -- источник пока что константа moex
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(begin)
ORDER BY (secid, begin, interval)
TTL begin + INTERVAL 3 YEAR;

CREATE TABLE moex_olap.daily_aggregates ( -- дневные агрегаты
    secid       String,                     -- secid из securities/{secid}.json
    trade_date  Date,                       -- tradedate из securities/{secid}.json
    open        Float64,                    -- open из securities/{secid}.json
    high        Float64,                    -- high из securities/{secid}.json
    low         Float64,                    -- low из securities/{secid}.json
    close       Float64,                    -- close из securities/{secid}.json
    volume      UInt64,                     -- volume из securities/{secid}.json
    value       Float64,                    -- value из securities/{secid}.json
    num_trades  UInt32,                     -- numtrades из securities/{secid}.json
    waprice     Float64,                    -- waprice из securities/{secid}.json
    currency    String,                     -- currencyid из securities/{secid}.json
    updated_at  DateTime    DEFAULT now()   -- now
) ENGINE = MergeTree()
ORDER BY (trade_date, secid)
PARTITION BY toYYYYMM(trade_date);

CREATE TABLE moex_olap.indices_ref ( -- справочник индексов
    index_code String,                  -- indexid из analytics
    index_name String,                  -- shortname из analytics
    updated_at DateTime DEFAULT now()   -- now
) ENGINE = MergeTree()
ORDER BY index_code;

CREATE TABLE moex_olap.index_history ( -- исторические данные индексов
    index_code      String,                     -- secid из analytics
    board           String,                     -- boardid из analytics
    trade_date      Date,                       -- tradedate из analytics
    open            Float64,                    -- open из analytics
    high            Float64,                    -- high из analytics
    low             Float64,                    -- low из analytics
    close           Float64,                    -- close из analytics
    value           Float64,                    -- value из analytics
    volume          Float64,                    -- volume из analytics
    capitalization  Float64,                    -- capitalization из analytics
    currency        String,                     -- currencyid из analytics
    yield           Float64,                    -- yield из analytics
    duration        Float64,                    -- duration из analytics
    trading_session String,                     -- tradingsession  из analytics
    recalc_date     Date,                       -- recalc_date из analytics
    updated_at      DateTime    DEFAULT now()   -- now
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(trade_date)
ORDER BY (index_code, trade_date, trading_session)
TTL trade_date + INTERVAL 3 YEAR;

CREATE TABLE moex_olap.corporate_actions ( -- история дивидендов/действий
    secid       String,                     -- secid из dividends
    isin        String,                     -- isin из dividends
    record_date Date,                       -- registryclosedate из dividends
    value       Float64,                    -- value из dividends
    currency    String,                     -- currencyid из dividends
    action_type String,                     -- тип, пока константа dividend
    status      String,                     -- вычисляемое, upcoming/paid
    source_url  String,                     -- url
    updated_at  DateTime    DEFAULT now()   -- now
) ENGINE = MergeTree()
ORDER BY (secid, record_date);