import json
import os
import re

image_dir = "static/italian_animals"
output_json = "italian_animals.json"
animal_dict = {}

for filename in os.listdir(image_dir):
    if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        continue

    name_raw = os.path.splitext(filename)[0]
    name_clean = re.sub(r"_\d+$", "", name_raw)  # убираем индекс
    name_clean = name_clean.replace("_", " ")  # заменяем подчёркивания на пробел
    animal_dict[name_clean] = os.path.join(os.path.join('static', image_dir), filename)

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(animal_dict, f, ensure_ascii=False, indent=2)

print(f"Словарь сохранён в {output_json}")
