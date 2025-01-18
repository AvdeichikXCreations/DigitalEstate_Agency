# handlers/text_handler.py

# handlers/text_handler.py

from core.llm_controller import generate_response_for_text

def handle_text(message: dict) -> str:
    """
    Получаем текст, вызываем LLM (OpenAI stub).
    """
    user_text = message.get("text", "")
    
    # Простейшая логика
    # Если это reply, можно тоже учитывать, но здесь пропустим.
    
    llm_answer = generate_response_for_text(user_text)
    return f"[TEXT HANDLER] LLM says: {llm_answer}"