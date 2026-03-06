from datetime import date

from clickhouse_driver import Client


class ClickHouseDAO:
    def __init__(self, settings):
        self.client = Client(
            host=settings.CLICKHOUSE_HOST,
            port=settings.CLICKHOUSE_PORT,
            user=settings.CLICKHOUSE_USER,
            password=settings.CLICKHOUSE_PASSWORD,
            database=settings.CLICKHOUSE_DB,
        )

    def close(self):
        self.client.disconnect()

    def insert_instruments(self, instruments):
        data_insert_instruments = []
        for instrument in instruments:
            data_insert_instruments.append(
                {
                    "secid": instrument.secid,
                    "sec_name": instrument.sec_name,
                    "sec_type": instrument.sec_type,
                    "short_name": instrument.short_name,
                    "isin": instrument.isin,
                    "lot_size": instrument.lot_size,
                    "currency": instrument.currency,
                    "board": instrument.board,
                    "engine": instrument.engine,
                    "market": instrument.market,
                }
            )

        query_insert_instruments_ref = (
            "INSERT INTO moex_olap.instruments_ref "
            "("
            " secid, "
            " sec_name, "
            " sec_type, "
            " short_name, "
            " isin, "
            " lot_size, "
            " currency, "
            " board, "
            " engine, "
            " market "
            ") "
            "VALUES "
        )

        self.client.execute(query_insert_instruments_ref, data_insert_instruments)

        # делаем optimize, тк наша таблица - справочник, и дублей не должно быть
        query_optimize_instruments_ref = "OPTIMIZE TABLE moex_olap.instruments_ref FINAL"
        self.client.execute(query_optimize_instruments_ref)

    def insert_indices(self, indices):
        data_insert_indices = []
        for index in indices:
            data_insert_indices.append(
                {
                    "secid": index.secid,
                    "index_name": index.index_name,
                    "engine": index.engine,
                    "market": index.market,
                }
            )

        query_insert_indices = (
            "INSERT INTO moex_olap.indices_ref "
            "("
            " secid, "
            " index_name, "
            " engine, "
            " market "
            ") "
            "VALUES "
        )

        self.client.execute(query_insert_indices, data_insert_indices)

        # делаем optimize, тк наша таблица - справочник, и дублей не должно быть
        query_optimize_indices_ref = "OPTIMIZE TABLE moex_olap.indices_ref FINAL"
        self.client.execute(query_optimize_indices_ref)

    def insert_candles(self, candles):
        data_insert_candles = []
        for c in candles:
            data_insert_candles.append(
                {
                    "secid": c.secid,
                    "open": c.open,
                    "close": c.close,
                    "high": c.high,
                    "low": c.low,
                    "value": c.value,
                    "volume": c.volume,
                    "begin": c.begin,
                    "end": c.end,
                    "interval": c.interval,
                    "source": c.source,
                }
            )

        query_insert_candles = (
            "INSERT INTO moex_olap.candles "
            "("
            " secid, "
            " open, "
            " close, "
            " high, "
            " low, "
            " value, "
            " volume, "
            " begin, "
            " end, "
            " interval, "
            " source "
            ") "
            "VALUES "
        )

        self.client.execute(
            query_insert_candles,
            data_insert_candles,
            settings={"max_partitions_per_insert_block": 0},
        )

        # делаем optimize, тк можем запросить данные за одинаковые промежутки 2+ раз, тогда будут дубли
        query_optimize_candles_ref = "OPTIMIZE TABLE moex_olap.candles FINAL"
        self.client.execute(query_optimize_candles_ref)

    def insert_corporate_actions(self, dividends):
        data_insert_corporate_actions = []
        for d in dividends:
            data_insert_corporate_actions.append(
                {
                    "secid": d.secid,
                    "isin": d.isin,
                    "record_date": d.record_date,
                    "value": d.value,
                    "currency": d.currency,
                    "action_type": d.action_type,
                    "status": d.status,
                    "source_url": d.source_url,
                }
            )

        query_insert_corporate_actions = (
            "INSERT INTO moex_olap.corporate_actions "
            "("
            " secid, "
            " isin, "
            " record_date, "
            " value, "
            " currency, "
            " action_type, "
            " status, "
            " source_url"
            ") "
            "VALUES "
        )

        self.client.execute(query_insert_corporate_actions, data_insert_corporate_actions)

        # делаем optimize, тк можем выполнить 2+ раз и будут дубли
        query_optimize_corporate_actions_ref = "OPTIMIZE TABLE moex_olap.corporate_actions FINAL"
        self.client.execute(query_optimize_corporate_actions_ref)

    def insert_daily_aggregates(self, daily_aggregates):
        data_insert_daily_aggregates = []
        for a in daily_aggregates:
            data_insert_daily_aggregates.append(
                {
                    "secid": a.secid,
                    "trade_date": a.trade_date,
                    "open": a.open,
                    "high": a.high,
                    "low": a.low,
                    "close": a.close,
                    "volume": a.volume,
                    "value": a.value,
                    "num_trades": a.num_trades,
                    "waprice": a.waprice,
                    "currency": a.currency,
                }
            )

        query_insert_daily_aggregates = (
            "INSERT INTO moex_olap.daily_aggregates "
            "("
            " secid, "
            " trade_date, "
            " open, "
            " high, "
            " low, "
            " close, "
            " volume, "
            " value, "
            " num_trades, "
            " waprice, "
            " currency"
            ") "
            "VALUES "
        )

        self.client.execute(
            query_insert_daily_aggregates,
            data_insert_daily_aggregates,
            settings={"max_partitions_per_insert_block": 0},
        )

        # делаем optimize, тк можем выполнить 2+ раз и будут дубли
        query_optimize_daily_aggregates_ref = "OPTIMIZE TABLE moex_olap.daily_aggregates FINAL"
        self.client.execute(query_optimize_daily_aggregates_ref)

    def insert_index_history(self, index_history):
        data_insert_index_history = []
        for h in index_history:
            data_insert_index_history.append(
                {
                    "secid": h.secid,
                    "board": h.board,
                    "trade_date": h.trade_date,
                    "open": h.open,
                    "high": h.high,
                    "low": h.low,
                    "close": h.close,
                    "value": h.value,
                    "volume": h.volume,
                    "capitalization": h.capitalization,
                    "currency": h.currency,
                    "yield": h.yield_value,
                    "duration": h.duration,
                    "trading_session": h.trading_session,
                    "recalc_date": h.recalc_date,
                }
            )

        query_insert_index_history = (
            "INSERT INTO moex_olap.index_history "
            "("
            " secid, "
            " board, "
            " trade_date, "
            " open, "
            " high, "
            " low, "
            " close, "
            " value, "
            " volume, "
            " capitalization, "
            " currency, "
            " yield, "
            " duration, "
            " trading_session, "
            " recalc_date"
            ") "
            "VALUES "
        )

        self.client.execute(
            query_insert_index_history,
            data_insert_index_history,
            settings={"max_partitions_per_insert_block": 0},
        )

        # делаем optimize, тк можем выполнить 2+ раз и будут дубли
        query_optimize_index_history = "OPTIMIZE TABLE moex_olap.index_history FINAL"
        self.client.execute(query_optimize_index_history)
