from pydantic import BaseModel
from typing import Optional
from datetime import time, date


class CurrentIndex(BaseModel):
    index_code: str
    current_value: float

    board: str = "SNDX"

    open_value: Optional[float] = None
    last_value: Optional[float] = None
    change_percent: Optional[float] = None
    change_points: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[float] = None
    capitalization: Optional[float] = None
    update_time: Optional[time] = None
    trade_date: Optional[date] = None
