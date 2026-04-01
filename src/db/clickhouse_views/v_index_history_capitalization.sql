CREATE OR REPLACE VIEW
    moex_olap.v_index_history_capitalization
AS
SELECT
    secid,
    trade_date,
    close,
    capitalization
FROM
    moex_olap.index_history
WHERE
    capitalization > 0;