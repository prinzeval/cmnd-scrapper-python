from fastapi import FastAPI, HTTPException
from models import ScrapedBaseUrl, Output
from scrapper.AllUrlsScrape import ScraperKING

app = FastAPI()

# Initialize ScraperKING
scraper_king = ScraperKING()

@app.post("/scrape/", response_model=Output)
async def scrape_endpoint(scrapper_url: ScrapedBaseUrl):
    try:
        # Scrape website links using ScraperKING instance
        url = scrapper_url.url
        whitelist = scrapper_url.whitelist if scrapper_url.whitelist is not None else []
        blacklist = scrapper_url.blacklist if scrapper_url.blacklist is not None else []

        scraped_data = scraper_king.scrape_website_links(url, whitelist, blacklist)
        return scraped_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
