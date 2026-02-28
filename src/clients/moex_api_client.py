import pandas as pd
import requests

from src.clients.moex_urls import MOEXUrls


class MOEXApiClient:
    def send_request(self, url, params):
        # print("-------------")
        print(f"sending {url}")
        response = requests.get(url, params=params)
        print(f"params: {params}")
        data = response.json()
        print(list(data.keys()))
        return data

    def get_instruments(self, params, engine, market, board, moex_mapper):
        url = MOEXUrls.SECURITIES.format(engine=engine, market=market, board=board)
        data = self.send_request(url=url, params=params)

        columns = data["securities"]["columns"]
        rows = data["securities"]["data"]
        # print(f"columns len: {len(columns)}")
        # print(f"rows len: {len(rows)}")

        instruments = []
        for row in rows:
            moex_data = dict(zip(columns, row))
            instrument = moex_mapper.to_instrument(moex_data, engine, market)
            instruments.append(instrument)
        return instruments

    def get_indices(self, params, engine, market, board, moex_mapper):
        url = MOEXUrls.SECURITIES.format(engine=engine, market=market, board=board)
        data = self.send_request(url=url, params=params)

        columns = data["securities"]["columns"]
        rows = data["securities"]["data"]
        # print(f"columns len: {len(columns)}")
        # print(f"rows len: {len(rows)}")

        indices = []
        for row in rows:
            moex_data = dict(zip(columns, row))
            index = moex_mapper.to_index(moex_data, engine, market)
            indices.append(index)
        return indices

    def get_current_prices(self, params, engine, market, board, moex_mapper):
        url = MOEXUrls.SECURITIES.format(engine=engine, market=market, board=board)
        data = self.send_request(url=url, params=params)

        columns = data["marketdata"]["columns"]
        rows = data["marketdata"]["data"]
        print(f"columns len: {len(columns)}")
        print(f"rows len: {len(rows)}")

        current_prices = []
        for row in rows:
            moex_data = dict(zip(columns, row))
            current_price = moex_mapper.to_current_price(moex_data)
            if current_price:
                current_prices.append(current_price)
        return current_prices

    def get_current_indices(self, params, engine, market, board, moex_mapper):
        url = MOEXUrls.SECURITIES.format(engine=engine, market=market, board=board)
        data = self.send_request(url=url, params=params)

        columns = data["marketdata"]["columns"]
        rows = data["marketdata"]["data"]
        print(f"columns len: {len(columns)}")
        print(f"rows len: {len(rows)}")

        current_indices = []
        for row in rows:
            moex_data = dict(zip(columns, row))
            current_index = moex_mapper.to_current_index(moex_data)
            if current_index:
                current_indices.append(current_index)
        return current_indices

    def get_statistics_analytics(self, params, engine, market):
        url = f"{self.BASE_URL}/statistics/engines/{engine}/markets/{market}/analytics.json"
        data = self.send_request(url=url, params=params)
        print(data["indices"]["columns"])

        df_analytics = pd.DataFrame(data["indices"]["data"], columns=data["indices"]["columns"])
        return df_analytics

    def get_candles_by_security(self, secid, params, engine, market, moex_mapper):
        url = MOEXUrls.CANDLES.format(engine=engine, market=market, secid=secid)
        data_moex_url = self.send_request(url=url, params=params)

        columns = data_moex_url["candles"]["columns"]
        data_all = data_moex_url["candles"]["data"]
        print(f"columns len: {len(columns)}")
        print(f"rows len: {len(data_all)}")

        while True:
            params["start"] = len(data_all)
            data_moex_url = self.send_request(url=url, params=params)
            data = data_moex_url["candles"]["data"]
            if not data:
                break
            data_all.extend(data)
            print(f"rows len: {len(data)}")

        candles = []
        for row in data_all:
            moex_data = dict(zip(columns, row))
            candle = moex_mapper.to_candle(moex_data, secid)
            if candle:
                candles.append(candle)
        return candles

    def get_dividends_by_security(self, secid, params, moex_mapper):
        url = MOEXUrls.DIVIDENDS.format(secid=secid)
        data = self.send_request(url=url, params=params)

        columns = data["dividends"]["columns"]
        rows = data["dividends"]["data"]
        # print(f"columns len: {len(columns)}")
        # print(f"rows len: {len(rows)}")

        dividends = []
        for row in rows:
            moex_data = dict(zip(columns, row))
            dividend = moex_mapper.to_dividend(moex_data)
            if dividend:
                dividends.append(dividend)
        return dividends

    def get_daily_aggregates(self, secid, params, engine, market, board, moex_mapper):
        url = MOEXUrls.HISTORY.format(engine=engine, market=market, board=board, secid=secid)
        data_moex_url = self.send_request(url=url, params=params)

        columns = data_moex_url["history"]["columns"]
        data_all = data_moex_url["history"]["data"]
        history_cursor_columns = data_moex_url["history.cursor"]["columns"]
        history_cursor_data = data_moex_url["history.cursor"]["data"][0]

        # print(f"columns len: {len(columns)}")
        # print(f"rows len: {len(rows)}")
        print(history_cursor_columns)
        print(history_cursor_data)

        moex_history_cursors = dict(zip(history_cursor_columns, history_cursor_data))

        pagesize = moex_history_cursors.get("PAGESIZE")
        total = moex_history_cursors.get("TOTAL")
        index = moex_history_cursors.get("INDEX")

        while index + pagesize < total:
            url = MOEXUrls.HISTORY.format(engine=engine, market=market, board=board, secid=secid)
            params["start"] = index + pagesize
            data_moex_url = self.send_request(url=url, params=params)

            history_cursor_columns = data_moex_url["history.cursor"]["columns"]
            history_cursor_data = data_moex_url["history.cursor"]["data"][0]

            print(history_cursor_columns)
            print(history_cursor_data)

            moex_history_cursors = dict(zip(history_cursor_columns, history_cursor_data))

            pagesize = moex_history_cursors.get("PAGESIZE")
            total = moex_history_cursors.get("TOTAL")
            index = moex_history_cursors.get("INDEX")

            data = data_moex_url["history"]["data"]
            print(f"rows len: {len(data)}")
            data_all.extend(data)

        daily_aggregates = []
        for row in data_all:
            moex_data = dict(zip(columns, row))
            aggregate = moex_mapper.to_daily_aggregates(moex_data)
            if aggregate:
                daily_aggregates.append(aggregate)
        return daily_aggregates

    def get_index_history(self, secid, params, engine, market, board, moex_mapper):
        url = MOEXUrls.HISTORY.format(engine=engine, market=market, board=board, secid=secid)
        data_moex_url = self.send_request(url=url, params=params)

        columns = data_moex_url["history"]["columns"]
        data_all = data_moex_url["history"]["data"]
        history_cursor_columns = data_moex_url["history.cursor"]["columns"]
        history_cursor_data = data_moex_url["history.cursor"]["data"][0]

        # print(f"columns len: {len(columns)}")
        # print(f"rows len: {len(rows)}")
        print(history_cursor_columns)
        print(history_cursor_data)

        moex_history_cursors = dict(zip(history_cursor_columns, history_cursor_data))

        pagesize = moex_history_cursors.get("PAGESIZE")
        total = moex_history_cursors.get("TOTAL")
        index = moex_history_cursors.get("INDEX")

        while index + pagesize < total:
            url = MOEXUrls.HISTORY.format(engine=engine, market=market, board=board, secid=secid)
            params["start"] = index + pagesize
            data_moex_url = self.send_request(url=url, params=params)

            history_cursor_columns = data_moex_url["history.cursor"]["columns"]
            history_cursor_data = data_moex_url["history.cursor"]["data"][0]

            print(history_cursor_columns)
            print(history_cursor_data)

            moex_history_cursors = dict(zip(history_cursor_columns, history_cursor_data))

            pagesize = moex_history_cursors.get("PAGESIZE")
            total = moex_history_cursors.get("TOTAL")
            index = moex_history_cursors.get("INDEX")

            data = data_moex_url["history"]["data"]
            print(f"rows len: {len(data)}")
            data_all.extend(data)

        index_history = []
        for row in data_all:
            moex_data = dict(zip(columns, row))
            record = moex_mapper.to_index_history(moex_data)
            if record:
                index_history.append(record)
        return index_history
