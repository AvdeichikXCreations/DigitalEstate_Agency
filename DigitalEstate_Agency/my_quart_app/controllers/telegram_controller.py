# controllers/telegram_controller.py

import os
import logging
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

    # ЛОГИРУЕМ входящее сообщение
    logging.info(f"[TELEGRAM_WEBHOOK] Received message from chat_id={chat_id}: {message}")

    # ВАЖНО: вызываем АСИНХРОННУЮ функцию через await 
    user_reply = await get_response_for_message(message, user_id=str(chat_id))

    if user_reply:
        send_telegram_message(chat_id, user_reply)
    
    return jsonify({"ok": True, "description": "Message processed"}), 200

def send_telegram_message(chat_id: int, text: str):
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is not set! Can't send message.")
        return
    
    url = f"{BASE_TELEGRAM_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        logging.info(f"[TELEGRAM] Sent message to chat_id={chat_id}")
    else:
        logging.error(f"[TELEGRAM] Failed to send message: {response.text}")