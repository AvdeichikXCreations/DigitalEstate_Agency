# handlers/photo_handler.py

import logging
from core.llm_controller import generate_response_for_image

async def handle_photo(message: dict, user_id: str) -> str:
    caption = message.get("caption")
    description = caption or "No description"
    logging.info(f"[PHOTO_HANDLER] user_id={user_id}, description={description}")

    llm_answer = await generate_response_for_image(user_id, description)

    logging.info(f"[PHOTO_HANDLER] LLM answer: {llm_answer}")
    return f"[PHOTO HANDLER] LLM says: {llm_answer}"