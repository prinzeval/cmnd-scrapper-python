# import requests
# from bs4 import BeautifulSoup
# import re
# from urllib.parse import urljoin

# class Scraper:
#     def __init__(self):
#         self.expression = re.compile(
#             r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&\/\/=]*)',
#             re.IGNORECASE
#         )

#     def is_valid_url(self, url):
#         return self.expression.match(url) is not None

#     def scrape(self, url):
#         print(f"Starting to scrape the base URL: {url}")
        
#         if not (url.startswith('http://') or url.startswith('https://')):
#             url = 'http://' + url  # Assuming http:// if no protocol is provided
        
#         try:
#             if not self.is_valid_url(url):
#                 raise ValueError(f"{url} is an invalid URL format")

#             response = requests.get(url)
#             response.raise_for_status()  # Raise HTTP error for 4xx or 5xx status

#             html_content = BeautifulSoup(response.content, 'html.parser')

#             # Extract links, filtering out those containing 'https', '#', or the main URL itself
#             urllinks = {
#                 urljoin(url, a['href']) for a in html_content.find_all('a', href=True)
#                 if not (a['href'].startswith('https') or '#' in a['href']or a['href'].startswith('mailto:')or a['href'].startswith('javascript:void(0)')) 
#             }

#             # Filter out the main URL itself from the links
#             urllinks = {link for link in urllinks if link.rstrip('/') != url.rstrip('/')}
            
#             print(f"Found links: {urllinks}")
#             return list(urllinks)

#         except requests.RequestException as e:
#             raise ValueError(f"Error fetching the URL: {e}")
