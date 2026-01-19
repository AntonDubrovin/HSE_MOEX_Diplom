from pydantic import BaseModel
from typing import Optional


class Instrument(BaseModel):
    secid: str
    short_name: str
    sec_name: str
    sec_type: str

    lot_size: int = 1
    currency: str = "SUR"
    board: str = "TQBR"
    engine: str = "stock"
    market: str = "shares"

    isin: Optional[str] = None
