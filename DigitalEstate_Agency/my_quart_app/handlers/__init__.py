# handlers/__init__.py

import logging
from .text_handler import handle_text
from .photo_handler import handle_photo
from .video_handler import handle_video
from .audio_handler import handle_audio

async def get_response_for_message(message: dict, user_id: str) -> str:
    """
    Асинхронный диспетчер типов сообщения.
    """
    text = message.get("text")
    photos = message.get("photo")
    video = message.get("video")
    audio = message.get("audio")
    voice = message.get("voice")
    caption = message.get("caption")

    logging.info(f"[HANDLERS] Dispatching message for user_id={user_id}; type=text? {bool(text)}, photo? {bool(photos)}, video? {bool(video)}, audio? {bool(audio or voice)}")

    if text:
        return await handle_text(message, user_id)
    elif photos:
        return await handle_photo(message, user_id)
    elif video:
        return await handle_video(message, user_id)
    elif audio or voice:
        return await handle_audio(message, user_id)
    else:
        logging.info(f"[HANDLERS] Unknown message type for user_id={user_id}")
        return "[DISPATCHER] Unknown type of message"