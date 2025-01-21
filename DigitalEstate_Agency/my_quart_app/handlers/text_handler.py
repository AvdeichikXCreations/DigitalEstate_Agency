# handlers/text_handler.py

import logging
from core.llm_controller import generate_response_for_text

async def handle_text(message: dict, user_id: str) -> str:
    """
    Асинхронная обработка текстового сообщения.
    """
    user_text = message.get("text", "")
    logging.info(f"[TEXT_HANDLER] Handling text for user_id={user_id}, text='{user_text}'")

    # ВАЖНО: вызывать через await
    llm_answer = await generate_response_for_text(user_id, user_text)

    logging.info(f"[TEXT_HANDLER] LLM answer for user_id={user_id}: {llm_answer}")
    return f"[TEXT HANDLER] LLM says: {llm_answer}"