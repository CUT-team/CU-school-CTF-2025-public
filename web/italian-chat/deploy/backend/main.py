import asyncio
import secrets
import uuid
import os
from typing import Any

from fastapi import Cookie, Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from init_db import init

app = FastAPI()
client = AsyncIOMotorClient("mongodb://mongo:27017")
db = client.ctf_db

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get('PUBLIC_URL')],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginModel(BaseModel):
    username: str
    password: str

class RegisterModel(BaseModel):
    username: str
    password: str
    avatar_url: str


class CreateChatModel(BaseModel):
    name: str


class InviteModel(BaseModel):
    chat_id: str
    username: str


class SendMessageModel(BaseModel):
    chat_id: str
    text: str


class SearchModel(BaseModel):
    chat_id: Any
    keyword: str = ""


async def get_current_user(session_id: str = Cookie(None)):
    if not session_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    session = await db.sessions.find_one({"session_id": session_id})
    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = await db.users.find_one({"username": session["username"]})
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user


@app.post("/api/register")
async def register(data: RegisterModel, response: Response):
    if await db.users.find_one({"username": data.username}):
        raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует")
    await db.users.insert_one({"username": data.username, "password": data.password, "avatar_url": data.avatar_url})
    
    session_id = str(uuid.uuid4())
    await db.sessions.insert_one({"session_id": session_id, "username": data.username})

    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return {"message": "Registered"}


@app.post("/api/login")
async def login(data: LoginModel, response: Response):
    user = await db.users.find_one({"username": data.username})
    if not user or not secrets.compare_digest(user["password"], data.password):
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")

    session_id = str(uuid.uuid4())
    await db.sessions.insert_one({"session_id": session_id, "username": user["username"]})

    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return {"message": "Logged in"}


@app.post("/api/logout")
async def logout(response: Response, session_id: str = Cookie(None)):
    if session_id:
        await db.sessions.delete_one({"session_id": session_id})

    response.delete_cookie("session_id")
    return {"message": "Logged out"}


@app.get('/api/avatar/{username}')
async def avatar(username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return {"avatar_url": user["avatar_url"]}


@app.post("/api/create_chat")
async def create_chat(data: CreateChatModel, user: dict = Depends(get_current_user)):
    chat_id = str(uuid.uuid4())
    chat = {"chat_id": chat_id, "name": data.name, "owner": user["username"], "members": [user["username"]]}
    await db.chats.insert_one(chat)
    return {"chat_id": chat_id}


@app.post("/api/invite")
async def invite(data: InviteModel, user: dict = Depends(get_current_user)):
    chat = await db.chats.find_one({"chat_id": data.chat_id})
    if not chat or chat["owner"] != user["username"]:
        raise HTTPException(status_code=403, detail="Not your chat")

    invited_user = await db.users.find_one({"username": data.username})
    if not invited_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    await db.chats.update_one({"chat_id": data.chat_id}, {"$addToSet": {"members": data.username}})
    return {"message": "User invited"}


@app.post("/api/send_message")
async def send_message(data: SendMessageModel, user: dict = Depends(get_current_user)):
    chat = await db.chats.find_one({"chat_id": data.chat_id})
    if not chat or user["username"] not in chat["members"]:
        raise HTTPException(status_code=403, detail="Access denied")
    await db.messages.insert_one({"chat_id": data.chat_id, "sender": user["username"], "text": data.text})
    return {"message": "Message sent"}


@app.post("/api/search_messages")
async def search_messages(data: SearchModel, user: dict = Depends(get_current_user)):
    chat_id = data.chat_id
    keyword = data.keyword

    if isinstance(chat_id, str):
        chat = await db.chats.find_one({"chat_id": chat_id})
        if not chat or user["username"] not in chat["members"]:
            raise HTTPException(status_code=403, detail="Access denied")

    query = {
        "chat_id": chat_id,
        "text": {"$regex": keyword}
    }
    try:
        messages = await db.messages.find(query, {"_id": 0}).to_list(length=1000)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return messages


@app.get("/api/chats")
async def get_chats(user: dict = Depends(get_current_user)):
    all_chats = await db.chats.find({}, {"chat_id": 1, "name": 1, "members": 1, "owner": 1}).to_list(length=1000)
    result = []

    for chat in all_chats:
        is_member = user["username"] in chat.get("members", [])
        result.append({
            "chat_id": chat["chat_id"],
            "name": chat["name"],
            "owner": chat["owner"],
            "forbidden": not is_member
        })

    return result

@app.get("/api/profile")
async def profile(user: dict = Depends(get_current_user)):
    return {
        "username": user["username"],
        "avatar_url": user.get("avatar_url", "")
    }


@app.get("/api/messages/{chat_id}")
async def get_chat_messages(chat_id: str, user: dict = Depends(get_current_user)):
    chat = await db.chats.find_one({"chat_id": chat_id})
    if not chat or user["username"] not in chat["members"]:
        raise HTTPException(status_code=403, detail="Access denied")

    messages = await db.messages.find({"chat_id": chat_id}, {"_id": 0}).to_list(length=1000)
    return messages


if __name__ == '__main__':
    import uvicorn

    asyncio.run(init())
    uvicorn.run('main:app', host="0.0.0.0", port=1335, workers=4)
