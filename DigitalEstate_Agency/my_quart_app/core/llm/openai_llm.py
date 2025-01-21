# core/llm/openai_llm.py

from .base_llm import BaseLLM

class OpenAILLM(BaseLLM):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "FAKE_OPENAI_KEY"

    def generate(self, prompt: str) -> str:
        # Заглушка — просто возвращаем строку, имитируя, что обратились к OpenAI
        return f"[OpenAI-Stub] Вот ответ на ваш промпт: '{prompt}'"