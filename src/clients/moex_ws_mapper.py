from src.models.moex_models.current_price import CurrentPrice


class MOEXWebSocketMapper:
    def extract_float(self, value):
        if isinstance(value, list):
            return value[0]
        return value

    def to_current_price(self, ws_data):
        last = self.extract_float(ws_data.get("LAST"))
        if last is None:
            return

        return CurrentPrice(
            secid=ws_data.get("TICKER", "").split(".")[-1],
            price=last,
            volume=self.extract_float(ws_data.get("VOLTODAY")) or 0,
            change=self.extract_float(ws_data.get("CHANGE")),
        )
