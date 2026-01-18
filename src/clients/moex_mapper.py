from typing import Dict, Any
from src.models.moex_models.instrument import Instrument


class MOEXMapper:
    @staticmethod
    def to_instrument(moex_data, engine, market):
        return Instrument(
            secid=moex_data.get("SECID", "").upper(),
            sec_name=moex_data.get("SECNAME"),
            # TODO добавить sectype
            short_name=moex_data.get("SHORTNAME", ""),
            lot_size=moex_data.get("LOTSIZE", 1),
            currency=moex_data.get("CURRENCYID", "SUR"),
            board=moex_data.get("BOARDID", "TQBR"),
            engine=engine,
            market=market,
            isin=moex_data.get("ISIN"),
        )
