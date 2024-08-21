from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tools import web_scraper, scrape_single_page, extract_media_from_single_page, multiple_page_media
from models import ScrapedBaseUrl, Output
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

@app.post("/scrape/", response_model=Output)
async def scrape_endpoint(scrapper_url: ScrapedBaseUrl):
    try:
        result = await web_scraper(
            url=scrapper_url.url, 
            whitelist=",".join(scrapper_url.whitelist), 
            blacklist=",".join(scrapper_url.blacklist)
        )
        return Output(all_links=result["memory"]["scrapedLinks"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape_single_page/")
async def scrape_single_page_endpoint(scrapper_url: ScrapedBaseUrl):
    try:
        result = await scrape_single_page(url=scrapper_url.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/single_page_media/")
async def single_page_media_endpoint(scrapper_url: ScrapedBaseUrl):
    try:
        result = await extract_media_from_single_page(url=scrapper_url.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/multiple_page_media/")
async def multiple_page_media_endpoint(scrapper_url: ScrapedBaseUrl):
    try:
        result = await multiple_page_media(
            url=scrapper_url.url, 
            whitelist=",".join(scrapper_url.whitelist), 
            blacklist=",".join(scrapper_url.blacklist)
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fetch/")
async def fetch_endpoint(url: str):
    try:
        result = fetch_data(url)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result["data"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))