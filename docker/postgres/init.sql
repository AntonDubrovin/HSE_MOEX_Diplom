CREATE TABLE instruments ( -- справочник инструментов
    id          SERIAL          PRIMARY KEY,        -- автоинкремент
    secid       VARCHAR(20)     NOT NULL UNIQUE,    -- secid из tqbr/securitites
    sec_name    VARCHAR(200),                       -- secname из tqbr/securitites
    -- TODO добавить sec_name, sec_type
    short_name  VARCHAR(200),                       -- shortname из tqbr/securitites
    isin        VARCHAR(12),                        -- isin из tqbr/securitites
    lot_size    INTEGER,                            -- lotsize из tqbr/securitites
    currency    VARCHAR(3),                         -- currencyid из tqbr/securitites
    board       VARCHAR(20),                        -- boardid из tqbr/securitites
    engine      VARCHAR(20),                        -- engine из url
    market      VARCHAR(20),                        -- market из url
    created_at  TIMESTAMP       DEFAULT NOW(),      -- now
    updated_at  TIMESTAMP       DEFAULT NOW()       -- now
);
CREATE INDEX idx_instruments_secid ON instruments(secid);

CREATE TABLE current_prices ( -- текущие цены
    secid       VARCHAR(20) PRIMARY KEY,    -- instrument из ws statistics/subscribe
    price       NUMERIC(18,6),              -- last из ws statistics/subscribe
    volume      INTEGER,                    -- volume из ws statistics/subscribe
    change      NUMERIC(10,4),              -- change из ws statistics/subscribe
    last_update TIMESTAMP DEFAULT NOW()     -- now
);

CREATE TABLE indices ( -- справочник индексов
    index_code VARCHAR(20)      PRIMARY KEY,    -- indexid из analytics
    index_name VARCHAR(100),                    -- shortname из analytics
    created_at TIMESTAMP        DEFAULT NOW(),  -- now
    updated_at TIMESTAMP        DEFAULT NOW()   -- now
);

CREATE TABLE current_indices ( -- текущие значения индексов
    index_code      VARCHAR(20)     PRIMARY KEY,    -- secid из analytics
    board           VARCHAR(10),                    -- boardid из analytics
    current_value   NUMERIC(18,4),                  -- currentvalue из analytics
    open_value      NUMERIC(18,4),                  -- openvalue из analytics
    last_value      NUMERIC(18,4),                  -- lastvalue из analytics
    change_percent  NUMERIC(10,4),                  -- lastchangeprc из analytics
    change_points   NUMERIC(10,4),                  -- lastchange из analytics
    high            NUMERIC(18,4),                  -- high из analytics
    low             NUMERIC(18,4),                  -- low из analytics
    volume          NUMERIC(18,2),                  -- valtoday из analytics
    capitalization  NUMERIC(18,2),                  -- capitalization из analytics
    update_time     TIME,                           -- updatetime из analytics
    trade_date      DATE,                           -- tradedate из analytics
    last_update     TIMESTAMP       DEFAULT NOW()   -- now
);

CREATE TABLE market_status ( -- статус торгов
    market      VARCHAR(50)     PRIMARY KEY,    -- instrument из ws tradingstatus
    status      VARCHAR(20),                    -- status из ws tradingstatus
    open_time   TIME,                           -- open_time из ws tradingstatus
    close_time  TIME,                           -- close_time из ws tradingstatus
    last_update TIMESTAMP       DEFAULT NOW()   -- now
);

CREATE TABLE corporate_actions ( -- корпоративные действия
    id SERIAL   PRIMARY KEY,                    -- автоинкремент
    secid       VARCHAR(20)     NOT NULL,       -- secid из dividends
    isin        VARCHAR(12),                    -- isin из dividends
    record_date DATE,                           -- registryclosedate из dividends
    value       NUMERIC(18,6),                  -- value из dividends
    currency    VARCHAR(3),                     -- currencyid из dividends
    action_type VARCHAR(20),                    -- тип, пока что всегда dividend
    status      VARCHAR(20),                    -- вычисляемое, upcoming/paid
    source_url  TEXT,                           -- url
    created_at  TIMESTAMP       DEFAULT NOW(),  -- now
    updated_at  TIMESTAMP       DEFAULT NOW(),  -- now
    UNIQUE(secid, record_date)
);