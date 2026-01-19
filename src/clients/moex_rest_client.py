import datetime

import requests
import pandas as pd

from config.settings import Settings
from moex_mapper import MOEXMapper
from src.db.postgres_dao import PostgresDAO


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

    def get_tqbr_securities(self, params, engine, market, moex_mapper):
        url = f"{self.BASE_URL}/engines/{engine}/markets/{market}/boards/TQBR/securities.json"
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

    def get_current_indices(self, params, engine, market):
        # print("start get_current_indices")
        url = f"{self.BASE_URL}/engines/{engine}/markets/{market}/analytics.json"
        data = self.send_request(url=url, params=params)
        print(data["marketdata"]["columns"])

        df_current_indices = pd.DataFrame(
            data["marketdata"]["data"], columns=data["marketdata"]["columns"]
        )
        return df_current_indices

    def get_index_history(self, params, engine, market):
        # print("start get_index_history")
        url = f"{self.BASE_URL}/engines/{engine}/markets/{market}/analytics.json"
        data = self.send_request(url=url, params=params)
        print(data["history"]["columns"])

        df_index_history = pd.DataFrame(data["history"]["data"], columns=data["history"]["columns"])
        return df_index_history

    def get_indices_metadata(self, params, engine, market):
        # print("start get_indices_metadata")
        url = f"{self.BASE_URL}/engines/{engine}/markets/{market}/analytics.json"
        data = self.send_request(url=url, params=params)
        print(data["securities"]["columns"])

        df_indices_metadata = pd.DataFrame(
            data["securities"]["data"], columns=data["securities"]["columns"]
        )
        return df_indices_metadata

    def main(self, moex_mapper, settings):
        instruments = self.get_tqbr_securities(
            params={
                "securities.columns": "SECID,SECNAME,SHORTNAME,ISIN,SECTYPE,LOTSIZE,CURRENCYID,BOARDID"
            },
            engine="stock",
            market="shares",
            moex_mapper=moex_mapper,
        )
        print(instruments)
        postgres_dao = PostgresDAO(settings)
        for instrument in instruments:
            postgres_dao.insert_instrument(instrument)
        print("Вставлены инструменты")
        # candles_by_security = self.get_candles_by_security(
        #     secid="SBER",
        #     params={"from": "2026-01-01", "till": "2026-01-31", "interval": 1},
        #     engine="stock",
        #     market="shares",
        # )
        # indices_metadata = self.get_indices_metadata(
        #     params={"boardid": "SNDX"},
        #     engine="stock",
        #     market="index",
        # )
        # corporate_actions_by_security = self.get_dividends_by_security(secid="SBER", params={})
        # daily_aggregates_by_security = self.get_info_by_security(
        #     secid="SBER",
        #     params={"date": "2026-01-14"},
        #     engine="stock",
        #     market="shares",
        # )
        # current_indices = self.get_current_indices(
        #     params={
        #         "boardid": "SNDX",
        #         "marketdata.columns": "SECID,BOARDID,CURRENTVALUE,LASTCHANGEPRC,OPENVALUE,LASTVALUE,HIGH,LOW,VALTODAY,CAPITALIZATION,UPDATETIME,TRADEDATE",
        #     },
        #     engine="stock",
        #     market="index",
        # )
        # index_history = self.get_index_history(
        #     params={
        #         "boardid": "SNDX",
        #         "secid": "IMOEX",
        #         "from": "2026-01-01",
        #         "till": "2026-01-31",
        #         "history.columns": "TRADEDATE,SECID,BOARDID,OPEN,HIGH,LOW,CLOSE,VALUE,CAPITALIZATION,CURRENCYID,TRADINGSESSION,RECALC_DATE",
        #     },
        #     engine="stock",
        #     market="index",
        # )


if __name__ == "__main__":
    moex = MOEXRestClient()
    moex_mapper = MOEXMapper()
    settings = Settings()
    moex.main(moex_mapper, settings)
