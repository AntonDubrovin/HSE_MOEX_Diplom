from pydantic import BaseModel
from typing import Optional
from datetime import date


class Dividend(BaseModel):
    secid: str
    record_date: date
    value: float

    action_type: str = "dividend"

    isin: Optional[str] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    source_url: Optional[str] = None
