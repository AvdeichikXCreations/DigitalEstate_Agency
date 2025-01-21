

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
        return jsonify({"status": "updated", "new_prompt": new_prompt}), 200