from src.models.moex_models.current_price import CurrentPrice
from src.models.moex_models.index import Index
from src.models.moex_models.instrument import Instrument


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
            index_code=moex_data.get("indexid").upper(),
            index_name=moex_data.get("shortname"),
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
