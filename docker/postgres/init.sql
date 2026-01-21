CREATE TABLE sec_types( -- справочник типов ценных бумаг
    sec_type VARCHAR(5) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

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

CREATE TABLE instruments ( -- справочник инструментов
    id SERIAL PRIMARY KEY,
    secid VARCHAR(20) NOT NULL UNIQUE,
    sec_name VARCHAR(200),
    sec_type VARCHAR(5),
    short_name VARCHAR(200),
    isin VARCHAR(12),
    lot_size INTEGER,
    currency VARCHAR(3),
    board VARCHAR(20),
    engine VARCHAR(20),
    market VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_sec_type FOREIGN KEY (sec_type) REFERENCES sec_types(sec_type)
);
CREATE INDEX idx_instruments_secid ON instruments(secid);

CREATE TABLE current_prices ( -- текущие цены
    secid VARCHAR(20) PRIMARY KEY,
    price NUMERIC(18,6),
    volume INTEGER,
    change NUMERIC(10,4),
    last_update TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_current_prices_secid FOREIGN KEY (secid) REFERENCES instruments(secid)
);

CREATE TABLE indices ( -- справочник индексов
    index_code VARCHAR(20) PRIMARY KEY,
    index_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE current_indices ( -- текущие значения индексов
    index_code VARCHAR(20) PRIMARY KEY,
    board VARCHAR(10),
    current_value NUMERIC(18,4),
    open_value NUMERIC(18,4),
    last_value NUMERIC(18,4),
    change_percent NUMERIC(10,4),
    change_points NUMERIC(10,4),
    high NUMERIC(18,4),
    low NUMERIC(18,4),
    volume NUMERIC(18,2),
    capitalization NUMERIC(18,2),
    update_time TIME,
    trade_date DATE,
    last_update TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_current_indices_code FOREIGN KEY (index_code) REFERENCES indices(index_code)
);

CREATE TABLE market_status ( -- статус торгов
    market VARCHAR(50) PRIMARY KEY,
    status VARCHAR(20),
    open_time TIME,
    close_time TIME,
    last_update TIMESTAMP DEFAULT NOW()
);

CREATE TABLE corporate_actions ( -- корпоративные действия
    id SERIAL PRIMARY KEY,
    secid VARCHAR(20) NOT NULL,
    isin VARCHAR(12),
    record_date DATE,
    value NUMERIC(18,6),
    currency VARCHAR(3),
    action_type VARCHAR(20),
    status VARCHAR(20),
    source_url TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(secid, record_date),

    CONSTRAINT fk_corporate_actions_secid FOREIGN KEY (secid) REFERENCES instruments(secid)
);