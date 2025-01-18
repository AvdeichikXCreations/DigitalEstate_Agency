# Project Structure
```
/Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app
├── app.py
├── controllers
│   ├── __init__.py
│   ├── admin_controller.py
│   ├── db_controller.py
│   ├── telegram_controller.py
│   ├── tester_controller.py
│   ├── umnico_controller.py
│   └── widget_controller.py
├── core
│   ├── llm
│   │   ├── azure_llm.py
│   │   ├── base_llm.py
│   │   ├── google_llm.py
│   │   └── openai_llm.py
│   ├── llm_controller.py
│   └── llm_manager.py
├── handlers
│   ├── __init__.py
│   ├── audio_handler.py
│   ├── photo_handler.py
│   ├── text_handler.py
│   └── video_handler.py
├── rag
│   └── rag_service.py
└── requirements.txt

6 directories, 21 files
```

# Source Code

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/core/llm/openai_llm.py
```python
# core/llm/openai_llm.py

from .base_llm import BaseLLM

class OpenAILLM(BaseLLM):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "FAKE_OPENAI_KEY"

    def generate(self, prompt: str) -> str:
        # Заглушка — просто возвращаем строку, имитируя, что обратились к OpenAI
        return f"[OpenAI-Stub] Вот ответ на ваш промпт: '{prompt}'"```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/core/llm/google_llm.py
```python
# core/llm/google_llm.py

from .base_llm import BaseLLM

class GoogleLLM(BaseLLM):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "FAKE_GOOGLE_KEY"

    def generate(self, prompt: str) -> str:
        return f"[Google-Stub] Ответ (генерация) на промпт: '{prompt}'"```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/core/llm/azure_llm.py
```python
# core/llm/azure_llm.py

from .base_llm import BaseLLM

class AzureLLM(BaseLLM):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "FAKE_AZURE_KEY"

    def generate(self, prompt: str) -> str:
        return f"[Azure-Stub] Ответ (генерация) на промпт: '{prompt}'"```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/core/llm/base_llm.py
```python
# core/llm/base_llm.py

from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Заглушка: сгенерировать ответ на переданный prompt.
        """
        pass```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/core/llm_controller.py
```python
# core/llm_controller.py

from .llm_manager import LLMManager

def generate_response_for_text(user_message: str) -> str:
    """
    Демонстрация: текст → используем 'text' -> OpenAI
    """
    llm = LLMManager.get_llm_for_task("text")
    prompt = f"User says: {user_message}. Provide a helpful text answer."
    return llm.generate(prompt)

def generate_response_for_image(description: str) -> str:
    """
    Демонстрация: фото → используем 'image' -> Azure
    description — это описание фото, если мы его как-то получили
    """
    llm = LLMManager.get_llm_for_task("image")
    prompt = f"User sent an image with description: {description}."
    return llm.generate(prompt)

def generate_response_for_video(description: str) -> str:
    """
    Пусть тоже пользуемся 'image' (или openai) — на ваш выбор.
    Здесь только заглушка
    """
    llm = LLMManager.get_llm_for_task("image")  # или "text"
    prompt = f"User sent a video. Additional info: {description}."
    return llm.generate(prompt)

def generate_response_for_audio(text_from_audio: str) -> str:
    """
    Голос → используем 'audio' -> Google LLM
    text_from_audio — предполагаем, что вы как-то уже распознали речь
    """
    llm = LLMManager.get_llm_for_task("audio")
    prompt = f"Transcribed user voice: '{text_from_audio}'. Please respond."
    return llm.generate(prompt)```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/core/llm_manager.py
```python
# core/llm_manager.py

import os
from .llm.openai_llm import OpenAILLM
from .llm.azure_llm import AzureLLM
from .llm.google_llm import GoogleLLM

class LLMManager:
    _llms = {}

    @classmethod
    def init_all_llms(cls):
        """
        Инициализирует все наши LLM (заглушки).
        В реальном проекте здесь можно читать .env, config и т.д.
        """
        cls._llms["openai"] = OpenAILLM(api_key=os.getenv("OPENAI_API_KEY"))
        cls._llms["azure"] = AzureLLM(api_key=os.getenv("AZURE_API_KEY"))
        cls._llms["google"] = GoogleLLM(api_key=os.getenv("GOOGLE_API_KEY"))

    @classmethod
    def get_llm_for_task(cls, task_type: str):
        """
        Возвращаем LLM-объект для нужного типа задачи.
        В нашем демо:
          - 'text' обрабатываем OpenAI
          - 'image' обрабатываем Azure
          - 'audio' обрабатываем Google
          - при других типах - default OpenAI
        """
        if not cls._llms:
            cls.init_all_llms()

        if task_type == "text":
            return cls._llms["openai"]
        elif task_type == "image":
            return cls._llms["azure"]
        elif task_type == "audio":
            return cls._llms["google"]
        else:
            return cls._llms["openai"]  # fallback```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/rag/rag_service.py
```python
```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/app.py
```python


# app.py
# app.py
import os
from quart import Quart
from dotenv import load_dotenv

load_dotenv()

# Импортируем наши Blueprint'ы
from controllers.telegram_controller import telegram_bp
from controllers.umnico_controller import umnico_bp
from controllers.widget_controller import widget_bp
from controllers.admin_controller import admin_bp
from controllers.db_controller import db_bp
from controllers.tester_controller import tester_bp

# Инициализируем LLM Manager
from core.llm_manager import LLMManager

def create_app():
    app = Quart(__name__)

    # Инициализируем все LLM (заглушки)
    LLMManager.init_all_llms()

    # Регистрируем blueprints
    app.register_blueprint(telegram_bp, url_prefix="/api/v1/telegram")
    app.register_blueprint(umnico_bp, url_prefix="/api/v1/umnico")
    app.register_blueprint(widget_bp, url_prefix="/api/v1/widget")
    app.register_blueprint(admin_bp, url_prefix="/api/v1/admin")
    app.register_blueprint(db_bp, url_prefix="/api/v1/db/mongodb")
    app.register_blueprint(tester_bp, url_prefix="/api/v1/tester")

    return app

if __name__ == "__main__":
    quart_app = create_app()
    quart_app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8010)))```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/controllers/db_controller.py
```python


# controllers/db_controller.py

from quart import Blueprint, request, jsonify
import os
from pymongo import MongoClient

db_bp = Blueprint("db_bp", __name__)

# Предположим, строку подключения берём из переменных окружения
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
mongo_db = client["my_chatbot_db"]  # имя БД
collection = mongo_db["history"]    # коллекция для хранения истории

@db_bp.route("/history", methods=["GET"])
async def get_history():
    """
    GET /api/v1/db/mongodb/history
    Возвращает все записи (ограничение не внедряем, это лишь демо).
    """
    docs = list(collection.find({}))  # Это будет список dict
    # Преобразуем _id в строку, так как ObjectId не сериализуется напрямую
    for doc in docs:
        doc["_id"] = str(doc["_id"])
    return jsonify(docs), 200

@db_bp.route("/history", methods=["POST"])
async def add_history():
    """
    POST /api/v1/db/mongodb/history
    Тело запроса: {"user": "...", "message": "...", ...}
    Добавляет новую запись в MongoDB.
    """
    data = await request.get_json()
    result = collection.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

@db_bp.route("/history/<doc_id>", methods=["PUT"])
async def update_history(doc_id):
    """
    PUT /api/v1/db/mongodb/history/<doc_id>
    Обновляет запись по ID
    """
    data = await request.get_json()
    from bson.objectid import ObjectId
    result = collection.update_one({"_id": ObjectId(doc_id)}, {"$set": data})
    return jsonify({"matched_count": result.matched_count, "modified_count": result.modified_count}), 200

@db_bp.route("/history/<doc_id>", methods=["DELETE"])
async def delete_history(doc_id):
    """
    DELETE /api/v1/db/mongodb/history/<doc_id>
    Удаляет запись по ID.
    """
    from bson.objectid import ObjectId
    result = collection.delete_one({"_id": ObjectId(doc_id)})
    return jsonify({"deleted_count": result.deleted_count}), 200```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/controllers/widget_controller.py
```python


# controllers/widget_controller.py

from quart import Blueprint, request, jsonify

widget_bp = Blueprint("widget_bp", __name__)

@widget_bp.route("/webhook", methods=["POST"])
async def widget_webhook():
    """
    Приём запросов из виджета на сайте.
    Например, user_message = data["message"], далее - LLM/RAG.
    """
    data = await request.get_json()
    return jsonify({"status": "ok", "source": "widget", "data": data}), 200```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/controllers/admin_controller.py
```python


# controllers/admin_controller.py

from quart import Blueprint, jsonify
admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/health", methods=["GET"])
async def health_check():
    """
    Пример проверки состояния приложения.
    """
    return jsonify({"status": "ok"}), 200

@admin_bp.route("/monitor", methods=["GET"])
async def monitor_info():
    """
    Возвращаем какую-то служебную информацию: кол-во запросов, uptime и т.д.
    """
    # Заглушка
    return jsonify({"requests_count": 123, "uptime": "1h:05m"}), 200

@admin_bp.route("/config", methods=["GET", "POST"])
async def bot_config():
    """
    GET - получить конфиг,
    POST - изменить конфиг (system prompt, temperature и т.д.)
    """
    # Заглушка
    if (await admin_bp.request).method == "GET":
        return jsonify({"system_prompt": "You are a helpful bot...", "temperature": 0.7})
    else:
        data = await admin_bp.request.get_json()
        # Применить новые настройки...
        return jsonify({"status": "updated", "new_config": data}), 200```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/controllers/__init__.py
```python
```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/controllers/telegram_controller.py
```python

# controllers/telegram_controller.py

# controllers/telegram_controller.py

import os
import requests
from quart import Blueprint, request, jsonify
from handlers import get_response_for_message

telegram_bp = Blueprint("telegram_bp", __name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@telegram_bp.route("/webhook", methods=["POST"])
async def telegram_webhook():
    data = await request.get_json()
    if not data:
        return jsonify({"ok": False, "description": "No data received"}), 400
    
    message = data.get("message", {})
    if not message:
        return jsonify({"ok": False, "description": "No message in update"}), 200
    
    chat_id = message.get("chat", {}).get("id")
    if not chat_id:
        return jsonify({"ok": False, "description": "No chat_id found"}), 200

    # Вместо build_response_for_message - зовём наш диспетчер:
    user_reply = get_response_for_message(message)

    if user_reply:
        send_telegram_message(chat_id, user_reply)
    
    return jsonify({"ok": True, "description": "Message processed"}), 200

def send_telegram_message(chat_id: int, text: str):
    if not BOT_TOKEN:
        print("BOT_TOKEN is not set! Can't send message.")
        return
    
    url = f"{BASE_TELEGRAM_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Failed to send message:", response.text)```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/controllers/umnico_controller.py
```python


# controllers/umnico_controller.py

from quart import Blueprint, request, jsonify

umnico_bp = Blueprint("umnico_bp", __name__)

@umnico_bp.route("/webhook", methods=["POST"])
async def umnico_webhook():
    """
    Эндпоинт для приёма сообщений от платформы Umnico.
    Аналогичная логика: достаём данные, обрабатываем, отвечаем.
    """
    data = await request.get_json()
    # ...вызовы RAG, генерация ответа...
    return jsonify({"status": "ok", "source": "umnico", "data": data}), 200```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/controllers/tester_controller.py
```python


# controllers/tester_controller.py

from quart import Blueprint, request, jsonify

tester_bp = Blueprint("tester_bp", __name__)

@tester_bp.route("/history", methods=["GET"])
async def tester_history():
    """
    Отдаёт историю переписки бота (например, агрегированную).
    Можно переиспользовать логику из db_controller
    или объединить всё в одном месте.
    """
    # Заглушка: вернём список фиктивных сообщений
    return jsonify([
        {"user": "Alice", "message": "Hi", "bot_reply": "Hello!"},
        {"user": "Bob", "message": "Price?", "bot_reply": "Our services..."}
    ]), 200

@tester_bp.route("/rag-pairs", methods=["GET", "POST", "PUT", "DELETE"])
async def rag_pairs():
    """
    Работа с Q&A или RAG-парами.
    - GET: получить список
    - POST: добавить новую пару
    - PUT: обновить
    - DELETE: удалить
    """
    if request.method == "GET":
        # Возвращаем имеющиеся пары (заглушка)
        return jsonify({"pairs": [{"q": "Price?", "a": "20% cheaper..."}]})
    elif request.method == "POST":
        data = await request.get_json()
        # Добавить пару в векторную БД или Mongo
        return jsonify({"status": "added", "data": data}), 201
    # ... и т.д. для PUT, DELETE
    return jsonify({"error": "Method not implemented"}), 501


@tester_bp.route("/tokens-usage", methods=["GET"])
async def tokens_usage():
    """
    Пример анализа расхода токенов (если собираете статистику).
    """
    # Заглушка
    return jsonify({"tokens_used": 1234, "model": "gpt-3.5-turbo"}), 200

@tester_bp.route("/system-prompt", methods=["GET", "POST"])
async def system_prompt():
    """
    GET: посмотреть текущий system prompt
    POST: изменить system prompt для бота
    """
    if request.method == "GET":
        return jsonify({"system_prompt": "You are a helpful assistant."}), 200
    else:
        data = await request.get_json()
        new_prompt = data.get("system_prompt", "")
        # Применить изменения...
        return jsonify({"status": "updated", "new_prompt": new_prompt}), 200```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/handlers/photo_handler.py
```python
# handlers/photo_handler.py

# handlers/photo_handler.py

from core.llm_controller import generate_response_for_image

def handle_photo(message: dict) -> str:
    """
    Обработка фото. Допустим, мы не скачиваем картинку,
    а просто берём caption как 'description'.
    """
    caption = message.get("caption")
    description = caption or "No description"
    
    llm_answer = generate_response_for_image(description)
    return f"[PHOTO HANDLER] LLM says: {llm_answer}"```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/handlers/video_handler.py
```python
# handlers/video_handler.py

# handlers/video_handler.py

from core.llm_controller import generate_response_for_video

def handle_video(message: dict) -> str:
    """
    Аналогичный stub для видео.
    """
    caption = message.get("caption")
    description = caption or "No description"
    
    llm_answer = generate_response_for_video(description)
    return f"[VIDEO HANDLER] LLM says: {llm_answer}"```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/handlers/__init__.py
```python
# handlers/__init__.py

# handlers/__init__.py

from .text_handler import handle_text
from .photo_handler import handle_photo
from .video_handler import handle_video
from .audio_handler import handle_audio

def get_response_for_message(message: dict) -> str:
    text = message.get("text")
    photos = message.get("photo")
    video = message.get("video")
    audio = message.get("audio")
    voice = message.get("voice")
    caption = message.get("caption")

    if text:
        return handle_text(message)
    elif photos:
        return handle_photo(message)
    elif video:
        return handle_video(message)
    elif audio or voice:
        return handle_audio(message)
    else:
        return "[DISPATCHER] Unknown type of message"```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/handlers/audio_handler.py
```python
# handlers/audio_handler.py

# handlers/audio_handler.py

from core.llm_controller import generate_response_for_audio

def handle_audio(message: dict) -> str:
    """
    Допустим, у нас есть audio/voice.
    Мы не делаем реальное распознавание,
    а просто берём caption или "Audio file" как 'text_from_audio'.
    """
    caption = message.get("caption")
    transcribed_text = caption or "Voice or audio with no text"
    
    llm_answer = generate_response_for_audio(transcribed_text)
    return f"[AUDIO HANDLER] LLM says: {llm_answer}"```

## /Users/sergejavdejcik/Library/Mobile Documents/com~apple~CloudDocs/code_2/rag_monitoring_app/rag_monitoring_app/my_quart_app/handlers/text_handler.py
```python
# handlers/text_handler.py

# handlers/text_handler.py

from core.llm_controller import generate_response_for_text

def handle_text(message: dict) -> str:
    """
    Получаем текст, вызываем LLM (OpenAI stub).
    """
    user_text = message.get("text", "")
    
    # Простейшая логика
    # Если это reply, можно тоже учитывать, но здесь пропустим.
    
    llm_answer = generate_response_for_text(user_text)
    return f"[TEXT HANDLER] LLM says: {llm_answer}"```

