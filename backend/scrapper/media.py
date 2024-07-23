from urllib.parse import urljoin, urlparse

# List of unwanted URL prefixes
UNWANTED_PREFIXES = [
    'data:image/svg+xml;charset=utf8,'
]

def extract_media_links(page_source, base_url):
    media_links = []

    def is_valid_url(url):
        # Validate URL by checking if it starts with a valid scheme (http/https)
        parsed_url = urlparse(url)
        return parsed_url.scheme in ['http', 'https'] and parsed_url.netloc

    def is_unwanted_prefix(url):
        # Check if the URL starts with any unwanted prefix
        return any(url.startswith(prefix) for prefix in UNWANTED_PREFIXES)

    # Extract and filter images
    for img_tag in page_source.find_all('img', src=True):
        src = img_tag['src']
        if not is_unwanted_prefix(src) and is_valid_url(src):
            full_url = urljoin(base_url, src)
            media_links.append(full_url)

    # Extract and filter videos
    for video_tag in page_source.find_all('video', src=True):
        src = video_tag['src']
        if not is_unwanted_prefix(src) and is_valid_url(src):
            full_url = urljoin(base_url, src)
            media_links.append(full_url)

    # Extract and filter audio
    for audio_tag in page_source.find_all('audio', src=True):
        src = audio_tag['src']
        if not is_unwanted_prefix(src) and is_valid_url(src):
            full_url = urljoin(base_url, src)
            media_links.append(full_url)

    # Extract and filter PDFs
    for a_tag in page_source.find_all('a', href=True):
        href = a_tag['href']
        if href.lower().endswith('.pdf') and not is_unwanted_prefix(href) and is_valid_url(href):
            full_url = urljoin(base_url, href)
            media_links.append(full_url)

    # Remove duplicates
    media_links = list(set(media_links))

    return media_links
