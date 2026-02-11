from src.models.moex_models.current_price import CurrentPrice
from src.models.moex_models.index import Index
from src.models.moex_models.instrument import Instrument
from src.models.moex_models.current_index import CurrentIndex


class MOEXMapper:
    def to_instrument(self, moex_data, engine, market):
        return Instrument(
            secid=moex_data.get("SECID").upper(),
            sec_name=moex_data.get("SECNAME"),
            sec_type=moex_data.get("SECTYPE"),
            short_name=moex_data.get("SHORTNAME"),
            lot_size=moex_data.get("LOTSIZE", 1),
            currency=moex_data.get("CURRENCYID", "SUR"),
            board=moex_data.get("BOARDID", "TQBR"),
            engine=engine,
            market=market,
            isin=moex_data.get("ISIN"),
        )

    def to_index(self, moex_data, engine, market):
        return Index(
            index_code=moex_data.get("SECID").upper(),
            index_name=moex_data.get("SHORTNAME"),
            engine=engine,
            market=market,
        )

    def to_current_price(self, moex_data):
        if moex_data.get("LAST") is None:
            return

        return CurrentPrice(
            secid=moex_data.get("SECID").upper(),
            price=float(moex_data.get("LAST")),
            volume=int(moex_data.get("VOLTODAY", 0)),
            change=moex_data.get("LASTTOPREVPRICE", ""),
        )

    def to_current_index(self, moex_data):
        if moex_data.get("CURRENTVALUE") is None:
            return

        return CurrentIndex(
            index_code=moex_data.get("SECID").upper(),
            current_value=float(moex_data.get("CURRENTVALUE")),
            board=moex_data.get("BOARDID", "SNDX"),
            open_value=moex_data.get("OPENVALUE"),
            last_value=moex_data.get("LASTVALUE"),
            change_percent=moex_data.get("LASTCHANGEPRC"),
            change_points=moex_data.get("LASTCHANGE"),
            high=moex_data.get("HIGH"),
            low=moex_data.get("LOW"),
            volume=moex_data.get("VALTODAY"),
            capitalization=moex_data.get("CAPITALIZATION"),
            update_time=moex_data.get("UPDATETIME"),
            trade_date=moex_data.get("TRADEDATE"),
        )
