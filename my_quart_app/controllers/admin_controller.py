

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
        return jsonify({"status": "updated", "new_config": data}), 200