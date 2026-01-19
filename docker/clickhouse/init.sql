CREATE TABLE moex_olap.instruments_ref ( -- справочник инструментов
    secid String,
    sec_name String,
    sec_type String,
    short_name String,
    isin String,
    lot_size UInt32,
    currency String,
    board String,
    engine String,
    market String,
    updated_at DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree(updated_at)
ORDER BY secid;

CREATE TABLE moex_olap.candles ( -- исторические свечи
    secid String,
    open Float64,
    close Float64,
    high Float64,
    low Float64,
    value Float64,
    volume UInt64,
    begin DateTime('Europe/Moscow'),
    end DateTime('Europe/Moscow'),
    interval UInt16,
    source String DEFAULT 'MOEX'
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(begin)
ORDER BY (secid, begin, interval)
TTL begin + INTERVAL 3 YEAR;

CREATE TABLE moex_olap.daily_aggregates ( -- дневные агрегаты
    secid String,
    trade_date Date,
    open Float64,
    high Float64,
    low Float64,
    close Float64,
    volume UInt64,
    value Float64,
    num_trades UInt32,
    waprice Float64,
    currency String,
    updated_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (trade_date, secid)
PARTITION BY toYYYYMM(trade_date);

CREATE TABLE moex_olap.indices_ref ( -- справочник индексов
    index_code String,
    index_name String,
    updated_at DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY index_code;

CREATE TABLE moex_olap.index_history ( -- исторические данные индексов
    index_code String,
    board String,
    trade_date Date,
    open Float64,
    high Float64,
    low Float64,
    close Float64,
    value Float64,
    volume Float64,
    capitalization  Float64,
    currency String,
    yield Float64,
    duration Float64,
    trading_session String,
    recalc_date Date,
    updated_at DateTime DEFAULT now()
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(trade_date)
ORDER BY (index_code, trade_date, trading_session)
TTL trade_date + INTERVAL 3 YEAR;

CREATE TABLE moex_olap.corporate_actions ( -- история дивидендов/действий
    secid String,
    isin String,
    record_date Date,
    value Float64,
    currency String,
    action_type String,
    status String,
    source_url String,
    updated_at DateTime    DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (secid, record_date);

CREATE TABLE IF NOT EXISTS moex_olap.sec_types ( -- справочник типов ценных бумаг
    sec_type String,
    name String
) ENGINE = MergeTree()
ORDER BY sec_type;

INSERT INTO
    sec_types
        (
            sec_type,
            name
        )
VALUES
    ('1', 'Акция обыкновенная'),
    ('2', 'Акция привилегированная'),
    ('3', 'Государственная облигация'),
    ('4', 'Региональная облигация'),
    ('5', 'Облигация ЦБ'),
    ('6', 'Корпоративная облигация'),
    ('7', 'Облигация МФО'),
    ('8', 'Биржевая облигация'),
    ('9', 'Пай открытого ПИФ'),
    ('A', 'Пай интервального ПИФ'),
    ('B', 'Пай закрытого ПИФ'),
    ('C', 'Муниципальная облигация'),
    ('D', 'Депозитарная расписка'),
    ('E', 'ETF'),
    ('F', 'Ипотечный сертификат'),
    ('G', 'Корзина бумаг'),
    ('I', 'ETC'),
    ('J', 'Пай биржевого ПИФа');