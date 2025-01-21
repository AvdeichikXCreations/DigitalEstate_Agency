# core/dialog_history_manager.py

import logging
from typing import List, Optional
from datetime import datetime, timedelta

# Вместо from pymongo import MongoClient -- используем Motor:
from motor.motor_asyncio import AsyncIOMotorClient

class AsyncDialogHistoryManager:
    def __init__(self, mongo_uri: str, db_name: str, collection_name: str):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        logging.info(
            f"[DialogHistoryManager] Connected to Mongo at {mongo_uri}, "
            f"DB='{db_name}', Collection='{collection_name}'"
        )

    async def save_dialog_pair(
        self,
        user_id: str,
        user_message: str,
        assistant_message: str,
        channel: Optional[str] = None,
        tags: Optional[List[str]] = None,
        system_prompt: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> None:
        """
        Асинхронно сохраняет пару (user_message, assistant_message) в массив messages
        внутри документа с _id = user_id (upsert).
        Если документа нет — создаёт (upsert=True).
        """
        if timestamp is None:
            timestamp = datetime.utcnow()

        dialog_entry = {
            "user_message": user_message,
            "assistant_message": assistant_message,
            "channel": channel,
            "tags": tags if tags else [],
            "system_prompt": system_prompt,
            "timestamp": timestamp
        }

        logging.info(
            f"[DialogHistoryManager] Saving dialog pair for user_id={user_id}: "
            f"{dialog_entry}"
        )

        result = await self.collection.update_one(
            {"_id": user_id},
            {
                "$setOnInsert": {"_id": user_id},
                "$push": {"messages": dialog_entry}
            },
            upsert=True
        )

        logging.info(
            f"[DialogHistoryManager] update_one result: matched={result.matched_count}, "
            f"modified={result.modified_count}, upserted_id={result.upserted_id}"
        )

    async def get_dialog_history(
        self,
        user_id: str,
        since_minutes: Optional[int] = None,
        since_hours: Optional[int] = None,
        since_days: Optional[int] = None,
        limit: Optional[int] = None,
        tags_filter: Optional[List[str]] = None,
        channel_filter: Optional[str] = None
    ) -> List[dict]:
        """
        Асинхронно извлекает (часть) истории диалога с фильтрами (по времени, количеству, тегам, каналу).
        Возвращает список словарей (user_message, assistant_message, channel, timestamp, ...).
        """
        logging.info(
            f"[DialogHistoryManager] get_dialog_history called for user_id={user_id}, "
            f"limit={limit}, since_days={since_days}, tags_filter={tags_filter}, channel_filter={channel_filter}"
        )

        doc = await self.collection.find_one({"_id": user_id})
        if not doc:
            logging.info(f"[DialogHistoryManager] No document found for user_id={user_id}, returning empty list.")
            return []

        all_messages = doc.get("messages", [])
        logging.info(f"[DialogHistoryManager] Found {len(all_messages)} total messages for user_id={user_id}")

        # 1) Фильтрация по времени
        if since_minutes or since_hours or since_days:
            now = datetime.utcnow()
            delta = timedelta(
                minutes=since_minutes or 0,
                hours=since_hours or 0,
                days=since_days or 0
            )
            threshold_time = now - delta

            before_filter_count = len(all_messages)
            all_messages = [m for m in all_messages if m["timestamp"] >= threshold_time]
            logging.info(
                f"[DialogHistoryManager] Time filter removed {before_filter_count - len(all_messages)} messages."
            )

        # 2) Фильтрация по тегам
        if tags_filter:
            def has_intersection(msg_tags, filter_tags):
                return any(t in msg_tags for t in filter_tags)

            before_filter_count = len(all_messages)
            all_messages = [
                m for m in all_messages
                if has_intersection(m.get("tags", []), tags_filter)
            ]
            logging.info(
                f"[DialogHistoryManager] Tags filter removed {before_filter_count - len(all_messages)} messages."
            )

        # 3) Фильтрация по каналу
        if channel_filter:
            before_filter_count = len(all_messages)
            all_messages = [
                m for m in all_messages if m.get("channel") == channel_filter
            ]
            logging.info(
                f"[DialogHistoryManager] Channel filter removed {before_filter_count - len(all_messages)} messages."
            )

        # 4) Сортируем по timestamp (от старых к новым)
        all_messages.sort(key=lambda x: x["timestamp"])

        # 5) Применяем limit (если нужно)
        if limit is not None and limit > 0 and len(all_messages) > limit:
            all_messages = all_messages[-limit:]

        logging.info(f"[DialogHistoryManager] Returning {len(all_messages)} messages after all filters.")
        return all_messages

    def format_history_as_markdown(self, messages: List[dict]) -> str:
        """
        Превращает список сообщений в Markdown-строку.
        """
        logging.info("[DialogHistoryManager] Formatting messages as Markdown.")
        lines = []
        for m in messages:
            user_part = f"**User**: {m['user_message']}"
            assistant_part = f"**Assistant**: {m['assistant_message']}"
            lines.append(user_part)
            lines.append(assistant_part)
            lines.append("")  # пустая строка для визуального разделения

        return "\n".join(lines)