# core/llm/google_llm.py

from .base_llm import BaseLLM

class GoogleLLM(BaseLLM):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "FAKE_GOOGLE_KEY"

    def generate(self, prompt: str) -> str:
        return f"[Google-Stub] Ответ (генерация) на промпт: '{prompt}'"