import random
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from models import ScrapedBaseUrl
from scrapper.Baseurlscrape import Scraper

class ScraperKING:
    def __init__(self):
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)

    def __del__(self):
        self.driver.quit()

    def scrape_website_links(self, base_url: str):
        all_links = set()
        try:
            # Initialize the BaseUrl scraper
            base_scraper = Scraper()
            base_urls = base_scraper.scrape(base_url)

            # Scrape each base URL using Selenium
            for url in base_urls:
                print(f"Starting to scrape URL: {url}")
                self.driver.get(url)
                delay = random.randint(2, 7)
                time.sleep(delay)
                
                page_source = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                urllinks = {
                    urljoin(url, a['href']) for a in page_source.find_all('a', href=True)
                    if not (a['href'].startswith('https') or '#' in a['href'])
                }
                
                urllinks = {link for link in urllinks if link.rstrip('/') != url.rstrip('/')}
                
                print(f"Found links on {url}: {urllinks}")
                all_links.update(urllinks)
            
            return ScrapedBaseUrl(url=base_url, links=list(all_links))

        except Exception as e:
            print(f"Error scraping {base_url}: {e}")
            return ScrapedBaseUrl(url=base_url, links=[])

