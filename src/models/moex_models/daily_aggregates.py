from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
from datetime import date


class DailyAggregates(BaseModel):
    secid: str
    trade_date: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal

    volume: Optional[int] = None
    value: Optional[Decimal] = None
    num_trades: Optional[int] = None
    waprice: Optional[Decimal] = None
    currency: Optional[str] = None
