import json
import os
import random
import time
import uuid

from PIL import Image
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    Response,
    send_from_directory,
)

# ==== КОНСТАНТЫ ====
FLAG = "cuctf{brainrot_z00mer_god}"
CHUNK_SIZE = 150
MAX_TRIES = 1000
CHUNK_LIFETIME = 60
CHUNK_FOLDER = "./static/chunks"
SESSION_FOLDER = "./sessions"
SESSION_LIFETIME = 1800
CLEANUP_INTERVAL = 60
last_session_cleanup = 0
os.makedirs(SESSION_FOLDER, exist_ok=True)

# ==== НАСТРОЙКА ====
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0  # отключаем кэширование статики

with open("italian_animals.json", encoding="utf-8") as f:
    animal_data = json.load(f)

os.makedirs(CHUNK_FOLDER, exist_ok=True)


# ==== СЕССИИ В ПАМЯТИ ====
def load_session(session_id: str):
    session_path = os.path.join(SESSION_FOLDER, f"{session_id}.json")
    if os.path.exists(session_path):
        with open(session_path, "r") as f:
            return json.load(f)
    return None


def save_session(session_id: str, session_data: dict):
    session_path = os.path.join(SESSION_FOLDER, f"{session_id}.json")
    with open(session_path, "w") as f:
        json.dump(session_data, f)


# ==== ХЕЛПЕРЫ ====


def clean_old_chunks():
    current_time = time.time()
    for filename in os.listdir(CHUNK_FOLDER):
        file_path = os.path.join(CHUNK_FOLDER, filename)
        if os.path.isfile(file_path):
            file_creation_time = os.path.getctime(file_path)
            if current_time - file_creation_time > CHUNK_LIFETIME:
                os.remove(file_path)


def clean_old_sessions():
    current_time = time.time()
    for filename in os.listdir(SESSION_FOLDER):
        file_path = os.path.join(SESSION_FOLDER, filename)
        if not filename.endswith(".json"):
            continue
        if os.path.isfile(file_path):
            file_creation_time = os.path.getctime(file_path)
            if current_time - file_creation_time > SESSION_LIFETIME:
                os.remove(file_path)


def crop_random_chunk(image_path: str, session_id: str, try_index: int):
    image = Image.open(image_path)
    width, height = image.size

    chunks_x = width // CHUNK_SIZE
    chunks_y = height // CHUNK_SIZE

    if chunks_x == 0 or chunks_y == 0:
        raise ValueError("Картинка слишком маленькая для чанков")

    chunk_x = random.randint(0, chunks_x - 1)
    chunk_y = random.randint(0, chunks_y - 1)

    left = chunk_x * CHUNK_SIZE
    top = chunk_y * CHUNK_SIZE
    right = left + CHUNK_SIZE
    bottom = top + CHUNK_SIZE
    chunk = image.crop((left, top, right, bottom))

    chunk_filename = f"chunk_{session_id}_{try_index}.png"
    chunk_path = os.path.join(CHUNK_FOLDER, chunk_filename)
    chunk.save(chunk_path)

    return f"/static/chunks/{chunk_filename}"


def create_new_round(session_id: str, session: dict):
    animal_name, image_path = random.choice(list(animal_data.items()))
    try_index = session["current_try"]
    img_url = crop_random_chunk(image_path, session_id, try_index)

    session["current_animal"] = animal_name.lower()
    session["current_image"] = image_path
    session["current_img_url"] = img_url


# ==== МАРШРУТЫ ====


@app.before_request
def before_request():
    global last_session_cleanup
    now = time.time()

    if now - last_session_cleanup > CLEANUP_INTERVAL:
        clean_old_chunks()
        clean_old_sessions()
        last_session_cleanup = now


@app.route("/")
def gallery():
    return render_template("gallery.html", animals=animal_data)


@app.route("/test")
def start_test():
    session_id = str(uuid.uuid4())
    session_data = {
        "current_try": 0,
        "score": 0,
    }
    save_session(session_id, session_data)
    resp = redirect(url_for("test_round"))
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/test/play")
def test_round():
    session_id = request.cookies.get("session_id")
    session = load_session(session_id)
    if not session:
        return redirect(url_for("start_test"))

    if session["current_try"] >= MAX_TRIES:
        show_flag = session["score"] == MAX_TRIES
        return render_template(
            "test_result.html",
            score=session["score"],
            show_flag=show_flag,
            flag=FLAG if show_flag else "",
        )

    create_new_round(session_id, session)
    save_session(session_id, session)

    return render_template(
        "test_play.html",
        img_src=session["current_img_url"],
        current_try=session["current_try"] + 1,
        max_tries=MAX_TRIES,
    )


@app.route("/test/play", methods=["POST"])
def handle_answer():
    session_id = request.cookies.get("session_id")
    session = load_session(session_id)
    if not session:
        return redirect(url_for("start_test"))

    session["current_try"] += 1

    answer = request.form.get("answer", "").strip().lower()
    if answer == session["current_animal"]:
        session["score"] += 1

    save_session(session_id, session)

    return redirect(url_for("test_round"))


@app.route("/static/chunks/<path:filename>")
def serve_chunk(filename):
    return send_from_directory(CHUNK_FOLDER, filename)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)
