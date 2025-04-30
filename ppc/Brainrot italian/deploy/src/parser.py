import os
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

base_url = "https://brainrot.fandom.com"
page_url = f"{base_url}/wiki/AI_Brainrot_animals"
output_dir = "static/italian_animals"

os.makedirs(output_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

# получаем список ссылок на итальянских животных
response = requests.get(page_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
italian_header = soup.find("span", id="Italian")
ul = italian_header.find_parent("h3").find_next_sibling("ul")

animal_links = []
for a in ul.find_all("a", href=True):
    href = a["href"]
    if href.startswith("/wiki/"):
        full_url = urljoin(base_url, href)
        animal_links.append((a.get_text(strip=True), full_url))  # имя + ссылка

# качаем все картинки с каждой страницы
for animal_name, link in animal_links:
    res = requests.get(link, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    img_tags = soup.find_all("img")

    for idx, img in enumerate(img_tags):
        src = img.get("src")
        if src and "static.wikia.nocookie.net" in src:
            img_url = src.split("/revision")[0]
            ext = os.path.splitext(urlparse(img_url).path)[-1] or ".png"
            img_name = f"{animal_name.replace(' ', '_')}_{idx}{ext}"
            img_data = requests.get(img_url, headers=headers).content
            with open(os.path.join(output_dir, img_name), "wb") as f:
                f.write(img_data)
            print(f"Скачано: {img_name}")
