import os
from pydantic import BaseModel, Field
from typing import List
from scrapper.Url_Info import bring_data
from scrapper.AllUrlsScrape import ScraperKING

class ScrapeBaseUrlSchema(BaseModel):
    url: str = Field(..., title="URL", description="URL to scrape")
    whitelist: List[str] = Field([], title="Whitelist", description="Whitelist of URLs to include")
    blacklist: List[str] = Field([], title="Blacklist", description="Blacklist of URLs to exclude")

async def scrape_website(url: str, whitelist: List[str], blacklist: List[str], memory: dict):
    scraper_king = ScraperKING(link_limit=10)
    scraped_data = scraper_king.scrape_website_links(url, whitelist, blacklist)
    bring_data(scraped_data, whitelist, blacklist)
    return {
        "responseString": f"Scraped data: {scraped_data}",
        "memory": memory
    }

def custom_json_schema(model):
    schema = model.schema()
    properties_formatted = {
        k: {
            "title": v.get("title"),
            "type": v.get("type")
        } for k, v in schema["properties"].items()
    }

    return {
        "type": "object",
        "default": {},
        "properties": properties_formatted,
        "required": schema.get("required", [])
    }

tools = [
    {
        "name": "scrape_website",
        "description": "Scrapes a website and returns the extracted links",
        "parameters": custom_json_schema(ScrapeBaseUrlSchema),
        "runCmd": scrape_website,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    }
]
