# handlers/video_handler.py

from core.llm_controller import generate_response_for_video

async def handle_video(message: dict, user_id: str) -> str:
    """
    Аналогичный stub для видео.
    """
    caption = message.get("caption")
    description = caption or "No description"
    
    llm_answer = await generate_response_for_video(user_id, description)
    return f"[VIDEO HANDLER] LLM says: {llm_answer}"