from typing import Optional

from pydantic import BaseModel


class CurrentPrice(BaseModel):
    secid: str
    price: float

    volume: int = 0

    change: Optional[float] = None
