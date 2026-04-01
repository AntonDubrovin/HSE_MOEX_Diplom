CREATE OR REPLACE VIEW
    moex_olap.v_daily_agg_top_tickers
AS
SELECT
    secid,
    toStartOfMonth(trade_date) as month,
    sum(volume) as total_volume,
    sum(value) as total_value,
    sum(num_trades) as total_num_trades
FROM
    moex_olap.daily_aggregates
GROUP BY
    secid, month;