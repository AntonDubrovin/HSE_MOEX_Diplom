from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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
