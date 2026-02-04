from pydantic import BaseModel


class Index(BaseModel):
    index_code: str
    index_name: str

    engine: str = "stock"
    market: str = "index"
