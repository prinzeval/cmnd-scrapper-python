import os
from pydantic import BaseModel, Field
from typing import Dict, List
from scrapper.AllUrlsScrape import ScraperKING
from scrapper.Url_Info import bring_data
from scrapper.media import extract_media_links
import requests
from bs4 import BeautifulSoup

# Define schemas for the tools
class WebScraperSchema(BaseModel):
    url: str = Field(..., title="Base URL", description="The base URL to start scraping from.")
    whitelist: str = Field("", title="Whitelist", description="Comma-separated URLs or substrings to include in the scrape.")
    blacklist: str = Field("", title="Blacklist", description="Comma-separated URLs or substrings to exclude from the scrape.")

class SinglePageScraperSchema(BaseModel):
    url: str = Field(..., title="URL", description="The URL of the page to scrape.")

class SinglePageMediaSchema(BaseModel):
    url: str = Field(..., title="URL", description="The URL of the page to scrape for media.")

class MultiplePageMediaSchema(BaseModel):
    url: str = Field(..., title="Base URL", description="The base URL to start scraping from.")
    whitelist: str = Field("", title="Whitelist", description="Comma-separated URLs or substrings to include in the scrape.")
    blacklist: str = Field("", title="Blacklist", description="Comma-separated URLs or substrings to exclude from the scrape.")

# Define the web scraping function
async def web_scraper(url: str, whitelist: str = "", blacklist: str = "", memory: Dict = {}):
    try:
        # Convert comma-separated strings to lists, handle empty strings
        whitelist_list = [item.strip() for item in whitelist.split(",") if item.strip()] if whitelist else []
        blacklist_list = [item.strip() for item in blacklist.split(",") if item.strip()] if blacklist else []

        # Initialize the scraper (replace with your actual scraper class)
        scraper = ScraperKING()

        # Perform the scraping
        result = scraper.scrape_website_links(url, whitelist_list, blacklist_list)

        # Update memory with scraped links
        memory["scrapedLinks"] = result.get("all_links", [])

        # Return the result
        return {
            "responseString": f"Scraped {len(memory['scrapedLinks'])} links.",
            "memory": memory
        }
    except Exception as e:
        # Return an error response
        return {
            "responseString": f"An error occurred: {str(e)}",
            "memory": memory
        }

# Define the single page scraping function
async def scrape_single_page(url: str, memory: Dict = {}):
    try:
        # Since bring_data expects lists for URLs, we'll wrap the single URL in a list
        needed_data = [url]
        whitelist = [url]  # Automatically duplicating the input link into the whitelist
        blacklist = []

        # Perform the scraping (replace with your actual function)
        bring_data(needed_data, whitelist, blacklist)

        # Assuming bring_data does not return a value, we manually set the memory
        memory["scrapedContent"] = "Content from the single page scrape is now available."

        # Return the result
        return {
            "responseString": f"Scraped content and media URLs from the page {url}.",
            "memory": memory
        }
    except Exception as e:
        # Return an error response
        return {
            "responseString": f"An error occurred: {str(e)}",
            "memory": memory
        }

# Define the single page media extraction function
async def extract_media_from_single_page(url: str, memory: Dict = {}):
    try:
        # Fetch the page content
        response = requests.get(url)
        page_source = BeautifulSoup(response.content, 'html.parser')

        # Extract media links (replace with your actual extraction function)
        media_links = extract_media_links(page_source, url)

        # Update memory with extracted media links
        memory["mediaLinks"] = media_links

        # Return the result
        return {
            "responseString": f"Extracted {len(media_links)} media links from the page {url}.",
            "memory": memory
        }
    except Exception as e:
        # Return an error response
        return {
            "responseString": f"An error occurred: {str(e)}",
            "memory": memory
        }

# Define the multiple page media extraction function
async def multiple_page_media(url: str, whitelist: str = "", blacklist: str = "", memory: Dict = {}):
    try:
        # Convert comma-separated strings to lists, handle empty strings
        whitelist_list = [item.strip() for item in whitelist.split(",") if item.strip()] if whitelist else []
        blacklist_list = [item.strip() for item in blacklist.split(",") if item.strip()] if blacklist else []

        # Initialize the scraper (replace with your actual scraper class)
        scraper = ScraperKING()

        # Perform the scraping to get all links
        result = scraper.scrape_website_links(url, whitelist_list, blacklist_list)
        all_links = result.get("all_links", [])

        # Extract media links from all the scraped links
        media_links = []
        for link in all_links:
            response = requests.get(link)
            page_source = BeautifulSoup(response.content, 'html.parser')
            media_links.extend(extract_media_links(page_source, link))

        # Update memory with extracted media links
        memory["mediaLinks"] = media_links

        # Return the result
        return {
            "responseString": f"Extracted {len(media_links)} media links from the website {url}.",
            "memory": memory
        }
    except Exception as e:
        # Return an error response
        return {
            "responseString": f"An error occurred: {str(e)}",
            "memory": memory
        }

# Define custom JSON schema function
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

# Define the tools list with the updated tools
tools = [
    {
        "name": "web_scraper",
        "description": "Scrapes a website for links based on provided parameters.",
        "parameters": custom_json_schema(WebScraperSchema),
        "runCmd": web_scraper,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": True,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "scrape_single_page",
        "description": "Scrapes a single webpage for content and media URLs.",
        "parameters": custom_json_schema(SinglePageScraperSchema),
        "runCmd": scrape_single_page,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "single_page_media",
        "description": "Extracts media content (images, videos, audio, PDFs) from a single webpage.",
        "parameters": custom_json_schema(SinglePageMediaSchema),
        "runCmd": extract_media_from_single_page,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
    {
        "name": "multiple_page_media",
        "description": "Extracts media content (images, videos, audio, PDFs) from multiple pages of a website.",
        "parameters": custom_json_schema(MultiplePageMediaSchema),
        "runCmd": multiple_page_media,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": True,
        "rerun": True,
        "rerunWithDifferentParameters": True
    }
]
