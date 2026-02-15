from pydantic import BaseModel
from typing import Optional
from datetime import date


class IndexHistory(BaseModel):
    index_code: str
    trade_date: date
    open: float
    high: float
    low: float
    close: float

    board: str = "SNDX"
    value: float = 0
    volume: float = 0
    capitalization: float = 0

    currency: Optional[str] = None
    yield_value: Optional[float] = None
    duration: Optional[float] = None
    trading_session: Optional[str] = None
    recalc_date: Optional[date] = None
