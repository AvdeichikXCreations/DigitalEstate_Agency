# core/llm_controller.py

import os
import logging
from datetime import datetime
from typing import Optional

from .llm_manager import LLMManager
from .dialog_history_manager import AsyncDialogHistoryManager

# Загружаем конфиги/переменные окружения (URI, имя БД и коллекции)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "Chat_bot"
COLLECTION_NAME = "Test_history_dialog"

# Создаём глобальный экземпляр нашего асинхронного менеджера истории
history_manager = AsyncDialogHistoryManager(
    mongo_uri=MONGO_URI,
    db_name=DB_NAME,
    collection_name=COLLECTION_NAME
)

async def generate_response_for_text(
    user_id: str,
    user_message: str
) -> str:
    """
    Асинхронная функция генерации ответа на текстовое сообщение.
    user_id: уникальный идентификатор пользователя (email, телеграм-id и т.д.)
    user_message: текст пользователя
    """
    logging.info(f"[LLM_CONTROLLER] generate_response_for_text called with user_id={user_id}, user_message='{user_message}'")

    llm = LLMManager.get_llm_for_task("text")
    prompt = f"User says: {user_message}. Provide a helpful text answer."

    logging.info(f"[LLM_CONTROLLER] Prompt for text = '{prompt}'")

    # Генерируем ответ (синхронным вызовом, т.к. LLMManager у нас — заглушка)
    bot_answer = llm.generate(prompt)

    logging.info(f"[LLM_CONTROLLER] LLM answered (text): '{bot_answer}'. Now saving to DB...")

    # Сохраняем пару (user_message, bot_answer) в историю
    await history_manager.save_dialog_pair(
        user_id=user_id,
        user_message=user_message,
        assistant_message=bot_answer,
        channel="widget_or_any",
        tags=["text_interaction"],
        system_prompt="system:You are a helpful assistant.",
        timestamp=datetime.utcnow()
    )

    logging.info("[LLM_CONTROLLER] Saved dialog pair in DB successfully (text).")
    return bot_answer


async def generate_response_for_image(
    user_id: str,
    description: str
) -> str:
    """
    Асинхронная функция для обработки изображений.
    description — описание картинки, которое вы как-то получили.
    """
    logging.info(f"[LLM_CONTROLLER] generate_response_for_image called with user_id={user_id}, description='{description}'")

    llm = LLMManager.get_llm_for_task("image")
    prompt = f"User sent an image with description: {description}."
    logging.info(f"[LLM_CONTROLLER] Prompt for image = '{prompt}'")

    bot_answer = llm.generate(prompt)

    logging.info(f"[LLM_CONTROLLER] LLM answered (image): '{bot_answer}'. Now saving to DB...")

    await history_manager.save_dialog_pair(
        user_id=user_id,
        user_message=f"[IMAGE DESC]: {description}",
        assistant_message=bot_answer,
        channel="image_channel",
        tags=["image_interaction"],
        system_prompt="system: You are an image-processing assistant.",
        timestamp=datetime.utcnow()
    )

    logging.info("[LLM_CONTROLLER] Saved dialog pair in DB successfully (image).")
    return bot_answer


async def generate_response_for_video(
    user_id: str,
    description: str
) -> str:
    """
    Аналогичный подход для видео.
    """
    logging.info(f"[LLM_CONTROLLER] generate_response_for_video called with user_id={user_id}, description='{description}'")

    llm = LLMManager.get_llm_for_task("image")  # или "text" — как в демо
    prompt = f"User sent a video. Additional info: {description}."
    logging.info(f"[LLM_CONTROLLER] Prompt for video = '{prompt}'")

    bot_answer = llm.generate(prompt)

    logging.info(f"[LLM_CONTROLLER] LLM answered (video): '{bot_answer}'. Now saving to DB...")

    await history_manager.save_dialog_pair(
        user_id=user_id,
        user_message=f"[VIDEO DESC]: {description}",
        assistant_message=bot_answer,
        channel="video_channel",
        tags=["video_interaction"],
        system_prompt="system: You handle video queries.",
        timestamp=datetime.utcnow()
    )

    logging.info("[LLM_CONTROLLER] Saved dialog pair in DB successfully (video).")
    return bot_answer


async def generate_response_for_audio(
    user_id: str,
    text_from_audio: str
) -> str:
    """
    Асинхронная функция для обработки аудио.
    text_from_audio — результат распознавания голоса.
    """
    logging.info(f"[LLM_CONTROLLER] generate_response_for_audio called with user_id={user_id}, text_from_audio='{text_from_audio}'")

    llm = LLMManager.get_llm_for_task("audio")
    prompt = f"Transcribed user voice: '{text_from_audio}'. Please respond."
    logging.info(f"[LLM_CONTROLLER] Prompt for audio = '{prompt}'")

    bot_answer = llm.generate(prompt)

    logging.info(f"[LLM_CONTROLLER] LLM answered (audio): '{bot_answer}'. Now saving to DB...")

    await history_manager.save_dialog_pair(
        user_id=user_id,
        user_message=f"[AUDIO TEXT]: {text_from_audio}",
        assistant_message=bot_answer,
        channel="audio_channel",
        tags=["audio_interaction"],
        system_prompt="system: You handle audio queries.",
        timestamp=datetime.utcnow()
    )

    logging.info("[LLM_CONTROLLER] Saved dialog pair in DB successfully (audio).")
    return bot_answer