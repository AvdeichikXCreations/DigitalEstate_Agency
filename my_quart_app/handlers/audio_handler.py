# handlers/audio_handler.py

# handlers/audio_handler.py

from core.llm_controller import generate_response_for_audio

def handle_audio(message: dict) -> str:
    """
    Допустим, у нас есть audio/voice.
    Мы не делаем реальное распознавание,
    а просто берём caption или "Audio file" как 'text_from_audio'.
    """
    caption = message.get("caption")
    transcribed_text = caption or "Voice or audio with no text"
    
    llm_answer = generate_response_for_audio(transcribed_text)
    return f"[AUDIO HANDLER] LLM says: {llm_answer}"