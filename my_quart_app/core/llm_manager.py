# core/llm_manager.py

import os
from .llm.openai_llm import OpenAILLM
from .llm.azure_llm import AzureLLM
from .llm.google_llm import GoogleLLM

class LLMManager:
    _llms = {}

    @classmethod
    def init_all_llms(cls):
        """
        Инициализирует все наши LLM (заглушки).
        В реальном проекте здесь можно читать .env, config и т.д.
        """
        cls._llms["openai"] = OpenAILLM(api_key=os.getenv("OPENAI_API_KEY"))
        cls._llms["azure"] = AzureLLM(api_key=os.getenv("AZURE_API_KEY"))
        cls._llms["google"] = GoogleLLM(api_key=os.getenv("GOOGLE_API_KEY"))

    @classmethod
    def get_llm_for_task(cls, task_type: str):
        """
        Возвращаем LLM-объект для нужного типа задачи.
        В нашем демо:
          - 'text' обрабатываем OpenAI
          - 'image' обрабатываем Azure
          - 'audio' обрабатываем Google
          - при других типах - default OpenAI
        """
        if not cls._llms:
            cls.init_all_llms()

        if task_type == "text":
            return cls._llms["openai"]
        elif task_type == "image":
            return cls._llms["azure"]
        elif task_type == "audio":
            return cls._llms["google"]
        else:
            return cls._llms["openai"]  # fallback