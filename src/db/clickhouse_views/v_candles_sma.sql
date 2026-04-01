CREATE OR REPLACE VIEW
    moex_olap.v_candles_sma
AS
SELECT
    secid,
    toDate(begin) as trade_date,
    close,
    avg(close) OVER sma20 as sma20,
    avg(close) OVER sma50 as sma50,
    avg(close) OVER sma200 as sma200,
    stddevPop(close) OVER sma20 as stddev20,
    avg(close) OVER sma20 + 2 * stddevPop(close) OVER sma20 as bollinger_upper,
    avg(close) OVER sma20 - 2 * stddevPop(close) OVER sma20 as bollinger_lower
FROM
    moex_olap.candles
WHERE
    interval = 24
WINDOW
    sma20 as (PARTITION BY secid ORDER BY begin ROWS 19 PRECEDING),
    sma50 as (PARTITION BY secid ORDER BY begin ROWS 49 PRECEDING),
    sma200 as (PARTITION BY secid ORDER BY begin ROWS 199 PRECEDING);