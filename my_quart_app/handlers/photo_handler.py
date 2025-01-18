# handlers/photo_handler.py

# handlers/photo_handler.py

from core.llm_controller import generate_response_for_image

def handle_photo(message: dict) -> str:
    """
    Обработка фото. Допустим, мы не скачиваем картинку,
    а просто берём caption как 'description'.
    """
    caption = message.get("caption")
    description = caption or "No description"
    
    llm_answer = generate_response_for_image(description)
    return f"[PHOTO HANDLER] LLM says: {llm_answer}"