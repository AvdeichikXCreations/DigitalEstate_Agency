

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
    return jsonify({"deleted_count": result.deleted_count}), 200