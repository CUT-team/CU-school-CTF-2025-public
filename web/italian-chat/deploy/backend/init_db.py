import uuid

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://mongo:27017"
DB_NAME = "ctf_db"


async def init():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    while True:
        try:
            await db.command("ping")
            break
        except Exception as e:
            pass

    # Очистим старые данные
    await db.users.delete_many({})
    await db.sessions.delete_many({})
    await db.chats.delete_many({})
    await db.messages.delete_many({})

    # Создаём пользователей
    await db.users.insert_many([
        {"username": "Bobrito Bondito", "password": "FHAFJKNFJANFJKANFNANJnjasnfdjdnakfnkfndafjkjfkanyqyiuiqd",
         "avatar_url": "https://i.imgur.com/RRgExlX.png"},
        {"username": "Crococroco Salami Bandino",
         "password": "FHAFJKNFJANFJKANFNANJnjasnfdjdnakfnkfndafjkjfkanyqyiuiqd",
         "avatar_url": "https://i.imgur.com/oRvG1iB.png"},
        {"username": "Kiwitto Banditto", "password": "FHAFJKNFJANFJKANFNANJnjasnfdjdnakfnkfndafjkjfkanyqyiuiqd",
         "avatar_url": "https://i.imgur.com/qqCjwIL.png"},
    ])

    # Создаём секретный чат
    secret_chat_id = str(uuid.uuid4())
    secret_chat = {
        "chat_id": secret_chat_id,
        "name": "Banditto Family",
        "owner": "Bobrito Bondito",
        "members": ["Bobrito Bondito", "Crococroco Salami Bandino", "Kiwitto Banditto"]
    }
    await db.chats.insert_one(secret_chat)

    # Сообщения в секретном чате
    await db.messages.insert_many([
        {"chat_id": secret_chat_id, "sender": "Bobrito Bondito",
         "text": "Я сегодня видел, как L'orso Patata катался на скейте... это было зрелище."},
        {"chat_id": secret_chat_id, "sender": "Crococroco Salami Bandino",
         "text": "Ха-ха, он снова отталкивался передней ногой? Легенда!"},
        {"chat_id": secret_chat_id, "sender": "Kiwitto Banditto",
         "text": "Поговаривают, что в его стиле скрыта какая-то древняя магия картошки..."},
        {"chat_id": secret_chat_id, "sender": "Bobrito Bondito", "text": "Или древняя магия позора. 😆"},
        {"chat_id": secret_chat_id, "sender": "Crococroco Salami Bandino",
         "text": "Я бы на его месте вообще снял шкурку и спрятался!"},
        {"chat_id": secret_chat_id, "sender": "Kiwitto Banditto",
         "text": "Лучше бы он отрастил себе вторую доску для баланса. 😂"},
        {"chat_id": secret_chat_id, "sender": "Bobrito Bondito",
         "text": "Между прочим, я слышал секрет о L'orso Patata..."},
        {"chat_id": secret_chat_id, "sender": "Bobrito Bondito", "text": "cuctf{patata_push3s_lik3_a_tru3_band1t0}"},
        {"chat_id": secret_chat_id, "sender": "Crococroco Salami Bandino",
         "text": "😱 Это надо срочно передать всем в Banditto Family!"},
        {"chat_id": secret_chat_id, "sender": "Kiwitto Banditto",
         "text": "Только тссс... иначе Patata узнает и заплачет в подушку из картошки."}
    ])

    print("[+] Инициализация базы данных завершена.")
    print(f"[+] Секретный чат создан. Chat ID: {secret_chat_id}")
