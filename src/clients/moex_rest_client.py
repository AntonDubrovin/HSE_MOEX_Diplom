import requests
import pandas as pd
from src.clients.moex_urls import MOEXUrls


class MOEXRestClient:
    BASE_URL = "https://iss.moex.com/iss"

    def send_request(self, url, params):
        # print("-------------")
        print(f"sending {url}")
        response = requests.get(url, params=params)
        print(f"params: {params}")
        data = response.json()
        print(list(data.keys()))
        return data

    def get_instruments(self, params, engine, market, moex_mapper, board):
        url = MOEXUrls.SECURITIES.format(engine=engine, market=market, board=board)
        data = self.send_request(url=url, params=params)

        columns = data["securities"]["columns"]
        rows = data["securities"]["data"]
        print(f"columns len: {len(columns)}")
        print(f"rows len: {len(rows)}")

        instruments = []
        for row in rows:
            moex_data = dict(zip(columns, row))
            instrument = moex_mapper.to_instrument(moex_data, engine, market)
            instruments.append(instrument)
        return instruments

    def get_indices(self, params, engine, market, moex_mapper, board):
        url = MOEXUrls.SECURITIES.format(engine=engine, market=market, board=board)
        data = self.send_request(url=url, params=params)

        columns = data["securities"]["columns"]
        rows = data["securities"]["data"]
        print(f"columns len: {len(columns)}")
        print(f"rows len: {len(rows)}")

        indices = []
        for row in rows:
            moex_data = dict(zip(columns, row))
            index = moex_mapper.to_index(moex_data, engine, market)
            indices.append(index)
        return indices

    def get_current_prices(self, params, engine, market, moex_mapper, board):
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

    def get_current_indices(self, params, engine, market, moex_mapper, board):
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

    def get_candles_by_security(self, secid, params, engine, market):
        # print("start get_candles_by_security")
        url = f"{self.BASE_URL}/engines/{engine}/markets/{market}/securities/{secid}/candles.json"
        data = self.send_request(url=url, params=params)
        print(data["candles"]["columns"])

        df_candles_by_security = pd.DataFrame(
            data["candles"]["data"], columns=data["candles"]["columns"]
        )
        return df_candles_by_security

    def get_dividends_by_security(self, secid, params):
        # print("start get_dividends_by_security")
        url = f"{self.BASE_URL}/securities/{secid}/dividends.json"
        data = self.send_request(url=url, params=params)
        print(data["dividends"]["columns"])

        df_dividends_by_security = pd.DataFrame(
            data["dividends"]["data"], columns=data["dividends"]["columns"]
        )
        return df_dividends_by_security

    def get_info_by_security(self, secid, params, engine, market):
        # print("start get_info_by_security")
        url = f"{self.BASE_URL}/history/engines/{engine}/markets/{market}/securities/{secid}.json"
        data = self.send_request(url=url, params=params)
        print(data["history"]["columns"])

        df_info_by_security = pd.DataFrame(
            data["history"]["data"], columns=data["history"]["columns"]
        )
        return df_info_by_security

    def get_index_history(self, params, engine, market):
        # print("start get_index_history")
        url = f"{self.BASE_URL}/engines/{engine}/markets/{market}/analytics.json"
        data = self.send_request(url=url, params=params)
        print(data["history"]["columns"])

        df_index_history = pd.DataFrame(data["history"]["data"], columns=data["history"]["columns"])
        return df_index_history
