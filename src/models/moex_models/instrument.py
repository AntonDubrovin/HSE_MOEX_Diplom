from pydantic import BaseModel
from typing import Optional


class Instrument(BaseModel):
    secid: str
    short_name: str
    sec_name: str

    lot_size: int = 1
    currency: str = "SUR"
    board: str = "TQBR"
    engine: str = "stock"
    market: str = "shares"

    isin: Optional[str] = None
# TODO добавить sec_type
# SECTYPE на Московской бирже (MOEX) — тип ценной бумаги.
# moex.com
# алготрейдинг.рф
# Некоторые возможные значения поля SecType:
# 1 — акция обыкновенная;
# 2 — акция привилегированная;
# 3 — государственные облигации;
# 4 — региональные облигации;
# 5 — облигации центральных банков;
# 6 — корпоративные облигации;
# 7 — облигации МФО;
# 8 — биржевые облигации;
# 9 — паи открытых ПИФов;
# A — паи интервальных ПИФов;
# B — паи закрытых ПИФов;
# C — муниципальные облигации;
# D — депозитарные расписки;
# E — бумаги иностранных инвестиционных фондов (ETF);
# F — ипотечный сертификат;
# G — корзина бумаг;
# H — дополнительный идентификатор списка;
# I — ETC (товарные инструменты);
# J — пай биржевого ПИФа (Exchange Investment Unit share).