import random
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import re
from collections import deque
from typing import List
from .Url_Info import bring_data

# Global flag to stop the scraper
stop_scraping = False

class ScraperKING:
    def __init__(self):
        self.url_pattern = re.compile(
            r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)',
            re.IGNORECASE
        )
        self.image_extensions = re.compile(r'\.(jpg|jpeg|png|gif|webp)$', re.IGNORECASE)

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

    def scrape_website_links(self, base_url: str, whitelist: List[str], blacklist: List[str]):
        global stop_scraping
        all_links = set()
        visited_links = set()
        output_data = {}

        try:
            link_queue = deque([base_url])

            while link_queue:
                # Check the global stop_scraping flag
                if stop_scraping:
                    print("Stopping the scraping process as requested.")
                    break

                url = link_queue.popleft()
                print(f"Starting to scrape URL: {url}")

                if url in visited_links:
                    print(f"Skipping {url} as it has already been visited")
                    continue

                if not self.is_valid_url(url, base_url):
                    print(f"Skipping {url} as it is not a valid or allowed URL")
                    continue

                # Check if URL is in the whitelist
                if self.is_in_whitelist(url, whitelist):
                    print(f"URL {url} is in the whitelist, stopping further scraping.")
                    all_links.add(url)
                    break

                # Check if URL is in the blacklist
                if self.is_in_blacklist(url, blacklist):
                    print(f"URL {url} is in the blacklist, skipping it.")
                    continue

                response = requests.get(url)
                delay = random.randint(0, 1)
                time.sleep(delay)

                if response.status_code == 200:
                    page_source = BeautifulSoup(response.text, 'html.parser')

                    urllinks = {
                        urljoin(url, a['href']) for a in page_source.find_all('a', href=True)
                        if self.is_valid_url(urljoin(url, a['href']), base_url) and self.is_valid_link(a['href']) and not (
                                
                                '#' in a['href'] or
                                a['href'].startswith('mailto:') or
                                a['href'].startswith('javascript:void(0)')
                        )
                    }

                    urllinks = {link for link in urllinks if link.rstrip('/') != url.rstrip('/')}

                    print(f"Found links on {url}: {urllinks}")
                    all_links.update(urllinks)
                    link_queue.extend(urllinks)

                    visited_links.add(url)

                else:
                    print(f"Failed to fetch {url}, status code: {response.status_code}")

            standardized_links = set()
            for link in all_links:
                if link.startswith('http://'):
                    standardized_links.add('https://' + link[len('http://'):])
                else:
                    standardized_links.add(link)

            output_data['all_links'] = list(standardized_links)

            # Process the standardized links appropriately
            bring_data(output_data['all_links'], whitelist, blacklist)

            return output_data

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {base_url}: {e}")
            return {"error": f"Error fetching {base_url}"}

        except Exception as e:
            print(f"Error scraping {base_url}: {e}")
            return {"error": f"Error scraping {base_url}"}
