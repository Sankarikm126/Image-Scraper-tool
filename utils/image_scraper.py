import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

def extract_child_links(base_url):
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            href = urljoin(base_url, a['href'])
            if urlparse(href).netloc == urlparse(base_url).netloc:
                links.add(href)
        return list(links)
    except Exception:
        return []

def scrape_images_from_site(base_url, save_dir):
    pages = [base_url] + extract_child_links(base_url)
    os.makedirs(save_dir, exist_ok=True)
    data = []

    for page_url in pages:
        try:
            response = requests.get(page_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            for img in soup.find_all('img'):
                src = img.get('src')
                if not src: continue
                image_url = urljoin(page_url, src)
                image_name = os.path.basename(urlparse(image_url).path)
                alt_text = img.get('alt', '')
                local_path = os.path.join(save_dir, image_name)
                try:
                    img_data = requests.get(image_url, timeout=10).content
                    with open(local_path, 'wb') as f:
                        f.write(img_data)
                    data.append({
                        'page_url': page_url,
                        'image_url': image_url,
                        'image_name': image_name,
                        'alt_text': alt_text,
                        'local_path': local_path
                    })
                except Exception:
                    continue
        except Exception:
            continue

    return data
