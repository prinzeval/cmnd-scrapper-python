from pydantic import BaseModel
from typing import List, Optional

class ScrapedBaseUrl(BaseModel):
    url: str
    whitelist: Optional[List[str]] = []
    blacklist: Optional[List[str]] = []

class Output(BaseModel):
    all_links: List[str] = []
