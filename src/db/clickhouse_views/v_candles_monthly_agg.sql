CREATE OR REPLACE VIEW
    moex_olap.v_candles_monthly_agg
AS
SELECT
    secid,
    toStartOfMonth(begin) as month,
    sum(volume) as total_volume,
    sum(value) as total_value,
    count(*) as trading_days
FROM
    moex_olap.candles
WHERE
    interval = 24
GROUP BY
    secid, month;
