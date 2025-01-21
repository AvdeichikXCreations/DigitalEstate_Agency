

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
    return jsonify({"status": "ok", "source": "widget", "data": data}), 200