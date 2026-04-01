CREATE OR REPLACE VIEW
    moex_olap.v_index_history_daily
AS
SELECT
    secid,
    trade_date,
    open,
    high,
    low,
    close,
    capitalization
FROM
    moex_olap.index_history;