# handlers/__init__.py

# handlers/__init__.py

from .text_handler import handle_text
from .photo_handler import handle_photo
from .video_handler import handle_video
from .audio_handler import handle_audio

def get_response_for_message(message: dict) -> str:
    text = message.get("text")
    photos = message.get("photo")
    video = message.get("video")
    audio = message.get("audio")
    voice = message.get("voice")
    caption = message.get("caption")

    if text:
        return handle_text(message)
    elif photos:
        return handle_photo(message)
    elif video:
        return handle_video(message)
    elif audio or voice:
        return handle_audio(message)
    else:
        return "[DISPATCHER] Unknown type of message"