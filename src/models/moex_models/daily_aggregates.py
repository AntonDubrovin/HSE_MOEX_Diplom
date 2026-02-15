from pydantic import BaseModel
from typing import Optional
from datetime import date


class DailyAggregates(BaseModel):
    secid: str
    trade_date: date
    open: float
    high: float
    low: float
    close: float

    volume: int = 0
    value: float = 0
    num_trades: int = 0

    waprice: Optional[float] = None
    currency: Optional[str] = None
