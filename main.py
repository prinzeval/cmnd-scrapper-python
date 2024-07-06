from typing import List
from fastapi import FastAPI, HTTPException, Query
from scrapper.AllUrlsScrape import ScraperKING
from models import ScrapedBaseUrl

app = FastAPI()

# Initialize ScraperKING
scraper_king = ScraperKING()

@app.get("/scrape/", response_model=ScrapedBaseUrl)
async def scrape_endpoint(url: str = Query(..., alias="url", description="URL to scrape")) -> ScrapedBaseUrl:
    try:
        # Scrape website links using ScraperKING instance
        scraped_data = scraper_king.scrape_website_links(url)
        return scraped_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
