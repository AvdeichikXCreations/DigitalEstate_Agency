

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
    return jsonify({"status": "ok", "source": "umnico", "data": data}), 200