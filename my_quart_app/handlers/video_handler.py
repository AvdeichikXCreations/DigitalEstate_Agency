# handlers/video_handler.py

# handlers/video_handler.py

from core.llm_controller import generate_response_for_video

def handle_video(message: dict) -> str:
    """
    Аналогичный stub для видео.
    """
    caption = message.get("caption")
    description = caption or "No description"
    
    llm_answer = generate_response_for_video(description)
    return f"[VIDEO HANDLER] LLM says: {llm_answer}"