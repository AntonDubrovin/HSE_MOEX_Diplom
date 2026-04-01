CREATE OR REPLACE VIEW
    moex_olap.v_dividends_yearly
AS
SELECT
    secid,
    toYear(record_date) as year,
    sum(value) as total_dividends,
    count(*) as count_dividends
FROM
    moex_olap.corporate_actions
GROUP BY
    secid, year;