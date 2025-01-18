# core/llm_controller.py

from .llm_manager import LLMManager

def generate_response_for_text(user_message: str) -> str:
    """
    Демонстрация: текст → используем 'text' -> OpenAI
    """
    llm = LLMManager.get_llm_for_task("text")
    prompt = f"User says: {user_message}. Provide a helpful text answer."
    return llm.generate(prompt)

def generate_response_for_image(description: str) -> str:
    """
    Демонстрация: фото → используем 'image' -> Azure
    description — это описание фото, если мы его как-то получили
    """
    llm = LLMManager.get_llm_for_task("image")
    prompt = f"User sent an image with description: {description}."
    return llm.generate(prompt)

def generate_response_for_video(description: str) -> str:
    """
    Пусть тоже пользуемся 'image' (или openai) — на ваш выбор.
    Здесь только заглушка
    """
    llm = LLMManager.get_llm_for_task("image")  # или "text"
    prompt = f"User sent a video. Additional info: {description}."
    return llm.generate(prompt)

def generate_response_for_audio(text_from_audio: str) -> str:
    """
    Голос → используем 'audio' -> Google LLM
    text_from_audio — предполагаем, что вы как-то уже распознали речь
    """
    llm = LLMManager.get_llm_for_task("audio")
    prompt = f"Transcribed user voice: '{text_from_audio}'. Please respond."
    return llm.generate(prompt)