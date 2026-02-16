from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Candle(BaseModel):
    secid: str
    open: float
    close: float
    high: float
    low: float
    begin: datetime
    end: datetime
    interval: int

    source: str = "MOEX"
    value: float = 0
    volume: int = 0
