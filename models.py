from pydantic import BaseModel
from typing import List

class ScrapedBaseUrl(BaseModel):
    url: str
    links: List[str]
