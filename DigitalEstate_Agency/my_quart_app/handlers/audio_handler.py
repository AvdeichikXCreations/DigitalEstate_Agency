# handlers/audio_handler.py

from core.llm_controller import generate_response_for_audio

async def handle_audio(message: dict, user_id: str) -> str:
    """
    Допустим, у нас есть audio/voice.
    Мы не делаем реальное распознавание,
    а просто берём caption или "Audio file" как 'text_from_audio'.
    """
    caption = message.get("caption")
    transcribed_text = caption or "Voice or audio with no text"
    
    llm_answer = await generate_response_for_audio(user_id, transcribed_text)
    return f"[AUDIO HANDLER] LLM says: {llm_answer}"