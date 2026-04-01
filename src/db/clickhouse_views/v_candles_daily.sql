CREATE OR REPLACE VIEW
    moex_olap.v_candles_daily
AS
SELECT
    secid,
    toDate(begin) as trade_date,
    open,
    high,
    low,
    close,
    volume,
    value
FROM
    moex_olap.candles
WHERE
    interval = 24;
