# core/llm/base_llm.py

from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Заглушка: сгенерировать ответ на переданный prompt.
        """
        pass