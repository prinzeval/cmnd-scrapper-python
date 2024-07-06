# from typing import List
# from scrapper.AllUrlsScrape import king_url
# import requests
# from bs4 import BeautifulSoup
# from models import ScrapedBaseUrl

# def process_url(url: str) -> Tuple[str, str, List[str]]:
#     response = requests.get(url)
#     if response.status_code == 200:
#         print(f"Successfully fetched the URL: {url}")
#     else:
#         print(f"Failed to fetch the URL: {url} with status code {response.status_code}")
#         return url, "No title found", []

#     soup = BeautifulSoup(response.content, 'html.parser')

#     for a in soup.find_all('a'):
#         a.decompose()

#     for unwanted in soup.find_all(['script', 'style', 'aside', 'footer', 'header', 'nav']):
#         unwanted.decompose()

#     for unwanted in soup.find_all(['div', 'section'], {'class': ['bw-wrapper']}):
#         unwanted.decompose()

#     for unwanted in soup.find_all('h2', string="Recommended articles"):
#         unwanted.decompose()

#     title_element = soup.find(lambda tag: tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title'])
#     title = title_element.text if title_element else "No title found"

#     body_text = soup.get_text()
#     body_text = body_text.replace("\n", " ").replace("\t", " ").replace("  ", " ")
#     body_text = body_text.strip()
#     body_text = body_text.split(". ")
#     body_text = ".\n".join(body_text)

#     image_links = [img['src'] for img in soup.find_all('img', src=True)]

#     return url, title, body_text, image_links

# def scrape_and_save():
#     result = []

#     my_set = set(king_url)
#     for url in my_set:
#         result.append(process_url(url))

#     with open("output.txt", "w", encoding="utf-8") as f:
#         for data in result:
#             f.write(f"URL: {data[0]}\n")
#             f.write(f"Title: {data[1]}\n")
#             f.write(f"Content:\n{data[2]}\n")
#             f.write("Image Links:\n")
#             for link in data[3]:
#                 f.write(f"{link}\n")
#             f.write("\n\n")

#     print("Data saved to output.txt")

# # Example usage:
# if __name__ == "__main__":
#     scrape_and_save()
