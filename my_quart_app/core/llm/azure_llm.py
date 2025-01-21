# core/llm/azure_llm.py

from .base_llm import BaseLLM

class AzureLLM(BaseLLM):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "FAKE_AZURE_KEY"

    def generate(self, prompt: str) -> str:
        return f"[Azure-Stub] Ответ (генерация) на промпт: '{prompt}'"