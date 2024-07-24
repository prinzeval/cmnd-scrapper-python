from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ScrapedBaseUrl, Output
from scrapper.AllUrlsScrape import ScraperKING
from fetch_db import fetch_data

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust this to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all HTTP headers
)

scraper_king = ScraperKING(link_limit=10000000000)  # Set the link limit here

@app.post("/scrape/", response_model=Output)
async def scrape_endpoint(scrapper_url: ScrapedBaseUrl):
    try:
        whitelist = scrapper_url.whitelist if scrapper_url.whitelist is not None else []
        blacklist = scrapper_url.blacklist if scrapper_url.blacklist is not None else []

        scraped_data = scraper_king.scrape_website_links(scrapper_url.url, whitelist, blacklist)
        return scraped_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/fetch/")
async def fetch_endpoint(url: str):
    try:
        result = fetch_data(url)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result["data"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
