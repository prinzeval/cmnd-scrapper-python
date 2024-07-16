import requests
from bs4 import BeautifulSoup
from typing import List
from datetime import datetime, timedelta
from database import get_supabase_client

# Define functions to check whitelist and blacklist
def is_in_whitelist(url, whitelist):
    if not whitelist:  # If whitelist is empty, consider it as passing all URLs
        return True
    for item in whitelist:
        if item in url:  # Check if whitelist item is a substring of the URL
            return True
    return False

def is_in_blacklist(url, blacklist):
    for item in blacklist:
        if item in url:  # Check if blacklist item is a substring of the URL
            return True
    return False

# Function to bring data from URLs and process them
def bring_data(needed_data: List[str], whitelist: List[str], blacklist: List[str]):
    print("All list extracted:", needed_data)

    # Get Supabase client
    supabase = get_supabase_client()

    try:
        for url in needed_data:
            # Check whitelist and blacklist
            if not is_in_whitelist(url, whitelist) or is_in_blacklist(url, blacklist):
                print(f"Skipping URL: {url} due to whitelist or blacklist settings.")
                continue

            # Check if the URL already exists in the database
            existing_data = supabase.table("scrapperDB").select("*").eq("url", url).execute()
            if existing_data.data:
                print(f"Data for URL: {url} already exists in the database.")
                continue

            # Perform the HTTP request
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Successfully fetched the URL: {url}")
            else:
                print(f"Failed to fetch the URL: {url} with status code {response.status_code}")
                continue

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove all <a> tags
            for a in soup.find_all('a'):
                a.decompose()

            # Remove ads and other unwanted elements
            for unwanted in soup.find_all(['script', 'style', 'aside', 'footer', 'header', 'nav']):
                unwanted.decompose()

            # Remove "Recommended articles" section
            for unwanted in soup.find_all(['div', 'section'], {'class': ['bw-wrapper']}):
                unwanted.decompose()

            for unwanted in soup.find_all('h2', string="Recommended articles"):
                unwanted.decompose()

            # Extract the title
            title_element = soup.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title'])
            title = title_element.text if title_element else "No title found"

            # Extract the body text and clean it up
            body_text = soup.get_text(separator=' ').strip()

            # Remove extra spaces and newlines
            body_text = ' '.join(body_text.split())

            # Split body text into sentences and join with new lines for better readability
            body_text = body_text.split('. ')
            body_text = '.\n'.join(body_text)

            # Extract image links
            image_links = [img['src'] for img in soup.find_all('img', src=True)]
            image_links_str = ', '.join(image_links)

            # Insert data into Supabase
            created_at = datetime.utcnow() - timedelta(hours=2)
            data = supabase.table("scrapperDB").insert({
                "created_at": str(created_at),
                "title": title,
                "content": body_text,
                "image_link": image_links_str,
                "url": url
            }).execute()

        print("Scraping completed and results saved to the database.")

    except Exception as e:
        print(f"Error while processing URLs: {e}")
