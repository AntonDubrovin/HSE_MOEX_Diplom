CREATE OR REPLACE VIEW
    moex_olap.v_candles_volatility
AS
SELECT
    secid,
    toDate(begin) as trade_date,
    high,
    low,
    close,
    high - low as range,
    100 * (high - low) / close as volatility
FROM
    moex_olap.candles
WHERE
    interval = 24;