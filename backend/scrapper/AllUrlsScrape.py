import random
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import re
from collections import deque
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .Url_Info import bring_data

class ScraperKING:
    def __init__(self, link_limit=10000000):
        self.url_pattern = re.compile(
            r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)',
            re.IGNORECASE
        )
        self.image_extensions = re.compile(r'\.(jpg|jpeg|png|gif|webp)$', re.IGNORECASE)
        self.all_links = set()
        self.visited_links = set()
        self.link_limit = link_limit  # Set the link limit (default to 10)

    def is_valid_url(self, url, base_url):
        return self.url_pattern.match(url) is not None and url.startswith(base_url)

    def is_valid_link(self, url):
        return not bool(self.image_extensions.search(url))

    def is_in_whitelist(self, url, whitelist):
        if not whitelist:  # If whitelist is empty, consider it as passing all URLs
            return False
        for item in whitelist:
            if item in url:  # Check if whitelist item is a substring of the URL
                return True
        return False

    def is_in_blacklist(self, url, blacklist):
        for item in blacklist:
            if item in url:  # Check if blacklist item is a substring of the URL
                return True
        return False

    def fetch_with_selenium(self, url):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        delay = random.randint(0, 1)
        time.sleep(delay)
        page_source = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        return page_source

    def scrape_website_links(self, base_url: str, whitelist: List[str], blacklist: List[str]):
        output_data = {}

        try:
            if not (base_url.startswith('http://') or base_url.startswith('https://')):
                base_url = 'http://' + base_url  # Assuming http:// if no protocol is provided
                
            link_queue = deque([base_url])
            links_scraped = 0

            if self.is_in_whitelist(base_url, whitelist):
                # Directly process the base URL
                print(f"Base URL {base_url} is in the whitelist, processing it directly.")
                self.all_links.add(base_url)
                self.visited_links.add(base_url)
                # Process the base URL directly without collecting additional links
                try:
                    response = requests.get(base_url)
                    delay = random.randint(0, 1)
                    time.sleep(delay)

                    if response.status_code == 200:
                        page_source = BeautifulSoup(response.text, 'html.parser')
                    elif response.status_code == 403:
                        print(f"Received 403 status code for {base_url}, switching to Selenium.")
                        page_source = self.fetch_with_selenium(base_url)
                    else:
                        print(f"Failed to fetch {base_url}, status code: {response.status_code}")
                        return {"error": f"Failed to fetch {base_url}"}

                    # Process the base URL content here (e.g., extract data and save to DB)
                    bring_data([base_url], whitelist, blacklist)

                except requests.exceptions.RequestException as e:
                    print(f"Error fetching {base_url}: {e}")
                    return {"error": f"Error fetching {base_url}"}
                
                output_data['all_links'] = list(self.all_links)
                return output_data

            # Continue with regular scraping process
            while link_queue and links_scraped < self.link_limit:
                url = link_queue.popleft()
                print(f"Starting to scrape URL: {url}")

                if url in self.visited_links:
                    print(f"Skipping {url} as it has already been visited")
                    continue

                if not self.is_valid_url(url, base_url):
                    print(f"Skipping {url} as it is not a valid or allowed URL")
                    continue

                # Check if URL is in the whitelist
                if self.is_in_whitelist(url, whitelist):
                    print(f"URL {url} is in the whitelist, stopping further scraping.")
                    self.all_links.add(url)
                    break

                # Check if URL is in the blacklist
                if self.is_in_blacklist(url, blacklist):
                    print(f"URL {url} is in the blacklist, skipping it.")
                    continue

                try:
                    response = requests.get(url)
                    delay = random.randint(0, 1)
                    time.sleep(delay)

                    if response.status_code == 200:
                        page_source = BeautifulSoup(response.text, 'html.parser')
                    elif response.status_code == 403:
                        print(f"Received 403 status code for {url}, switching to Selenium.")
                        page_source = self.fetch_with_selenium(url)
                    else:
                        print(f"Failed to fetch {url}, status code: {response.status_code}")
                        continue

                    urllinks = {
                        urljoin(url, a['href']) for a in page_source.find_all('a', href=True)
                        if self.is_valid_url(urljoin(url, a['href']), base_url) and self.is_valid_link(a['href']) and not (
                                a['href'].startswith('https') or
                                '#' in a['href'] or
                                a['href'].startswith('mailto:') or
                                a['href'].startswith('javascript:void(0)')
                        )
                    }

                    urllinks = {link for link in urllinks if link.rstrip('/') != url.rstrip('/')}
                    print(f"Found links on {url}: {urllinks}")

                    self.all_links.update(urllinks)
                    link_queue.extend(urllinks)
                    self.visited_links.add(url)
                    links_scraped += 1

                except requests.exceptions.RequestException as e:
                    print(f"Error fetching {url}: {e}")
                    continue

            # Ensure the base URL is included in the list if no other links were found
            if not self.all_links:
                self.all_links.add(base_url)

            standardized_links = set()
            for link in self.all_links:
                if link.startswith('http://'):
                    standardized_links.add('https://' + link[len('http://'):])
                else:
                    standardized_links.add(link)

            output_data['all_links'] = list(standardized_links)

            # Process the standardized links appropriately
            bring_data(output_data['all_links'], whitelist, blacklist)

            return output_data

        except Exception as e:
            print(f"Error scraping {base_url}: {e}")
            return {"error": f"Error scraping {base_url}"}
