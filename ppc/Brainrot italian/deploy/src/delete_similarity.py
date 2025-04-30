import hashlib
import os

image_dir = "static/italian_animals"
hashes = {}
deleted = 0

for filename in os.listdir(image_dir):
    filepath = os.path.join(image_dir, filename)

    if not os.path.isfile(filepath):
        continue

    with open(filepath, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    if file_hash in hashes:
        os.remove(filepath)
        deleted += 1
        print(f"Удалено повторяющееся: {filename}")
    else:
        hashes[file_hash] = filename

print(f"Готово. Удалено {deleted} дубликатов.")
