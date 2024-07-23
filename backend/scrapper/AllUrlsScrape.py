import random
import time
from collections import deque
from typing import List
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .Url_Info import bring_data
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScraperKING:
    def __init__(self, link_limit=100):
        self.url_pattern = re.compile(
            r'(http(s)?://)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)',
            re.IGNORECASE
        )
        self.image_extensions = re.compile(r'\.(jpg|jpeg|png|gif|webp)$', re.IGNORECASE)
        self.all_links = set()
        self.visited_links = set()
        self.link_limit = link_limit

    def is_valid_url(self, url, base_url):
        return self.url_pattern.match(url) is not None and url.startswith(base_url)

    def is_valid_link(self, url):
        return not self.image_extensions.search(url)

    def is_in_whitelist(self, url, whitelist):
        return any(item in url for item in whitelist) if whitelist else True

    def is_in_blacklist(self, url, blacklist):
        return any(item in url for item in blacklist)

    def fetch_with_selenium(self, url):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')

        logger.info(f"Fetching {url} with Selenium.")
        with webdriver.Chrome(options=options) as driver:
            driver.get(url)
            time.sleep(random.uniform(0, 1))
            return BeautifulSoup(driver.page_source, 'html.parser')

    def scrape_website_links(self, base_url: str, whitelist: List[str], blacklist: List[str]):
        output_data = {}
        found_whitelisted_urls = set()

        try:
            if not (base_url.startswith('http://') or base_url.startswith('https://')):
                base_url = 'http://' + base_url

            logger.info(f"Starting scraping with base URL: {base_url}")
            link_queue = deque([base_url])
            links_scraped = 0

            if self.is_in_whitelist(base_url, whitelist):
                found_whitelisted_urls.add(base_url)

            while link_queue and links_scraped < self.link_limit:
                url = link_queue.popleft()
                if url in self.visited_links or not self.is_valid_url(url, base_url):
                    continue

                if self.is_in_whitelist(url, whitelist):
                    found_whitelisted_urls.add(url)

                if len(found_whitelisted_urls) == len(whitelist):
                    logger.info("All whitelisted URLs found, stopping further scraping.")
                    break

                if self.is_in_blacklist(url, blacklist):
                    continue

                try:
                    logger.info(f"Scraping URL: {url}")
                    response = requests.get(url)
                    time.sleep(random.uniform(0, 1))

                    if response.status_code == 200:
                        page_source = BeautifulSoup(response.text, 'html.parser')
                    elif response.status_code == 403:
                        page_source = self.fetch_with_selenium(url)
                    else:
                        logger.warning(f"Skipping URL {url} with status code {response.status_code}.")
                        continue

                    urllinks = {
                        urljoin(url, a['href']) for a in page_source.find_all('a', href=True)
                        if self.is_valid_url(urljoin(url, a['href']), base_url) and self.is_valid_link(a['href'])
                    }

                    urllinks = {link for link in urllinks if link.rstrip('/') != url.rstrip('/')}
                    self.all_links.update(urllinks)
                    link_queue.extend(urllinks)
                    self.visited_links.add(url)
                    links_scraped += 1

                except requests.exceptions.RequestException as e:
                    logger.error(f"Request exception for URL {url}: {e}")
                    continue

            if not self.all_links:
                self.all_links.add(base_url)

            standardized_links = set()
            for link in self.all_links:
                if link.startswith('http://'):
                    standardized_links.add('https://' + link[len('http://'):])
                else:
                    standardized_links.add(link)

            output_data['all_links'] = list(standardized_links)
            bring_data(output_data['all_links'], whitelist, blacklist)
            logger.info(f"Scraping completed. Found {len(output_data['all_links'])} links.")
            return output_data

        except Exception as e:
            logger.error(f"Error scraping {base_url}: {e}")
            return {"error": f"Error scraping {base_url}"}
