from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
import datetime


class Candle(BaseModel):
    secid: str
    open: Decimal
    close: Decimal
    high: Decimal
    low: Decimal
    begin: datetime
    end: datetime
    interval: int

    source: str = "MOEX"

    value: Optional[Decimal] = None
    volume: Optional[int] = None
