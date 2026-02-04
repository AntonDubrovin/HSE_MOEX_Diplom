from pydantic import BaseModel
from typing import Optional


class CurrentPrice(BaseModel):
    secid: str
    price: float

    volume: int = 0

    change: Optional[float] = None
