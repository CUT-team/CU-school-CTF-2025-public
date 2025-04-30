import hashlib
import io
import os
import re

import requests
from PIL import Image
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8000"
CHUNK_SIZE = 150
CHUNK_FOLDER = "solver_chunks"

os.makedirs(CHUNK_FOLDER, exist_ok=True)

session = requests.Session()
hash_dict = {}  # hash: animal_name


def hash_chunk(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return hashlib.sha256(buf.getvalue()).hexdigest()


def build_hash_dict():
    print("Парсим галерею...")
    resp = session.get(BASE_URL)
    soup = BeautifulSoup(resp.text, "html.parser")

    cards = soup.select(".animal-card")

    for card in cards:
        name = card.find("p").text.strip()
        img_url = card.find("img")["src"]
        img_full_url = BASE_URL + img_url if img_url.startswith("/") else BASE_URL + "/" + img_url
        img_full_url = img_full_url.replace("\\", '/')

        img_resp = session.get(img_full_url)
        img = Image.open(io.BytesIO(img_resp.content))
        w, h = img.size

        for x in range(w // CHUNK_SIZE):
            for y in range(h // CHUNK_SIZE):
                chunk = img.crop((
                    x * CHUNK_SIZE,
                    y * CHUNK_SIZE,
                    x * CHUNK_SIZE + CHUNK_SIZE,
                    y * CHUNK_SIZE + CHUNK_SIZE
                ))
                hsh = hash_chunk(chunk)
                hash_dict[hsh] = name.lower()


def solve_test():
    session.get(f"{BASE_URL}/test")

    correct = 0
    for i in range(1002):
        r = session.get(f"{BASE_URL}/test/play")
        if "Флаг" in r.text:
            soup = BeautifulSoup(r.text, "html.parser")
            flag_div = soup.find(string=re.compile(r"cuctf{.*}"))
            print(f"🏁 FLAG: {flag_div.strip()}")
        soup = BeautifulSoup(r.text, "html.parser")

        try:
            img_tag = soup.find("img")
            if not img_tag:
                break

            img_url = img_tag["src"]
            full_img_url = BASE_URL + img_url if img_url.startswith("/") else img_url
            img_resp = session.get(full_img_url)
            img = Image.open(io.BytesIO(img_resp.content))

            hsh = hash_chunk(img)
            guess = hash_dict.get(hsh, "")

            print(f"Попытка {i + 1}: '{guess}'")

            session.post(f"{BASE_URL}/test/play", data={"answer": guess})

            if guess:
                correct += 1

        except Exception as e:
            break

    print(f"Завершено: {correct}/100")


if __name__ == "__main__":
    build_hash_dict()
    solve_test()
