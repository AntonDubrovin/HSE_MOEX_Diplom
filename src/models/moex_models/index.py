from pydantic import BaseModel


class Index(BaseModel):
    secid: str
    index_name: str

    engine: str = "stock"
    market: str = "index"
