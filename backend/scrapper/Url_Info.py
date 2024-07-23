# import requests
# from bs4 import BeautifulSoup
# from typing import List
# from datetime import datetime, timedelta
# from database import get_supabase_client

# # Define functions to check whitelist and blacklist
# def is_in_whitelist(url, whitelist):
#     if not whitelist:  # If whitelist is empty, consider it as passing all URLs
#         return True
#     for item in whitelist:
#         if item in url:  # Check if whitelist item is a substring of the URL
#             return True
#     return False

# def is_in_blacklist(url, blacklist):
#     for item in blacklist:
#         if item in url:  # Check if blacklist item is a substring of the URL
#             return True
#     return False

# # Function to bring data from URLs and process them
# def bring_data(needed_data: List[str], whitelist: List[str], blacklist: List[str]):
#     print("All list extracted:", needed_data)

#     # Get Supabase client
#     supabase = get_supabase_client()

#     try:
#         for url in needed_data:
#             # Check whitelist and blacklist
#             if not is_in_whitelist(url, whitelist) or is_in_blacklist(url, blacklist):
#                 print(f"Skipping URL: {url} due to whitelist or blacklist settings.")
#                 continue

#             # Check if the URL already exists in the database
#             existing_data = supabase.table("scrapperDB").select("*").eq("url", url).execute()
#             if existing_data.data:
#                 print(f"Data for URL: {url} already exists in the database.")
#                 continue

#             # Perform the HTTP request
#             response = requests.get(url)
#             if response.status_code == 200:
#                 print(f"Successfully fetched the URL: {url}")
#             else:
#                 print(f"Failed to fetch the URL: {url} with status code {response.status_code}")
#                 continue

#             # Parse the HTML content using BeautifulSoup
#             soup = BeautifulSoup(response.content, 'html.parser')

#             # Remove all <a> tags
#             for a in soup.find_all('a'):
#                 a.decompose()

#             # Remove ads and other unwanted elements
#             for unwanted in soup.find_all(['script', 'style', 'aside', 'footer', 'header', 'nav']):
#                 unwanted.decompose()

#             # Remove "Recommended articles" section
#             for unwanted in soup.find_all(['div', 'section'], {'class': ['bw-wrapper']}):
#                 unwanted.decompose()

#             for unwanted in soup.find_all('h2', string="Recommended articles"):
#                 unwanted.decompose()

#             # Extract the title
#             title_element = soup.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title'])
#             title = title_element.text if title_element else "No title found"

#             # Extract the body text and clean it up
#             body_text = soup.get_text(separator=' ').strip()

#             # Remove extra spaces and newlines
#             body_text = ' '.join(body_text.split())

#             # Split body text into sentences and join with new lines for better readability
#             body_text = body_text.split('. ')
#             body_text = '.\n'.join(body_text)

#             # Extract image links
#             image_links = [img['src'] for img in soup.find_all('img', src=True)]
#             image_links_str = ', '.join(image_links)

#             # Insert data into Supabase
#             created_at = datetime.utcnow() - timedelta(hours=2)
#             data = supabase.table("scrapperDB").insert({
#                 "created_at": str(created_at),
#                 "title": title,
#                 "content": body_text,
#                 "image_link": image_links_str,
#                 "url": url
#             }).execute()

#         print("Scraping completed and results saved to the database.")

#     except Exception as e:
#         print(f"Error while processing URLs: {e}")












import random
import time
from datetime import datetime, timedelta
from typing import List

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from database import get_supabase_client
from scrapper.media import extract_media_links

def extract_media_links(page_source, base_url):
    """Extract media links from the page source."""
    media_links = []
    for img_tag in page_source.find_all('img'):
        src = img_tag.get('src')
        if src:
            media_links.append(requests.compat.urljoin(base_url, src))
    return media_links

def is_in_whitelist(url, whitelist):
    """Check if the URL is in the whitelist."""
    return any(item in url for item in whitelist) if whitelist else True

def is_in_blacklist(url, blacklist):
    """Check if the URL is in the blacklist."""
    return any(item in url for item in blacklist)

def fetch_with_selenium(url):
    """Fetch page content using Selenium."""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(random.randint(0, 1))  # Random sleep
    page_source = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return page_source

def bring_data(needed_data: List[str], whitelist: List[str], blacklist: List[str]):
    """Fetch data from URLs and save to the database."""
    print("All list extracted:", needed_data)
    supabase = get_supabase_client()

    try:
        for url in needed_data:
            if not is_in_whitelist(url, whitelist) or is_in_blacklist(url, blacklist):
                print(f"Skipping URL: {url} due to whitelist or blacklist settings.")
                continue

            existing_data = supabase.table("scrapperDB").select("*").eq("url", url).execute()
            if existing_data.data:
                print(f"Data for URL: {url} already exists in the database.")
                continue

            try:
                response = requests.get(url)
                response.raise_for_status()
                print(f"Successfully fetched the URL: {url}")
                page_source = BeautifulSoup(response.content, 'html.parser')
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                if response.status_code == 403:
                    print(f"Received 403 status code for {url}, switching to Selenium.")
                    page_source = fetch_with_selenium(url)
                else:
                    print(f"Failed to fetch the URL: {url} with status code {response.status_code}")
                    continue
            except requests.exceptions.RequestException as req_err:
                print(f"Request error occurred: {req_err}")
                continue

            # Remove unwanted elements
            for a in page_source.find_all('a'):
                a.decompose()
            for unwanted in page_source.find_all(['script', 'style', 'aside', 'footer', 'header', 'nav']):
                unwanted.decompose()
            for unwanted in page_source.find_all(['div', 'section'], {'class': ['bw-wrapper']}):
                unwanted.decompose()
            for unwanted in page_source.find_all('h2', string="Recommended articles"):
                unwanted.decompose()

            # Extract title
            title_element = page_source.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title'])
            title = title_element.text if title_element else "No title found"

            # Extract and format body text
            body_text = page_source.get_text(separator=' ').strip()
            body_text = ' '.join(body_text.split())
            body_text = body_text.split('. ')
            body_text = '.\n'.join(body_text)

            # Extract media links
            media_links = extract_media_links(page_source, url)
            print(f"Extracted media links: {media_links}")
            media_links_str = ', '.join(media_links)

            created_at = datetime.utcnow() - timedelta(hours=2)
            try:
                data = supabase.table("scrapperDB").insert({
                    "created_at": str(created_at),
                    "title": title,
                    "content": body_text,
                    "media_links": media_links_str,
                    "url": url
                }).execute()
                print(f"Data for URL: {url} inserted into the database.")
            except Exception as e:
                print(f"Error inserting data for URL: {url} into the database: {e}")

        print("Scraping completed and results saved to the database.")
    except Exception as e:
        print(f"Error while processing URLs: {e}")
